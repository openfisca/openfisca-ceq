import configparser
import logging
import os
import pandas as pd


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_ceq.tools.data_ceq_correspondence import (
    non_ceq_input_by_person_variable,
    ceq_intermediate_by_person_variable,
    ceq_input_by_person_variable,
    )


log = logging.getLogger(__name__)


config_parser = configparser.ConfigParser()
config_parser.read(os.path.join(config_files_directory, 'raw_data.ini'))

# income_data_path = config_parser.get('mali', 'revenus_harmonises_2014')
income_data_path = config_parser.get('senegal', 'revenus_harmonises_2011')

model_variable_by_person_variable = dict()
for d in [non_ceq_input_by_person_variable, ceq_intermediate_by_person_variable, ceq_input_by_person_variable]:
    model_variable_by_person_variable.update(d)


print(income_data_path)

income = pd.read_stata(income_data_path)

assert set(model_variable_by_person_variable.keys()) <= set(income.columns), "Missing {} in income data source".format(
    set(model_variable_by_person_variable.keys()).difference(set(income.columns))
    )

print(income.columns)
for var in income.columns:
    print(income[var].describe())
