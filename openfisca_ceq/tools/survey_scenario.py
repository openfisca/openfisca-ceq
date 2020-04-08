import logging
import pandas as pd

from openfisca_core import periods

from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_ceq.tools.tax_benefit_system_ceq_completion import ceq
from openfisca_ceq.tools.indirect_taxation.tax_benefit_system_indirect_taxation_completion import (
    add_coicop_item_to_tax_benefit_system)
from openfisca_ceq.tools.data.expenditures_loader import load_expenditures
from openfisca_ceq.tools.data.income_loader import build_income_dataframes
from openfisca_ceq.tools.data.income_targets import read_income_target
from openfisca_ceq.tools.data_ceq_correspondence import (
    ceq_input_by_harmonized_variable,
    ceq_intermediate_by_harmonized_variable,
    data_by_model_weight_variable,
    model_by_data_id_variable,
    non_ceq_input_by_harmonized_variable,
    other_model_by_harmonized_person_variable,
    )

from openfisca_cote_d_ivoire import CountryTaxBenefitSystem as CoteDIvoireTaxBenefitSystem
from openfisca_mali import CountryTaxBenefitSystem as MaliTaxBenefitSystem
from openfisca_senegal import CountryTaxBenefitSystem as SenegalTaxBenefitSystem


log = logging.getLogger(__name__)


tax_benefit_system_class_by_country = dict(
    cote_d_ivoire = CoteDIvoireTaxBenefitSystem,
    mali = MaliTaxBenefitSystem,
    senegal = SenegalTaxBenefitSystem,
    )


class CEQSurveyScenario(AbstractSurveyScenario):
    weight_variable_by_entity = dict(
        household = 'household_weight',
        person = 'person_weight',
        )
    legislation_coutry = None
    data_country = None
    varying_variable = None

    def __init__(self, tax_benefit_system = None, baseline_tax_benefit_system = None, year = None,
            data = None, use_marginal_tax_rate = False, varying_variable = None, variation_factor = 0.03):
        super(CEQSurveyScenario, self).__init__()
        assert year is not None
        self.year = year

        assert tax_benefit_system is not None
        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            )

        if use_marginal_tax_rate:
            assert varying_variable is not None
            assert varying_variable in self.tax_benefit_system.variables
            self.variation_factor = variation_factor
            self.varying_variable = varying_variable

        if data is None:
            return

        if 'input_data_frame_by_entity_by_period' in data:
            period = periods.period(year)
            dataframe_variables = set()
            for entity_dataframe in data['input_data_frame_by_entity_by_period'][period].values():
                if not isinstance(entity_dataframe, pd.DataFrame):
                    continue
                dataframe_variables = dataframe_variables.union(set(entity_dataframe.columns))
            self.used_as_input_variables = list(
                set(tax_benefit_system.variables.keys()).intersection(dataframe_variables)
                )

        elif 'input_data_frame' in data:
            input_data_frame = data.get('input_data_frame')
            self.used_as_input_variables = list(
                set(tax_benefit_system.variables.keys()).intersection(
                    set(input_data_frame.columns)
                    )
                )

        self.init_from_data(data = data, use_marginal_tax_rate = use_marginal_tax_rate)

    def inflate_variables_sum_to_target(self, income_variables, target, period):
        for income_variable in income_variables:
            assert income_variable in self.tax_benefit_system.variables

        aggregate = sum(
            self.compute_aggregate(income_variable, period = period)
            for income_variable in income_variables
            )
        inflator = target / aggregate
        inflator_by_variable = dict(
            (income_variable, inflator)
            for income_variable in income_variables
            )
        self.inflate(inflator_by_variable = inflator_by_variable, period = period)


