# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_ceq.entities import *


class corporate_income_tax(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Corporate Income Tax"


class direct_taxes(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Direct Taxes"

    def formual(household, period):
        personal_income_tax = household('personal_income_tax', period)
        corporate_income_tax = household('corporate_income_tax', period)
        payroll_tax = household('payroll_tax', period)
        property_tax = household('property_tax', period)
        other_taxes = household('other_taxes', period)

        direct_taxes = (
            personal_income_tax
            + corporate_income_tax
            + payroll_tax
            + property_tax
            + other_taxes
            )
        return direct_taxes


class other_taxes(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Other taxes"


class payroll_tax(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Payroll Tax"


class personal_income_tax(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Personal Income Tax"


class property_tax(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Taxes on Property "
