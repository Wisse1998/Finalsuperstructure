# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:37:15 2022

@author: Gebruiker
"""

import pandas as pd
from Superstructure_classV103 import Superstructure
from Superstructure_modelV103 import Superstructure_model

# 'C:/Users/Gebruiker/iCloudDrive/Master/Thesis/Mathematical formulation/SSdataV1.xlsx'
# 'C:/Users/Gebruiker/iCloudDrive/Master/Thesis/Python/Vincent\SS_dataVINCENT.xlsx'

xlsx_file = 'C:/Users/Gebruiker/iCloudDrive/Master/Thesis/Mathematical formulation/SSdataV103.xlsx'


Superstructure = Superstructure(xlsx_file)
Superstructure.get_SF(xlsx_file)
Superstructure.get_EC(xlsx_file)
Superstructure.get_F0(xlsx_file)
Superstructure.get_RatiomR(xlsx_file)
Superstructure.get_CF(xlsx_file)
Superstructure.get_SEL(xlsx_file)
Superstructure.get_MW(xlsx_file)
Superstructure.get_ALPHA(xlsx_file)
Superstructure.get_UB(xlsx_file)
Superstructure.get_LB(xlsx_file)
Superstructure.get_Slope(xlsx_file)
Superstructure.get_constant(xlsx_file)
Superstructure.get_Uprice(xlsx_file)
Superstructure.get_Tau(xlsx_file)
Superstructure.get_Distance(xlsx_file)
Superstructure.get_SupplyLoad(xlsx_file)
Superstructure.get_CCost(xlsx_file)
Superstructure.get_Demand(xlsx_file)
Superstructure.get_Marketdis(xlsx_file)



##############################################################
model = Superstructure_model(Superstructure)

Superstructure.get_results(model)