def build_ceq_data(country, year = None):
    household_expenditures = load_expenditures(country)
    person, household_income = build_income_dataframes(country)

    households_missing_in_income = set(household_expenditures.hh_id).difference(
        set(household_income.hh_id))
    if households_missing_in_income:
        log.debug("Households missing in income: \n {}".format(households_missing_in_income))
    households_missing_in_expenditures = set(household_income.hh_id).difference(set(household_expenditures.hh_id))
    if households_missing_in_expenditures:
        log.debug("Households missing in expenditures: \n {}".format(households_missing_in_expenditures))

    household = household_income.merge(household_expenditures, on = "hh_id", how = "left")
    log.info(
        "{}: keeping only {} households from income data but {} are present in expenditures data".format(
            country, len(household_income.hh_id.unique()), len(household_expenditures.hh_id.unique())
            )
        )

    person.rename(columns = {"cov_i_lien_cm": "household_role_index"}, inplace = True)
    if person.household_role_index.dtype.name == 'category':
        if country == "mali":
            log.info("{}: there are {} NaN household_role_index".format(
                country,
                person.household_role_index.isnull().sum(),
                ))
            person = person.loc[person.household_role_index.notnull()].copy()

        assert person.household_role_index.notnull().all()
        person.household_role_index = person.household_role_index.cat.codes.clip(0, 3)

        if country == "mali":
            person.loc[
                (person.hh_id == "098105") & (person.household_role_index == 0),
                "household_role_index"
                ] = (0, 1)

        one_personne_de_reference = (person
            .query("household_role_index == 0")
            .groupby("hh_id")['household_role_index']
            .count() == 1)

        problematic_hh_id = one_personne_de_reference.loc[~one_personne_de_reference].index.tolist()
        assert one_personne_de_reference.all(), "Problem with households: {}".format(
            person.loc[person.hh_id.isin(problematic_hh_id), ["household_role_index", "hh_id"]]
            )

        if country == "mali":
            hh_id_with_missing_personne_de_reference = set(household.hh_id).difference(
                set(
                    person.loc[person.household_role_index == 0, 'hh_id'].unique()
                    )
                )
            person = person.loc[~person.hh_id.isin(hh_id_with_missing_personne_de_reference)].copy()
            household = household.loc[~household.hh_id.isin(hh_id_with_missing_personne_de_reference)].copy()

    else:
        assert person.household_role_index.min() == 1
        person.household_role_index = (person.household_role_index - 1).clip(0, 3).astype(int)

    assert (person.household_role_index == 0).sum() == len(household), (
        "Only {} personne de reference for {} households".format(
            (person.household_role_index == 0).sum(), len(household)),
        "Household without personne de reference are: {}".format(
            set(household.hh_id).difference(
                set(
                    person.loc[person.household_role_index == 0, 'hh_id'].unique()
                    )
                )
            )
        )

    assert (person.household_role_index == 0).sum() == len(person.hh_id.unique()), (
        "Only {} personne de reference for {} unique households IDs".format(
            (person.household_role_index == 0).sum(), len(person.hh_id.unique())
            )
        )

    model_by_data_weight_variable = {v: k for k, v in data_by_model_weight_variable.items()}

    model_variable_by_person_variable = dict()
    variables = [
        ceq_input_by_harmonized_variable,
        ceq_intermediate_by_harmonized_variable,
        model_by_data_id_variable,
        non_ceq_input_by_harmonized_variable,
        model_by_data_weight_variable,
        other_model_by_harmonized_person_variable,
        ]
    for item in variables:
        model_variable_by_person_variable.update(item)

    household.rename(columns = model_variable_by_person_variable, inplace = True)
    person.rename(columns = model_variable_by_person_variable, inplace = True)

    if pd.api.types.is_numeric_dtype(person.eleve_enseignement_niveau):
        person.eleve_enseignement_niveau = person.eleve_enseignement_niveau.fillna(0).astype(int) - 1

    elif person.eleve_enseignement_niveau.dtype == pd.CategoricalDtype(
            categories = [
                'Maternelle', 'Primaire', 'Secondaire', 'Superieur'],
            ordered = True
            ):  # senegal and mali
        person.eleve_enseignement_niveau = person.eleve_enseignement_niveau.cat.codes

    assert set(person.eleve_enseignement_niveau.unique()) == set(range(-1, 4))
    assert 'person_weight' in person
    assert 'household_weight' in household
    person.person_id = (person.person_id.rank() - 1).astype(int)
    person.household_id = (person.household_id.rank() - 1).astype(int)
    household.household_id = (household.household_id.rank() - 1).astype(int)
    input_data_frame_by_entity = dict(household = household, person = person)
    input_data_frame_by_entity_by_period = {periods.period(year): input_data_frame_by_entity}
    data = dict(input_data_frame_by_entity_by_period = input_data_frame_by_entity_by_period)
    return data


def build_ceq_survey_scenario(legislation_country, year = None, data_country = None,
        income_variables = [], inflate = False):

    if data_country is None:
        data_country = legislation_country

    CountryTaxBenefitSystem = tax_benefit_system_class_by_country[legislation_country]
    CountryTaxBenefitSystem.legislation_country = legislation_country
    tax_benefit_system = ceq(CountryTaxBenefitSystem(coicop = False))
    add_coicop_item_to_tax_benefit_system(tax_benefit_system, legislation_country)

    data = build_ceq_data(data_country, year)

    scenario = CEQSurveyScenario(
        tax_benefit_system = tax_benefit_system,
        year = year,
        data = data,
        )

    if not inflate:
        return scenario

    assert income_variables
    target = read_income_target(data_country)
    scenario.inflate_variables_sum_to_target(
        target = target,
        income_variables = income_variables,
        period = year
        )

    return scenario


if __name__ == "__main__":
    from openfisca_ceq.tools.data import year_by_country
    import sys
    country = "senegal"
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    log.info(country)
    year = year_by_country[country]
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
