# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:37:15 2022

@author: Gebruiker
"""

import pandas as pd
from pyomo.environ import *

def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    if type(key) == int:
                        yield (key,) + (subkey,), subvalue
                    else:
                        yield key + (subkey,), subvalue
            else:
                yield key, value

    return dict(items())

class Superstructure:
    def __init__(self, xlsx_file):
        """Initializes the superstructure by getting the indices j,k,i,u and corresponding names
        NOTE: Leave the excel tabs empty besides the corresponding tables"""

        df = pd.read_excel(xlsx_file,'Superstructure j,k')
        j = list(df.iloc[1,2:])
        k = list(df.iloc[2:,1])
        equipment_names = df.iloc[2:, 2:]
        
        
        equipment_names.index = k
        equipment_names.columns = j
        equipment_names.index.name = 'k'
        equipment_names.columns.name = 'j'
        
        df = pd.read_excel(xlsx_file,'Components i')
        i = list(df.iloc[2:,0])
        component_names = df.iloc[2:,1]
        component_names.index = i
        component_names.index.name = 'i'
        
        df = pd.read_excel(xlsx_file,'Range a')
        a = list(df.iloc[2:,0])
        capacity_names = df.iloc[2:,1]
        capacity_names.index = a
        capacity_names.index.name = 'a'
        
        df = pd.read_excel(xlsx_file,'Utilities u')
        u = list(df.iloc[2:,0])
        utilities_names = df.iloc[2:,1]
        utilities_names.index = u
        utilities_names.index.name = 'u'
        
        df = pd.read_excel(xlsx_file,'Supply s')
        s = list(df.iloc[2:,0])
        supply_names = df.iloc[2:,1]
        supply_names.index = s
        supply_names.index.name = 's'
       
        df = pd.read_excel(xlsx_file,'Demand d')
        d = list(df.iloc[2:,0])
        demand_names = df.iloc[2:,1]
        demand_names.index = d
        demand_names.index.name = 'd' 
        
        df = pd.read_excel(xlsx_file,'Products p')
        p = list(df.iloc[2:,0])
        product_names = df.iloc[2:,1]
        product_names.index = p
        product_names.index.name = 'p'
       
        
        g = [1,2,3,4,5,6,7,8,9,10]
        
        self.j = j
        self.k = k
        self.i = i
        self.a = a
        self.u = u
        self.s = s
        self.d = d
        self.p = p
        self.g = g
        self.equipment_names = equipment_names
        self.component_names = component_names
        self.capacity_names = capacity_names
        self.utilities_names = utilities_names
        self.supply_names = supply_names
        self.demand_names = demand_names
        self.product_names = product_names
        print(u)
        print(s)
        print(d)
        print(p)
        
    def get_SF(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'SF j,k,i')
        SF_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        SF_data.columns = columns
        SF_data.index = self.i
        SF_data.columns.names = ['j','k']
        SF_data.index.name = 'i'
        SF_data = SF_data.to_dict()
        SF_data = flatten_dict(SF_data)
        self.SF_data = SF_data
        
    def get_EC(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'EC j,k')
        EC_data = df.iloc[2:,2:]
        EC_data.columns = self.j
        EC_data.index = self.k
        EC_data.columns.name = 'j'
        EC_data.index.name = 'k'
        EC_data = EC_data.to_dict()
        EC_data = flatten_dict(EC_data)
        self.EC_data = EC_data
        
    def get_Demand(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Demand2 d,p')
        Demand_data = df.iloc[2:,2:]
        Demand_data.columns = self.d
        Demand_data.index = self.p
        Demand_data.columns.name = 'd'
        Demand_data.index.name = 'p'
        Demand_data = Demand_data.to_dict()
        Demand_data = flatten_dict(Demand_data)
        self.Demand_data = Demand_data
   
    def get_F0(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Flow0 i')
        F0_data = df.iloc[2:,2]
        F0_data.index = self.i
        F0_data.index.name = 'i'
        F0_data = F0_data.to_dict()
        self.F0_data = F0_data
        
    def get_RatiomR(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'RatiomR j,k,i')
        RatiomR_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        RatiomR_data.columns = columns
        RatiomR_data.index = self.i
        RatiomR_data.columns.names = ['j','k']
        RatiomR_data.index.name = 'i'
        RatiomR_data = RatiomR_data.to_dict()
        RatiomR_data = flatten_dict(RatiomR_data)
        self.RatiomR_data = RatiomR_data
    
    def get_CF(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'CF j,k,i')
        CF_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        CF_data.columns = columns
        CF_data.index = self.i
        CF_data.columns.names = ['j','k']
        CF_data.index.name = 'i'
        CF_data = CF_data.to_dict()
        CF_data = flatten_dict(CF_data)
        self.CF_data = CF_data
        
    def get_SEL(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'SEL j,k,i')
        SEL_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        SEL_data.columns = columns
        SEL_data.index = self.i
        SEL_data.columns.names = ['j','k']
        SEL_data.index.name = 'i'
        SEL_data = SEL_data.to_dict()
        SEL_data = flatten_dict(SEL_data)
        self.SEL_data = SEL_data
        
    def get_MW(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'MW i')
        MW_data = df.iloc[2:,2]
        MW_data.index = self.i
        MW_data.index.name = 'i'
        MW_data = MW_data.to_dict()
        self.MW_data = MW_data
        
    def get_ALPHA(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'alpha i')
        ALPHA_data = df.iloc[2:,2]
        ALPHA_data.index = self.i
        ALPHA_data.index.name = 'i'
        ALPHA_data = ALPHA_data.to_dict()
        self.ALPHA_data = ALPHA_data
        
    def get_Marketdis(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Countries d,k')
        Marketdis_data = df.iloc[2:,2:]
        Marketdis_data.columns = self.d
        Marketdis_data.index = self.k
        Marketdis_data.columns.name = 'd'
        Marketdis_data.index.name = 'k'
        Marketdis_data = Marketdis_data.to_dict()
        Marketdis_data = flatten_dict(Marketdis_data)
        self.Marketdis_data = Marketdis_data
    
    def get_Slope(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'slope j,k,a')
        Slope_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        Slope_data.columns = columns
        Slope_data.index = self.a
        Slope_data.columns.names = ['j','k']
        Slope_data.index.name = 'a'
        Slope_data = Slope_data.to_dict()
        Slope_data = flatten_dict(Slope_data)
        self.Slope_data = Slope_data

    def get_constant(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'constant j,k,a')
        constant_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        constant_data.columns = columns
        constant_data.index = self.a
        constant_data.columns.names = ['j','k']
        constant_data.index.name = 'a'
        constant_data = constant_data.to_dict()
        constant_data = flatten_dict(constant_data)
        self.constant_data = constant_data
        
    def get_LB(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'LB a')
        LB_data = df.iloc[2:,2]
        LB_data.index = self.a
        LB_data.index.name = 'a'
        LB_data = LB_data.to_dict()
        self.LB_data = LB_data
        
    def get_UB(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'UB a')
        UB_data = df.iloc[2:,2]
        UB_data.index = self.a
        UB_data.index.name = 'a'
        UB_data = UB_data.to_dict()
        self.UB_data = UB_data 
        
    def get_Tau(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Tau j,k,u')
        Tau_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        Tau_data.columns = columns
        Tau_data.index = self.u
        Tau_data.columns.names = ['j','k']
        Tau_data.index.name = 'u'
        Tau_data = Tau_data.to_dict()
        Tau_data = flatten_dict(Tau_data)
        self.Tau_data = Tau_data
        
    def get_Uprice(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Uprice u')
        Uprice_data = df.iloc[2:,2]
        Uprice_data.index = self.u
        Uprice_data.index.name = 'u'
        Uprice_data = Uprice_data.to_dict()
        self.Uprice_data = Uprice_data
    
    def get_CCost(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'CCost i')
        CCost_data = df.iloc[2:,2]
        CCost_data.index = self.i
        CCost_data.index.name = 'i'
        CCost_data = CCost_data.to_dict()
        self.CCost_data = CCost_data   
        
    def get_SupplyLoad(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Supply load s')
        SupplyLoad_data = df.iloc[2:,2]
        SupplyLoad_data.index = self.s
        SupplyLoad_data.index.name = 's'
        SupplyLoad_data = SupplyLoad_data.to_dict()
        self.SupplyLoad_data = SupplyLoad_data
        
    def get_Distance(self,xlsx_file):
        df = pd.read_excel(xlsx_file, 'Distance j,k,s')
        Distance_data = df.iloc[3:,2:]
        columns = pd.MultiIndex.from_product([self.j,self.k])
        Distance_data.columns = columns
        Distance_data.index = self.s
        Distance_data.columns.names = ['j','k']
        Distance_data.index.name = 's'
        Distance_data = Distance_data.to_dict()
        Distance_data = flatten_dict(Distance_data)
        self.Distance_data = Distance_data   

        
    def get_results(self,model):
        """Get results from the pyomo model (Logic and flow data)"""
        Flow_data = {(j, k, i): value(flow) for (j, k, i), flow in model.flow.items()}
        Flow_data = pd.DataFrame.from_dict(Flow_data, orient="index", columns=["variable value"])
        Flow_data = Flow_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
        Flow_data = pd.DataFrame(Flow_data)
        Flow_data.index = self.i
        Flow_data.index.name = 'i'
        columns = pd.MultiIndex.from_product([self.j,self.k])
        Flow_data.columns = columns
        Flow_data.columns.names = ['j','k']
        self.Flow_data = Flow_data
        
# =============================================================================
#         Waste_data = {(j, k, i): value(Waste) for (j, k, i), Waste in model.Waste.items()}
#         Waste_data = pd.DataFrame.from_dict(Waste_data, orient="index", columns=["variable value"])
#         Waste_data = Waste_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
#         Waste_data = pd.DataFrame(Waste_data)
#         Waste_data.index = self.i
#         Waste_data.index.name = 'i'
#         columns = pd.MultiIndex.from_product([self.j,self.k])
#         Waste_data.columns = columns
#         Waste_data.columns.names = ['j','k']
#         self.Waste_data = Waste_data
# =============================================================================
        
        
        
        
# =============================================================================
#         SECCost_data = {(j, k, i): value(SECCost) for (j, k, i), SECCost in model.SECCost.items()}
#         SECCost_data = pd.DataFrame.from_dict(SECCost_data, orient="index", columns=["variable value"])
#         SECCost_data = SECCost_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
#         SECCost_data = pd.DataFrame(SECCost_data)
#         SECCost_data.index = self.i
#         SECCost_data.index.name = 'i'
#         columns = pd.MultiIndex.from_product([self.j,self.k])
#         SECCost_data.columns = columns
#         SECCost_data.columns.names = ['j','k']
#         self.SECCost_data = SECCost_data
# =============================================================================
        
        TotSECCost_data = {(j, k, i): value(TotSECCost) for (j, k, i), TotSECCost in model.TotSECCost.items()}
        TotSECCost_data = pd.DataFrame.from_dict(TotSECCost_data, orient="index", columns=["variable value"])
        TotSECCost_data = TotSECCost_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
        TotSECCost_data = pd.DataFrame(TotSECCost_data)
        TotSECCost_data.index = self.i
        TotSECCost_data.index.name = 'i'
        columns = pd.MultiIndex.from_product([self.j,self.k])
        TotSECCost_data.columns = columns
        TotSECCost_data.columns.names = ['j','k']
        self.TotSECCost_data = TotSECCost_data
        print(TotSECCost_data.to_string())
        print()
        
        Logic_data = {(j,k) : value(y) for (j, k), y in model.y.items()}
        Logic_data = pd.DataFrame.from_dict(Logic_data, orient="index", columns=["variable value"])
        Logic_data = Logic_data.values.reshape(len(self.j),len(self.k)).transpose()
        Logic_data = pd.DataFrame(Logic_data)
        Logic_data.index = self.k
        Logic_data.index.name = 'k'
        Logic_data.columns = self.j
        Logic_data.columns.name = 'j'
        self.Logic_data = Logic_data     
        
        Transport_data = {(d,p) : value(Transport) for (d, p), Transport in model.Transport.items()}
        Transport_data = pd.DataFrame.from_dict(Transport_data, orient="index", columns=["variable value"])
        Transport_data = Transport_data.values.reshape(len(self.d),len(self.p)).transpose()
        Transport_data = pd.DataFrame(Transport_data)
        Transport_data.index = self.p
        Transport_data.index.name = 'p'
        Transport_data.columns = self.d
        Transport_data.columns.name = 'd'
        self.Transport_data = Transport_data    
        print(Transport_data.to_string())
        print()
        
        TransportCost_data = {(d,p) : value(TransportCost) for (d, p), TransportCost in model.TransportCost.items()}
        TransportCost_data = pd.DataFrame.from_dict(TransportCost_data, orient="index", columns=["variable value"])
        TransportCost_data = TransportCost_data.values.reshape(len(self.d),len(self.p)).transpose()
        TransportCost_data = pd.DataFrame(TransportCost_data)
        TransportCost_data.index = self.p
        TransportCost_data.index.name = 'p'
        TransportCost_data.columns = self.d
        TransportCost_data.columns.name = 'd'
        self.TransportCost_data = TransportCost_data    
        print(TransportCost_data.to_string())
        print()
        
# =============================================================================
#         Util_data = {(j, k, u): value(Util) for (j, k, u), Util in model.Util.items()}
#         Util_data = pd.DataFrame.from_dict(Util_data, orient="index", columns=["variable value"])
#         Util_data = Util_data.values.reshape(len(self.j)*len(self.k),len(self.u)).transpose()
#         Util_data = pd.DataFrame(Util_data)
#         Util_data.index = self.u
#         Util_data.index.name = 'u'
#         columns = pd.MultiIndex.from_product([self.j,self.k])
#         Util_data.columns = columns
#         Util_data.columns.names = ['j','k']
#         self.Util_data = Util_data
# =============================================================================
        
# =============================================================================
#         TrCOST_data = {(j, k, s): value(TrCost) for (j, k, s), TrCost in model.TrCost.items()}
#         TrCOST_data = pd.DataFrame.from_dict(TrCOST_data, orient="index", columns=["variable value"])
#         TrCOST_data = TrCOST_data.values.reshape(len(self.j)*len(self.k),len(self.s)).transpose()
#         TrCOST_data = pd.DataFrame(TrCOST_data)
#         TrCOST_data.index = self.s
#         TrCOST_data.index.name = 's'
#         columns = pd.MultiIndex.from_product([self.j,self.k])
#         TrCOST_data.columns = columns
#         TrCOST_data.columns.names = ['j','k']
#         self.TrCOST_data = TrCOST_data
# =============================================================================
        
        EQCost_data = {(j,k) : value(EQCost) for (j, k), EQCost in model.EQCost.items()}
        EQCost_data = pd.DataFrame.from_dict(EQCost_data, orient="index", columns=["variable value"])
        EQCost_data = EQCost_data.values.reshape(len(self.j),len(self.k)).transpose()
        EQCost_data = pd.DataFrame(EQCost_data)
        EQCost_data.index = self.k
        EQCost_data.index.name = 'k'
        EQCost_data.columns = self.j
        EQCost_data.columns.name = 'j'
        self.EQCost_data = EQCost_data
        print(EQCost_data)
        print()
        
        Results_data = {(g) : value(Results) for g, Results in model.Results.items()}
        Results_data = pd.DataFrame.from_dict(Results_data, orient="index", columns=["variable value"])
        Results_data = Results_data.values.reshape(len(self.g)).transpose()
        Results_data = pd.DataFrame(Results_data)
        Results_data.index = self.g
        Results_data.index.name = 'g'
        self.Results_data = Results_data
        
        TarProd_data = {(p) : value(TarProd) for p, TarProd in model.TarProd.items()}
        TarProd_data = pd.DataFrame.from_dict(TarProd_data, orient="index", columns=["variable value"])
        TarProd_data = TarProd_data.values.reshape(len(self.p)).transpose()
        TarProd_data = pd.DataFrame(TarProd_data)
        TarProd_data.index = self.p
        TarProd_data.index.name = 'p'
        self.TarProd_data = TarProd_data
        print(TarProd_data)
        print()
        
        Lambda_data = {(u) : value(x) for u, x in model.x.items()}
        Lambda_data = pd.DataFrame.from_dict(Lambda_data, orient="index", columns=["variable value"])
        Lambda_data = Lambda_data.values.reshape(len(self.u)).transpose()
        Lambda_data = pd.DataFrame(Lambda_data)
        Lambda_data.index = self.u
        Lambda_data.index.name = 'u'
        self.Lambda_data = Lambda_data
        print(Lambda_data)
        print()
        
        'Validation of mass balance'
        TESTin_data = {(j,i) : value(TESTin) for (j, i), TESTin in model.TESTin.items()}
        TESTin_data = pd.DataFrame.from_dict(TESTin_data, orient="index", columns=["variable value"])
        TESTin_data = TESTin_data.values.reshape(len(self.j),len(self.i)).transpose()
        TESTin_data = pd.DataFrame(TESTin_data)
        TESTin_data.index = self.i
        TESTin_data.index.name = 'i'
        TESTin_data.columns = self.j
        TESTin_data.columns.name = 'j'
        
        TESTout_data = {(j,i) : value(TESTout) for (j, i), TESTout in model.TESTout.items()}
        TESTout_data = pd.DataFrame.from_dict(TESTout_data, orient="index", columns=["variable value"])
        TESTout_data = TESTout_data.values.reshape(len(self.j),len(self.i)).transpose()
        TESTout_data = pd.DataFrame(TESTout_data)
        TESTout_data.index = self.i
        TESTout_data.index.name = 'i'
        TESTout_data.columns = self.j
        TESTout_data.columns.name = 'j'
        self.TESTin_data = TESTin_data
        self.TESTout_data = TESTout_data
        
        
        
# =============================================================================
#         print()
#         print(TESTin_data)
#         print()
#         print(TESTin_data)
#         print()
# =============================================================================
        
        print(Logic_data)
        print()
        print(Flow_data.to_string())
# =============================================================================
#         print()
#         print(EQCost_data)
# # =============================================================================
# =============================================================================
#         print()
#         print(SECCost_data.to_string())
# =============================================================================
# =============================================================================
#         print()
#         print(TotSECCost_data.to_string())
# =============================================================================
# =============================================================================
#         print()
#         print(Waste_data.to_string())
#         print()
#         print(Util_data.to_string())
# =============================================================================
# =============================================================================
#         print()
#         print(Profit_data.to_string())
# =============================================================================
        print()
        print(Results_data)
        
        
        
    
       