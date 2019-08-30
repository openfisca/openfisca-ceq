import configparser
import logging
import os
import pandas as pd


from openfisca_survey_manager import default_config_files_directory as config_files_directory

log = logging.getLogger(__name__)


config_parser = configparser.ConfigParser()
config_parser.read(os.path.join(config_files_directory, 'raw_data.ini'))

expenditures_data_path = config_parser.get('mali', 'consommation_2014')
# expenditures_data_path = config_parser.get('senegal', 'consommation_2011')

expenditures = pd.read_stata(expenditures_data_path)

print(expenditures.columns)
for var in expenditures.columns:
    print(expenditures[var].describe())
