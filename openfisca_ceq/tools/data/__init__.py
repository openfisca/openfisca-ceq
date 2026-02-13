import configparser
import os


from pathlib import Path

# Get config directory using XDG Base Directory specification
# Fallback to ~/.config if XDG_CONFIG_HOME is not set
xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
if xdg_config_home:
    config_files_directory = os.path.join(xdg_config_home, 'openfisca-survey-manager')
else:
    config_files_directory = os.path.join(Path.home(), '.config', 'openfisca-survey-manager')


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
