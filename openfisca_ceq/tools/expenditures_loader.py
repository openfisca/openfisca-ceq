import configparser
import logging
import os
import pandas as pd


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import (
    build_label_by_code_coicop,
    )


log = logging.getLogger(__name__)


config_parser = configparser.ConfigParser()
config_parser.read(os.path.join(config_files_directory, 'raw_data.ini'))


def build_consumption_items_list(country):
    df = build_label_by_code_coicop(country, additional_variables = ['prod_id'])
    return df.astype({"prod_id": str})


def load_expenditures(country):
    year_by_country = {
        'mali': 2014,
        'senegal': 2011,
        }
    missing_variables_by_country = {
        'mali': [
            'prix',
            'quantite',
            ],
        'senegal': [
            'prix',
            'quantite',
            ],
        }

    expenditures_variables = ['prod_id', 'hh_id', 'depense', 'quantite', 'prix']
    year = year_by_country[country]
    expenditures_data_path = config_parser.get(country, 'consommation_{}'.format(year))

    expenditures = pd.read_stata(expenditures_data_path)

    country_expenditures_variables = set(expenditures_variables).difference(
        set(missing_variables_by_country.get(country, []))
        )
    assert country_expenditures_variables <= set(expenditures.columns), "{}: missing variables {}".format(
        country,
        set(expenditures_variables).difference(set(expenditures.columns)),
        )

    # Checks
    consumption_items = build_consumption_items_list(country)
    missing_products_in_legislation = set(expenditures.prod_id.unique()).difference(
        set(consumption_items.prod_id.unique()))
    if missing_products_in_legislation:
        log.info("Missing product in legislation: \n {}".format(
            (expenditures
                .reset_index()
                .query("prod_id in @missing_products_in_legislation")
                .filter(items = [
                    'label', 'prod_id'
                    ])
                .drop_duplicates()
                )
            ))
    missing_products_in_expenditures = set(consumption_items.prod_id.unique()).difference(
        set(expenditures.prod_id.unique()))
    if missing_products_in_expenditures:
        log.info("Missing product in legislation: \n {}".format(
            (expenditures
                .reset_index()
                .query("prod_id in @missing_products_in_legislation")
                .filter(items = [
                    'label', 'prod_id'
                    ])
                .drop_duplicates()
                )
            ))

    return expenditures.astype({"prod_id": str})


if __name__ == "__main__":
    country = 'senegal'
