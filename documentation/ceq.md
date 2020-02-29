# CEQ concepts

We describe here the various income concepts used by the CEQ framework.

## market income (`market_income`)

- Earned and Unearned Incomes of All Possible Sources and Excluding Government Transfers (`all_income_excluding_transfers`)
- Gifts, proceeds from sale of durables (`gifts_sales_durables`).
- Alimony (`alimony`)
- Autoconsumption (`autoconsumption`)
- Imputed rent for owner occupied housing (`imputed_rent`)
- Other (add more rows if needed) (`other_income`)

```python
market_income = (
    all_income_excluding_transfers
    + gifts_sales_durables
    + alimony
    + autoconsumption
    + imputed_rent
    + other_income
    )
```

## market income plus pensions = market income + pensions - contributions to pensions

- Old-age contributory pensions (`pensions`)
- Total contributions to social security for old-age pensions (`contributions_pensions`)
  - Employer contributions to social security for old-age pensions (`employer_contributions_pensions`)
  - Employee contributions to social security for old-age pensions (`employee_contributions_pensions`)
  - Self-employed contributions to social security for old-age pensions (`self_employed_contributions_pensions`)
- Other (add more rows if needed)

```python
market_income_plus_pensions = market_income + pensions - contributions_pensions
```

## net market income= market income + pensions - contributions_pensions - (direct taxes and contributions to social security that are not directed to old-age pensions)

- Direct Taxes (`direct_taxes`)
  - Personal Income Tax (`personal_income_tax`)
  - Corporate Income Tax (`corporate_income_tax`)
  - Payroll Tax (`payroll_tax`)
  - Taxes on Property (`property_tax`)
  - Other (add more rows if needed) (`other_taxes`)

```python
  direct_taxes = (
      personal_income_tax
      + corporate_income_tax
      + payroll_tax
      + property_tax
      + other_taxes
      )
```
- Total contributions to social security for health (`contributions_health`)
  - Employer contributions to social security for health (`employer_contributions_health`)
  - Employee contributions to social security for health (`employee_contributions_health`)
  - Self-employed contributions to social security for health (`self_employed_contributions_health`)

```python
contributions_health = (
    employer_contributions_health
    + employee_contributions_health
    + self_employed_contributions_health
    )
```

- Total contributions to social security for other contributory programs (such as unemployment insurance) (`other_contributions`)
  - Employer contributions to social security for other contributory programs (such as unemployment insurance and others) (`employer_other_contributions`)
  - Employee contributions to social security for other contributory programs (such as unemployment insurance) (`employee_other_contributions`)
  - Self-employed contributions to social security for other contributory programs (such as unemployment insurance) (`self_employed_other_contributions`)

```python
other_contributions = (
    employer_other_contributions
    + employee_other_contributions
    + self_employed_other_contributions
    )

net_market_income = market_income_plus_pensions - (direct_taxes + contributions_health + other_contributions)
```

## gross income = market income plus pensions + direct transfers

- Social Protection (`direct_transfers`)
   - Social Assistance (`social_assistance`)
     - Conditional and Unconditional Cash Transfers (`cash_transfers`)
        - ADD one row per program analyzed
     - Noncontributory Pensions (`noncontributory_pensions`)
     - Near Cash Transfers (Food, School Uniforms, etc.)  (`near_cash_transfers`)
       - Add one row per program analyzed
   - Social Insurance (`social_insurance`)
      - Other social insurance transfers different from old-age pensions (add more rows if needed)

```python
social_assistance = cash_transfers + noncontributory_pensions + near_cash_transfers
direct_transfers = social_assistance + social_insurance
gross_income = market_income_plus_pensions + direct_transfert
```

## taxable income = gross_income - nontaxable_income

```python
taxable_income = gross income - nontaxable income
```
- Add rows if needed

## disposable income = net market income + direct government transfers

```python
disposable_income = net_market_income + direct_transfers
```
## private consumption

## consumable income = disposable income + indirect subsidies - indirect taxes

- Indirect taxes
  - VAT
  - Sales Tax
  - Excise Taxes
    - Add one row per excise tax analyzed
  - Customs Duties
    - Other (add more rows if needed)
- Indirect subsidies
  - Electricity
  - Fuel
  - Food
  - Agricultural Inputs
  - Other (add more rows if needed)

```python
consumable_income = disposable_income + indirect_subsidies - indirect_taxes
```

## final income = consumable income + government in-kind transfers

- Education (`education_net_transfers`)
  - Pre-school (`pre_school`)
  - Primary (`primary_education`)
  - Secondary (`secondary_education`)
  - Post-secondary non-tertiary (`post_secondary_education`)
  - Tertiary (tertiary_education)
  - School Fees (school_fees)

```python
education_net_transfers = (
    pre_school
    + primary_education
    + secondary_education
    + tertiary_education
    - school_fees
    )
```

- Health (`health_net_transfers`)
  - Contributory (`health_contributory`)
  - Noncontributory (`health_noncontributory`)
  - In-patient (`health_in_patient`)
  - Out-patient (`health_out_patient`)
  - Copayments or Fees (`health_copay_fees`)

```python
health_net_copay_fees = (
  health_contributory
  + health_noncontributory
  - health_in_patient
  - health_out_patient
  - health_copay_fees
  )
```

- Housing (`housing_transfers`)

```python
in_kind_transfers = (
  education_net_transfers
  + health_net_transfers
  + housing_transfers
  )

final_income = consumable_income + in_kind_transfers
```

## Issues : market income

What should we do with corporate_income_tax ?
  - simple for the self-employed
  - distribute macro aggregate using distribution of capital income in the survey (?)

