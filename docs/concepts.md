# Concepts de revenu CEQ

Le cœur implémente l'échelle des concepts de revenu du cadre CEQ (Lustig,
*Commitment to Equity Handbook*, 2022). Chaque concept est une variable OpenFisca au
niveau du **ménage** ; les agrégats sont de pures sommes de leurs composantes.

!!! note "Notations"
    Dans la littérature CEQ, le revenu *consommable* (`consumable_income`) est noté **yc**
    et le revenu *final* (`final_income`) **yf**.

## Market income (`market_income`)

Revenus du marché, hors transferts publics.

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

## Market income plus pensions (`market_income_plus_pensions`)

```python
market_income_plus_pensions = market_income + pensions - contributions_pensions
```

où `contributions_pensions = employer_ + employee_ + self_employed_contributions_pensions`.

## Net market income (`net_market_income`)

Retranche les impôts directs et les cotisations hors retraite.

```python
direct_taxes = (
    personal_income_tax + corporate_income_tax + payroll_tax + property_tax + other_taxes
)
contributions_health = (
    employer_ + employee_ + self_employed_contributions_health
)
other_contributions = (
    employer_ + employee_ + self_employed_other_contributions
)
net_market_income = market_income_plus_pensions - (
    direct_taxes + contributions_health + other_contributions
)
```

## Gross income (`gross_income`) et taxable income (`taxable_income`)

```python
social_assistance = cash_transfers + noncontributory_pensions + near_cash_transfers
direct_transfers = social_assistance + social_insurance
gross_income = market_income_plus_pensions + direct_transfers
taxable_income = gross_income - nontaxable_income
```

## Disposable income (`disposable_income`)

```python
disposable_income = net_market_income + direct_transfers
```

## Consumable income — yc (`consumable_income`)

```python
indirect_taxes = value_added_tax + sales_tax + excise_taxes + customs_duties
indirect_subsidies = (
    electricity_subsidies + fuel_subsidies + food_subsidies + agricultural_inputs_subsidies
)
consumable_income = disposable_income + indirect_subsidies - indirect_taxes
```

## Final income — yf (`final_income`)

Ajoute la valeur monétisée des transferts en nature (éducation, santé) au coût moyen
de l'État, nets des frais d'usager.

```python
education_net_transfers = (
    pre_school + primary_education + secondary_education + tertiary_education
    - school_fees
)

health_net_transfers = (
    health_contributory + health_noncontributory
    + health_in_patient + health_out_patient
    - health_copay_fees
)

in_kind_transfers = education_net_transfers + health_net_transfers + housing_transfers
final_income = consumable_income + in_kind_transfers
```

!!! warning "Signe des transferts de santé (corrigé en 2.0)"
    Conformément au manuel CEQ, `health_net_transfers` **additionne** toutes les
    prestations de santé reçues (contributif, non contributif, hospitalier,
    ambulatoire) et ne **retranche que** les co-paiements / frais d'usager
    (`health_copay_fees`). Avant la 2.0, `health_in_patient` et `health_out_patient`
    étaient retranchés à tort.
