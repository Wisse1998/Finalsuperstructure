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
       
        L = [1,2,3,4,5,6,7] 
       
        self.L = L
        self.j = j
        self.k = k
        self.i = i
        self.a = a
        self.u = u
        self.s = s
        self.d = d
        self.p = p
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
        print(L)
        
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
#         print(SECCost_data.to_string())
# =============================================================================
        
# =============================================================================
#         TotSECCost_data = {(j, k, i): value(TotSECCost) for (j, k, i), TotSECCost in model.TotSECCost.items()}
#         TotSECCost_data = pd.DataFrame.from_dict(TotSECCost_data, orient="index", columns=["variable value"])
#         TotSECCost_data = TotSECCost_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
#         TotSECCost_data = pd.DataFrame(TotSECCost_data)
#         TotSECCost_data.index = self.i
#         TotSECCost_data.index.name = 'i'
#         columns = pd.MultiIndex.from_product([self.j,self.k])
#         TotSECCost_data.columns = columns
#         TotSECCost_data.columns.names = ['j','k']
#         self.TotSECCost_data = TotSECCost_data
# =============================================================================
        
        
        Logic_data = {(j,k) : value(y) for (j, k), y in model.y.items()}
        Logic_data = pd.DataFrame.from_dict(Logic_data, orient="index", columns=["variable value"])
        Logic_data = Logic_data.values.reshape(len(self.j),len(self.k)).transpose()
        Logic_data = pd.DataFrame(Logic_data)
        Logic_data.index = self.k
        Logic_data.index.name = 'k'
        Logic_data.columns = self.j
        Logic_data.columns.name = 'j'
        self.Logic_data = Logic_data
        
# =============================================================================
#         IntDist_data = {(d,k) : value(IntDist) for (d, k), IntDist in model.IntDist.items()}
#         IntDist_data = pd.DataFrame.from_dict(IntDist_data, orient="index", columns=["variable value"])
#         IntDist_data = IntDist_data.values.reshape(len(self.d),len(self.k)).transpose()
#         IntDist_data = pd.DataFrame(IntDist_data)
#         IntDist_data.index = self.k
#         IntDist_data.index.name = 'k'
#         IntDist_data.columns = self.d
#         IntDist_data.columns.name = 'd'
#         self.IntDist_data = IntDist_data   
#         print(IntDist_data)
# =============================================================================
        
        Transport1_data = {(d,p) : value(Transport1) for (d, p), Transport1 in model.Transport1.items()}
        Transport1_data = pd.DataFrame.from_dict(Transport1_data, orient="index", columns=["variable value"])
        Transport1_data = Transport1_data.values.reshape(len(self.d),len(self.p)).transpose()
        Transport1_data = pd.DataFrame(Transport1_data)
        Transport1_data.index = self.p
        Transport1_data.index.name = 'p'
        Transport1_data.columns = self.d
        Transport1_data.columns.name = 'd'
        self.Transport1_data = Transport1_data    
        print(Transport1_data.to_string())
        print()
        
        Transport2_data = {(d,p) : value(Transport2) for (d, p), Transport2 in model.Transport2.items()}
        Transport2_data = pd.DataFrame.from_dict(Transport2_data, orient="index", columns=["variable value"])
        Transport2_data = Transport2_data.values.reshape(len(self.d),len(self.p)).transpose()
        Transport2_data = pd.DataFrame(Transport2_data)
        Transport2_data.index = self.p
        Transport2_data.index.name = 'p'
        Transport2_data.columns = self.d
        Transport2_data.columns.name = 'd'
        self.Transport2_data = Transport2_data    
        print(Transport2_data.to_string())
        print()
        
        Transport3_data = {(d,p) : value(Transport3) for (d, p), Transport3 in model.Transport3.items()}
        Transport3_data = pd.DataFrame.from_dict(Transport3_data, orient="index", columns=["variable value"])
        Transport3_data = Transport3_data.values.reshape(len(self.d),len(self.p)).transpose()
        Transport3_data = pd.DataFrame(Transport3_data)
        Transport3_data.index = self.p
        Transport3_data.index.name = 'p'
        Transport3_data.columns = self.d
        Transport3_data.columns.name = 'd'
        self.Transport3_data = Transport3_data    
        print(Transport3_data.to_string())
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
#         print(Util_data.to_string())
#         print()
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
        
        IntTrans1_data = {(j,k) : value(TotInTrans1) for (j, k), TotInTrans1 in model.TotInTrans1.items()}
        IntTrans1_data = pd.DataFrame.from_dict(IntTrans1_data, orient="index", columns=["variable value"])
        IntTrans1_data = IntTrans1_data.values.reshape(len(self.j),len(self.k)).transpose()
        IntTrans1_data = pd.DataFrame(IntTrans1_data)
        IntTrans1_data.index = self.k
        IntTrans1_data.index.name = 'k'
        IntTrans1_data.columns = self.j
        IntTrans1_data.columns.name = 'j'
        self.IntTrans1_data = IntTrans1_data    
        print(IntTrans1_data.to_string())    
        print()
        
        IntTrans2_data = {(j,k) : value(TotInTrans2) for (j, k), TotInTrans2 in model.TotInTrans2.items()}
        IntTrans2_data = pd.DataFrame.from_dict(IntTrans2_data, orient="index", columns=["variable value"])
        IntTrans2_data = IntTrans2_data.values.reshape(len(self.j),len(self.k)).transpose()
        IntTrans2_data = pd.DataFrame(IntTrans2_data)
        IntTrans2_data.index = self.k
        IntTrans2_data.index.name = 'k'
        IntTrans2_data.columns = self.j
        IntTrans2_data.columns.name = 'j'
        self.IntTrans2_data = IntTrans1_data    
        print(IntTrans2_data.to_string())
        print()
    

