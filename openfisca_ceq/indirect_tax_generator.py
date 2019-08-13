# -*- coding: utf-8 -*-


import os
import pandas as pd




produits_file_path = os.path.join("/home/benjello/Dropbox/Projet_Micro_Sim/1_CIV/micro_data/exemple_table_produit_CIV.dta")

produits = pd.read_stata(produits_file_path)

print(produits.columns)
taxes = ['tva', 'tax_speciale_1',  'tax_speciale_2', 'tax_import']
taxe = 'tva'
for taxe in taxes:
    print(produits.groupby(['id_produit', taxe])['id_hh'].count())
