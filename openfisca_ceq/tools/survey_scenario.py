import logging
import pandas as pd

from openfisca_core import periods
from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_ceq.tools.tax_benefit_system_ceq_completion import ceq
from openfisca_ceq.tools.indirect_taxation.tax_benefit_system_indirect_taxation_completion import (
    add_coicop_item_to_tax_benefit_system)
from openfisca_ceq.tools.expenditures_loader import load_expenditures


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
    weight_column_name_by_entity = dict(
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
                    ))

        self.init_from_data(data = data, use_marginal_tax_rate = use_marginal_tax_rate)


def build_ceq_data(country, year = None):
    expenditures = load_expenditures(country)
    print(expenditures.columns)

    household = expenditures
    person = None
    input_data_frame_by_entity = dict(household = household, person = person)
    input_data_frame_by_entity_by_period = {periods.period(year): input_data_frame_by_entity}
    data = dict(input_data_frame_by_entity_by_period = input_data_frame_by_entity_by_period)
    return data




def build_ceq_survey_scenario(legislation_country, year = None, data_country = None):
    if data_country is None:
        data_country = legislation_country

    CountryTaxBenefitSystem = tax_benefit_system_class_by_country[legislation_country]
    tax_benefit_system = ceq(CountryTaxBenefitSystem())
    add_coicop_item_to_tax_benefit_system(tax_benefit_system, legislation_country)
    data = build_ceq_data(data_country, year)

    scenario = CEQSurveyScenario(
        tax_benefit_system = tax_benefit_system,
        year = year,
        data = data,
        )

    return scenario