# =============================================================================
#         TotIntDist_data = {(d) : value(TotIntDist) for d, TotIntDist in model.TotIntDist.items()}
#         TotIntDist_data = pd.DataFrame.from_dict(TotIntDist_data, orient="index", columns=["variable value"])
#         TotIntDist_data = TotIntDist_data.values.reshape(len(self.d)).transpose()
#         TotIntDist_data = pd.DataFrame(TotIntDist_data)
#         TotIntDist_data.index = self.d
#         TotIntDist_data.index.name = 'd'
#         self.TotIntDist_data = TotIntDist_data
#         print(TotIntDist_data)
# =============================================================================
        
        ProductTrans1_data = {(k, d, p): value(ProductTrans1) for (k, d, p), ProductTrans1 in model.ProductTrans1.items()}
        ProductTrans1_data = pd.DataFrame.from_dict(ProductTrans1_data, orient="index", columns=["variable value"])
        ProductTrans1_data = ProductTrans1_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTrans1_data = pd.DataFrame(ProductTrans1_data)
        ProductTrans1_data.index = self.p
        ProductTrans1_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTrans1_data.columns = columns
        ProductTrans1_data.columns.names = ['k','d']
        self.ProductTrans1_data = ProductTrans1_data
        print(ProductTrans1_data.to_string())
        print()
        
        ProductTrans2_data = {(k, d, p): value(ProductTrans2) for (k, d, p), ProductTrans2 in model.ProductTrans2.items()}
        ProductTrans2_data = pd.DataFrame.from_dict(ProductTrans2_data, orient="index", columns=["variable value"])
        ProductTrans2_data = ProductTrans2_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTrans2_data = pd.DataFrame(ProductTrans2_data)
        ProductTrans2_data.index = self.p
        ProductTrans2_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTrans2_data.columns = columns
        ProductTrans2_data.columns.names = ['k','d']
        self.ProductTrans2_data = ProductTrans2_data
        print(ProductTrans2_data.to_string())
        print()
        
        ProductTrans3_data = {(k, d, p): value(ProductTrans3) for (k, d, p), ProductTrans3 in model.ProductTrans3.items()}
        ProductTrans3_data = pd.DataFrame.from_dict(ProductTrans3_data, orient="index", columns=["variable value"])
        ProductTrans3_data = ProductTrans3_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTrans3_data = pd.DataFrame(ProductTrans3_data)
        ProductTrans3_data.index = self.p
        ProductTrans3_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTrans3_data.columns = columns
        ProductTrans3_data.columns.names = ['k','d']
        self.ProductTrans3_data = ProductTrans3_data
        print(ProductTrans3_data.to_string())
        print()
        
        ProductTrans11_data = {(k, d, p): value(ProductTrans11) for (k, d, p), ProductTrans11 in model.ProductTrans11.items()}
        ProductTrans11_data = pd.DataFrame.from_dict(ProductTrans11_data, orient="index", columns=["variable value"])
        ProductTrans11_data = ProductTrans11_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTrans11_data = pd.DataFrame(ProductTrans11_data)
        ProductTrans11_data.index = self.p
        ProductTrans11_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTrans11_data.columns = columns
        ProductTrans11_data.columns.names = ['k','d']
        self.ProductTrans11_data = ProductTrans11_data
        print(ProductTrans11_data.to_string())
        print()
        
        ProductTrans22_data = {(k, d, p): value(ProductTrans22) for (k, d, p), ProductTrans22 in model.ProductTrans22.items()}
        ProductTrans22_data = pd.DataFrame.from_dict(ProductTrans22_data, orient="index", columns=["variable value"])
        ProductTrans22_data = ProductTrans22_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTrans22_data = pd.DataFrame(ProductTrans22_data)
        ProductTrans22_data.index = self.p
        ProductTrans22_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTrans22_data.columns = columns
        ProductTrans22_data.columns.names = ['k','d']
        self.ProductTrans22_data = ProductTrans22_data
        print(ProductTrans22_data.to_string())
        print()
        
        ProductTrans33_data = {(k, d, p): value(ProductTrans33) for (k, d, p), ProductTrans33 in model.ProductTrans33.items()}
        ProductTrans33_data = pd.DataFrame.from_dict(ProductTrans33_data, orient="index", columns=["variable value"])
        ProductTrans33_data = ProductTrans33_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTrans33_data = pd.DataFrame(ProductTrans33_data)
        ProductTrans33_data.index = self.p
        ProductTrans33_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTrans33_data.columns = columns
        ProductTrans33_data.columns.names = ['k','d']
        self.ProductTrans33_data = ProductTrans33_data
        print(ProductTrans33_data.to_string())
        print()
        
        Results_data = {(k) : value(Results) for k, Results in model.Results.items()}
        Results_data = pd.DataFrame.from_dict(Results_data, orient="index", columns=["variable value"])
        Results_data = Results_data.values.reshape(len(self.k)).transpose()
        Results_data = pd.DataFrame(Results_data)
        Results_data.index = self.k
        Results_data.index.name = 'k'
        self.Results_data = Results_data
        print(Results_data)
        print()
        
