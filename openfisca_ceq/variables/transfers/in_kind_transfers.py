# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_ceq.entities import *


class in_kind_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Government in-kind transfers"

    def formula(household, period):


        in_kind_transfers = (
            education_net_transfers
            + health_net_transfers
            + housing_transfers
            )


class education_net_transfers(Variable):value_type = float
    entity = Household
    definition_period = YEAR
    label = "Education in-kind transfers net of school fees"

    def formula(household, period):
        pre_school = household('pre_school', period)
        primary_education = household('primary_education', period)
        secondary_education = household('secondary_education', period)
        tertiary_education = household('tertiary_education', period)
        school_fees = household('school_fees', period)

        education_net_transfers = (
            pre_school
            + primary_education
            + secondary_education
            + tertiary_education
            - school_fees
            )
        return education_net_transfers


class health_net_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Health in-kind transfers net of copay, fees, etc"

    def formula(household, period):
        health_contributory = household('health_contributory', period)
        health_noncontributory = household('health_noncontributory', period)
        health_in_patient = household('health_in_patient', period)
        health_out_patient = household('health_out_patient', period)
        health_copay_fees = household('health_copay_fees', period)

        health_net_copay_fees = (
            health_contributory
            + health_noncontributory
            - health_in_patient
            - health_out_patient
            - health_copay_fees
            )
        return health_net_copay_fees


class housing_transfers(Variable):value_type = float
    entity = Household
    definition_period = YEAR
    label = "Housing in-kind transfers"

    def formula(household, period):



class pre_school(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Pre-school"


class primary_education(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Primary"


class secondary_education(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Secondary"


class post_secondary_education(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Post-secondary non-tertiary"


class tertiary_education(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Tertiary"


class school_fees(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "School Fees"


class health_net_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Health"


class health_contributory(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Contributory"


class health_noncontributory(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Noncontributory"


class health_in_patient(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "In-patient"


class health_out_patient(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Out-patient"


class health_copay_fees(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Copayments or Fees"
