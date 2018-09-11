# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_ceq.entities import *


class contributions_pensions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Total contributions to social security for old-age pensions"

    def formula(household, period):
        employee_contributions_pensions = household('employee_contributions_pensions', period)
        employer_contributions_pensions = household('employer_contributions_pensions', period)
        contributions_pensions = (
            employee_contributions_pensions + employer_contributions_pensions
            )
        return contributions_pensions


class employee_contributions_pensions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Employee contributions to social security for old-age pensions"


class employer_contributions_pensions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Employer contributions to social security for old-age pensions"


class self_employed_contribution_old_age_pension(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Self-employed contributions to social security for old-age pensions"