# =============================================================================
#         TarProd_data = {(p) : value(TarProd) for p, TarProd in model.TarProd.items()}
#         TarProd_data = pd.DataFrame.from_dict(TarProd_data, orient="index", columns=["variable value"])
#         TarProd_data = TarProd_data.values.reshape(len(self.p)).transpose()
#         TarProd_data = pd.DataFrame(TarProd_data)
#         TarProd_data.index = self.p
#         TarProd_data.index.name = 'p'
#         self.TarProd_data = TarProd_data
#         print(TarProd_data)
# =============================================================================
        
# =============================================================================
#         Lambda_data = {(u) : value(x) for u, x in model.x.items()}
#         Lambda_data = pd.DataFrame.from_dict(Lambda_data, orient="index", columns=["variable value"])
#         Lambda_data = Lambda_data.values.reshape(len(self.u)).transpose()
#         Lambda_data = pd.DataFrame(Lambda_data)
#         Lambda_data.index = self.u
#         Lambda_data.index.name = 'u'
#         self.Lambda_data = Lambda_data
#         print(Lambda_data)
# =============================================================================
        
        Lambda_data = {(u,L) : value(x) for (u, L), x in model.x.items()}
        Lambda_data = pd.DataFrame.from_dict(Lambda_data, orient="index", columns=["variable value"])
        Lambda_data = Lambda_data.values.reshape(len(self.u),len(self.L)).transpose()
        Lambda_data = pd.DataFrame(Lambda_data)
        Lambda_data.index = self.L
        Lambda_data.index.name = 'L'
        Lambda_data.columns = self.u
        Lambda_data.columns.name = 'u'
        self.Lambda_data = Lambda_data
        print(Lambda_data)
        print()
        
        
# =============================================================================
#         Profit_data = {(j, k, i): value(Profit) for (j, k, i), Profit in model.Profit.items()}
#         Profit_data = pd.DataFrame.from_dict(Profit_data, orient="index", columns=["variable value"])
#         Profit_data = Profit_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
#         Profit_data = pd.DataFrame(Profit_data)
#         Profit_data.index = self.i
#         Profit_data.index.name = 'i'
#         columns = pd.MultiIndex.from_product([self.j,self.k])
#         Profit_data.columns = columns
#         Profit_data.columns.names = ['j','k']
#         self.Profit_data = Profit_data
#         print(Profit_data.to_string())
# =============================================================================
        
        'Validation of mass balance'
# =============================================================================
#         TESTin_data = {(j,i) : value(TESTin) for (j, i), TESTin in model.TESTin.items()}
#         TESTin_data = pd.DataFrame.from_dict(TESTin_data, orient="index", columns=["variable value"])
#         TESTin_data = TESTin_data.values.reshape(len(self.j),len(self.i)).transpose()
#         TESTin_data = pd.DataFrame(TESTin_data)
#         TESTin_data.index = self.i
#         TESTin_data.index.name = 'i'
#         TESTin_data.columns = self.j
#         TESTin_data.columns.name = 'j'
#         
#         TESTout_data = {(j,i) : value(TESTout) for (j, i), TESTout in model.TESTout.items()}
#         TESTout_data = pd.DataFrame.from_dict(TESTout_data, orient="index", columns=["variable value"])
#         TESTout_data = TESTout_data.values.reshape(len(self.j),len(self.i)).transpose()
#         TESTout_data = pd.DataFrame(TESTout_data)
#         TESTout_data.index = self.i
#         TESTout_data.index.name = 'i'
#         TESTout_data.columns = self.j
#         TESTout_data.columns.name = 'j'
#         self.TESTin_data = TESTin_data
#         self.TESTout_data = TESTout_data
# =============================================================================
        
        
        
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

        
        
        self.AIC = value(model.AIC)
       