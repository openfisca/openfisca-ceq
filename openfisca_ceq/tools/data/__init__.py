import configparser
import os


from pyxdg import XDG_CONFIG_HOME
import os
config_files_directory = os.path.join(XDG_CONFIG_HOME, 'openfisca-survey-manager')


config_parser = configparser.ConfigParser()
config_parser.read(os.path.join(config_files_directory, 'raw_data.ini'))


year_by_country = {
    'cote_d_ivoire': 2014,
    'mali': 2011,
    'senegal': 2011,
    }


def get_data_file_paths(country, year):
    file_paths = dict(config_parser.items(country))

    for key in ["consommation_{}".format(year), "revenus_harmonises_{}".format(year)]:
        assert key in file_paths, "No path for {}. Available entries are {}".format(
            key, file_paths.keys())

    return file_paths["consommation_{}".format(year)], file_paths["revenus_harmonises_{}".format(year)]
