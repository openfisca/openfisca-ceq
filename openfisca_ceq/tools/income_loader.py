import configparser
import logging
import os
import pandas as pd


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_ceq.tools.data_ceq_correspondence import (
    ceq_input_by_person_variable,
    ceq_intermediate_by_person_variable,
    household_variables,
    model_by_data_id_variables,
    non_ceq_input_by_person_variable,
    person_variables,
    )


log = logging.getLogger(__name__)


config_parser = configparser.ConfigParser()
config_parser.read(os.path.join(config_files_directory, 'raw_data.ini'))

year_by_country = {
    'mali': 2014,
    'senegal': 2011,
    }


missing_revenus_by_country = {
    'mali': [
        'rev_i_independants_taxe',
        'rev_i_independants_Ntaxe',
        'rev_i_loyers',
        'rev_i_autres_revenus_capital',
        'rev_i_pensions',
        'rev_i_transferts_publics',
        ],
    }


for country, year in year_by_country.items():
    income_data_path = config_parser.get(country, 'revenus_harmonises_{}'.format(year))
    model_variable_by_person_variable = dict()
    for d in [
        ceq_input_by_person_variable,
        ceq_intermediate_by_person_variable,
        model_by_data_id_variables,
        non_ceq_input_by_person_variable,
        ]:
        model_variable_by_person_variable.update(d)

    income = pd.read_stata(income_data_path)

    for var in income.columns:
        if var.startswith("rev"):
            print(var, income[var].notnull().any())

    assert (
        set(model_variable_by_person_variable.keys()).difference(
            set(missing_revenus_by_country.get(country, []))
            )
        <= set(income.columns)
        ), \
        "Missing {} in income data source".format(
            set(model_variable_by_person_variable.keys()).difference(set(income.columns))
            )

    for variables in person_variables:
        data_by_model_id_variables = {v: k for k, v in model_by_data_id_variables.items()}

        filtered_person_variables = list(
            set(person_variables).difference(
                set(missing_revenus_by_country.get(country, [])))
            )

        person_dataframe = income[
            filtered_person_variables
            + [data_by_model_id_variables["person_id"]]
            ]
