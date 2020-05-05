from slugify import slugify
import logging


from openfisca_core.model_api import Variable, YEAR


log = logging.getLogger(__name__)


GLOBAL_YEAR_START = 1994
GLOBAL_YEAR_STOP = 2019


def generate_specific_tax_base_variables(tax_benefit_system, specific_tax_name, tax_rate_by_code_coicop, null_rates = []):
    reference_rates = sorted(tax_rate_by_code_coicop[specific_tax_name].unique())
    time_varying_rates = 'start' in tax_rate_by_code_coicop.columns
    for specific_tax_rate in reference_rates:
        functions_by_name = dict()
        if time_varying_rates:
            start_years = reference_rates.start.fillna(GLOBAL_YEAR_START).unique()
            stop_years = reference_rates.start.fillna(GLOBAL_YEAR_STOP).unique()  # last year
            years_range = sorted(list(set(start_years + stop_years)))
            year_stop_by_year_start = zip(years_range[:-1], years_range[1:])
        else:
            year_stop_by_year_start = {GLOBAL_YEAR_START: GLOBAL_YEAR_STOP}

        for year_start, year_stop in year_stop_by_year_start.items():
            filter_expression = '({} == @specific_tax_rate)'.format(specific_tax_name)
            if time_varying_rates:
                filter_expression += 'and (start <= @yyear_start) and (stop >= @yyear_stop)'
            postes_coicop = sorted(
                tax_rate_by_code_coicop.query(filter_expression)['code_coicop'].astype(str)
                )

            log.debug('Creating tariff category {} - {} (starting in {} and ending in {}) aggregate expenses with the following products {}'.format(
                specific_tax_name, specific_tax_rate, year_start, year_stop, postes_coicop))

            dated_func = depenses_ht_hst_categorie_function_creator(
                postes_coicop,
                specific_tax_name,
                specific_tax_rate,
                year_start = year_start,
                null_rates = null_rates,
                )
            dated_function_name = "formula_{year_start}".format(year_start = year_start)
            functions_by_name[dated_function_name] = dated_func

        class_name = 'depenses_ht_hst_{}_{}'.format(specific_tax_name, specific_tax_rate)
        definitions_by_name = dict(
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "Dépenses hors taxes hors taxe spécifique {} - {}".format(specific_tax_name, specific_tax_rate),
            definition_period = YEAR,
            )
        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )

        del definitions_by_name, functions_by_name


def depenses_ht_hst_categorie_function_creator(postes_coicop, specific_tax_name, specific_tax_rate, year_start = None, null_rates = []):
    if len(postes_coicop) != 0:

        if (specific_tax_rate is None) or (specific_tax_rate in null_rates):
            def func(entity, period_arg, parameters):
                return sum(entity(
                    'depenses_ht_poste_' + slugify(poste, separator = '_'), period_arg)
                    for poste in postes_coicop
                    )

        else:
            def func(entity, period_arg, parameters):
                rate = parameters(period_arg).prelevements_obligatoires.impots_indirects[specific_tax_name][specific_tax_rate]
                return sum(entity(
                    'depenses_ht_poste_' + slugify(poste, separator = '_'), period_arg)
                    for poste in postes_coicop
                    ) / (1 + rate)

        func.__name__ = "formula_{year_start}".format(year_start = year_start)
        return func

    else:  # To deal with Reform emptying some fiscal categories
        def func(entity, period_arg):
            return 0

    func.__name__ = "formula_{year_start}".format(year_start = year_start)
    return func


def generate_specific_taxes(tax_benefit_system, specific_tax_name, tax_rate_by_code_coicop, null_rates = []):
    reference_rates = sorted(tax_rate_by_code_coicop[specific_tax_name].unique())
    specific_tax_components = list()
    for specific_tax_rate in reference_rates:
        if specific_tax_rate in null_rates:
            continue

        log.debug('Creating specific tax {} - {}'.format(specific_tax_name, specific_tax_rate))

        class_name = '{}_{}'.format(specific_tax_name, specific_tax_rate)

        definitions_by_name = dict(
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "{} - {}".format(specific_tax_name, specific_tax_rate),
            definition_period = YEAR,
            )

        definitions_by_name.update({"formula": create_specific_tax_formula(
            specific_tax_name, specific_tax_rate)})
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )

        specific_tax_components += [class_name]

    class_name = specific_tax_name

    def tariff_total_func(entity, period_arg):
        return sum(
            entity(class_name, period_arg)
            for class_name in specific_tax_components
            )

    tariff_total_func.__name__ = "formula_{year_start}".format(year_start = GLOBAL_YEAR_START)
    definitions_by_name = dict(
        value_type = float,
        entity = tax_benefit_system.entities_by_singular()['household'],
        label = "{} - total".format(specific_tax_name),
        definition_period = YEAR,
        )
    definitions_by_name.update(
        {tariff_total_func.__name__: tariff_total_func}
        )

    tax_benefit_system.add_variable(
        type(class_name, (Variable,), definitions_by_name)
        )


def create_specific_tax_formula(specific_tax_name, specific_tax_rate):
    def func(entity, period_arg, parameters):
        pre_tax_expenses = entity('depenses_ht_hst_{}_{}'.format(specific_tax_name, specific_tax_rate), period_arg)
        rate = parameters(period_arg).prelevements_obligatoires.impots_indirects[specific_tax_name][specific_tax_rate]
        return pre_tax_expenses * rate

    func.__name__ = "formula_{year_start}".format(year_start = GLOBAL_YEAR_START)
    return func



