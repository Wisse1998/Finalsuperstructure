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
        
        L = [1,2]
       
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
        print(EC_data)
        
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
        
        Flow1_data = {(j, k, i): value(flow1) for (j, k, i), flow1 in model.flow1.items()}
        Flow1_data = pd.DataFrame.from_dict(Flow1_data, orient="index", columns=["variable value"])
        Flow1_data = Flow1_data.values.reshape(len(self.j)*len(self.k),len(self.i)).transpose()
        Flow1_data = pd.DataFrame(Flow1_data)
        Flow1_data.index = self.i
        Flow1_data.index.name = 'i'
        columns = pd.MultiIndex.from_product([self.j,self.k])
        Flow1_data.columns = columns
        Flow1_data.columns.names = ['j','k']
        self.Flow1_data = Flow1_data
        
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
#         flowstage1_data = {(j,i) : value(flowstage1) for (j, i), flowstage1 in model.flowstage1.items()}
#         flowstage1_data = pd.DataFrame.from_dict(flowstage1_data, orient="index", columns=["variable value"])
#         flowstage1_data = flowstage1_data.values.reshape(len(self.j),len(self.i)).transpose()
#         flowstage1_data = pd.DataFrame(flowstage1_data)
#         flowstage1_data.index = self.i
#         flowstage1_data.index.name = 'i'
#         flowstage1_data.columns = self.j
#         flowstage1_data.columns.name = 'j'
#         self.flowstage1_data = flowstage1_data
#         print(flowstage1_data)
#         
#         flowstage2_data = {(j,i) : value(flowstage2) for (j, i), flowstage2 in model.flowstage2.items()}
#         flowstage2_data = pd.DataFrame.from_dict(flowstage2_data, orient="index", columns=["variable value"])
#         flowstage2_data = flowstage2_data.values.reshape(len(self.j),len(self.i)).transpose()
#         flowstage2_data = pd.DataFrame(flowstage2_data)
#         flowstage2_data.index = self.i
#         flowstage2_data.index.name = 'i'
#         flowstage2_data.columns = self.j
#         flowstage2_data.columns.name = 'j'
#         self.flowstage2_data = flowstage2_data
#         print(flowstage2_data)
#         
#         flowstage_data = {(j,i) : value(flowstage) for (j, i), flowstage in model.flowstage.items()}
#         flowstage_data = pd.DataFrame.from_dict(flowstage_data, orient="index", columns=["variable value"])
#         flowstage_data = flowstage_data.values.reshape(len(self.j),len(self.i)).transpose()
#         flowstage_data = pd.DataFrame(flowstage_data)
#         flowstage_data.index = self.i
#         flowstage_data.index.name = 'i'
#         flowstage_data.columns = self.j
#         flowstage_data.columns.name = 'j'
#         self.flowstage_data = flowstage_data
#         print(flowstage_data)
# =============================================================================
        


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
        
# =============================================================================
#         Transport_data = {(d,p) : value(Transport) for (d, p), Transport in model.Transport.items()}
#         Transport_data = pd.DataFrame.from_dict(Transport_data, orient="index", columns=["variable value"])
#         Transport_data = Transport_data.values.reshape(len(self.d),len(self.p)).transpose()
#         Transport_data = pd.DataFrame(Transport_data)
#         Transport_data.index = self.p
#         Transport_data.index.name = 'p'
#         Transport_data.columns = self.d
#         Transport_data.columns.name = 'd'
#         self.Transport_data = Transport_data    
#         #print(Transport_data.to_string())
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
        
# =============================================================================
#         TransportCost_data = {(d,p) : value(TransportCost) for (d, p), TransportCost in model.TransportCost.items()}
#         TransportCost_data = pd.DataFrame.from_dict(TransportCost_data, orient="index", columns=["variable value"])
#         TransportCost_data = TransportCost_data.values.reshape(len(self.d),len(self.p)).transpose()
#         TransportCost_data = pd.DataFrame(TransportCost_data)
#         TransportCost_data.index = self.p
#         TransportCost_data.index.name = 'p'
#         TransportCost_data.columns = self.d
#         TransportCost_data.columns.name = 'd'
#         self.TransportCost_data = TransportCost_data    
#         print(TransportCost_data.to_string())
# =============================================================================
        
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
        #print(EQCost_data)
        
        InTrans12_data = {(d,k) : value(InTransMS12) for (d, k), InTransMS12 in model.InTransMS12.items()}
        InTrans12_data = pd.DataFrame.from_dict(InTrans12_data, orient="index", columns=["variable value"])
        InTrans12_data = InTrans12_data.values.reshape(len(self.d),len(self.k)).transpose()
        InTrans12_data = pd.DataFrame(InTrans12_data)
        InTrans12_data.index = self.k
        InTrans12_data.index.name = 'k'
        InTrans12_data.columns = self.d
        InTrans12_data.columns.name = 'd'
        self.InTrans12_data = InTrans12_data    
        #print(InTrans12_data.to_string())
        
        InTrans13_data = {(k) : value(InTransMS13) for k, InTransMS13 in model.InTransMS13.items()}
        InTrans13_data = pd.DataFrame.from_dict(InTrans13_data, orient="index", columns=["variable value"])
        InTrans13_data = InTrans13_data.values.reshape(len(self.k)).transpose()
        InTrans13_data = pd.DataFrame(InTrans13_data)
        InTrans13_data.index = self.k
        InTrans13_data.index.name = 'k'
        self.InTrans13_data = InTrans13_data
        #print(InTrans13_data)
        print()
        
        IntTransMS14_data = {(k) : value(InTransMS14) for k, InTransMS14 in model.InTransMS14.items()}
        IntTransMS14_data = pd.DataFrame.from_dict(IntTransMS14_data, orient="index", columns=["variable value"])
        IntTransMS14_data = IntTransMS14_data.values.reshape(len(self.k)).transpose()
        IntTransMS14_data = pd.DataFrame(IntTransMS14_data)
        IntTransMS14_data.index = self.k
        IntTransMS14_data.index.name = 'k'
        self.IntTransMS14_data = IntTransMS14_data
        #print(IntTransMS14_data)
        #print()
        
        InTrans22_data = {(d,k) : value(InTransMS22) for (d, k), InTransMS22 in model.InTransMS22.items()}
        InTrans22_data = pd.DataFrame.from_dict(InTrans22_data, orient="index", columns=["variable value"])
        InTrans22_data = InTrans22_data.values.reshape(len(self.d),len(self.k)).transpose()
        InTrans22_data = pd.DataFrame(InTrans22_data)
        InTrans22_data.index = self.k
        InTrans22_data.index.name = 'k'
        InTrans22_data.columns = self.d
        InTrans22_data.columns.name = 'd'
        self.InTrans22_data = InTrans22_data    
        #print(InTrans22_data.to_string())
        
        InTransMS23_data = {(k) : value(InTransMS23) for k, InTransMS23 in model.InTransMS23.items()}
        InTransMS23_data = pd.DataFrame.from_dict(InTransMS23_data, orient="index", columns=["variable value"])
        InTransMS23_data = InTransMS23_data.values.reshape(len(self.k)).transpose()
        InTransMS23_data = pd.DataFrame(InTransMS23_data)
        InTransMS23_data.index = self.k
        InTransMS23_data.index.name = 'k'
        self.InTransMS23_data = InTransMS23_data
        #print(InTransMS23_data)
        print()
        
        IntTransMS24_data = {(k) : value(InTransMS24) for k, InTransMS24 in model.InTransMS24.items()}
        IntTransMS24_data = pd.DataFrame.from_dict(IntTransMS24_data, orient="index", columns=["variable value"])
        IntTransMS24_data = IntTransMS24_data.values.reshape(len(self.k)).transpose()
        IntTransMS24_data = pd.DataFrame(IntTransMS24_data)
        IntTransMS24_data.index = self.k
        IntTransMS24_data.index.name = 'k'
        self.IntTransMS24_data = IntTransMS24_data
        #print(IntTransMS24_data)
        
        ProductTransMS1_data = {(k, d, p): value(ProductTransMS1) for (k, d, p), ProductTransMS1 in model.ProductTransMS1.items()}
        ProductTransMS1_data = pd.DataFrame.from_dict(ProductTransMS1_data, orient="index", columns=["variable value"])
        ProductTransMS1_data = ProductTransMS1_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTransMS1_data = pd.DataFrame(ProductTransMS1_data)
        ProductTransMS1_data.index = self.p
        ProductTransMS1_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTransMS1_data.columns = columns
        ProductTransMS1_data.columns.names = ['k','d']
        self.ProductTransMS1_data = ProductTransMS1_data
        #print(ProductTransMS1_data.to_string())
        print()
        
        ProductTransMS2_data = {(k, d, p): value(ProductTransMS2) for (k, d, p), ProductTransMS2 in model.ProductTransMS2.items()}
        ProductTransMS2_data = pd.DataFrame.from_dict(ProductTransMS2_data, orient="index", columns=["variable value"])
        ProductTransMS2_data = ProductTransMS2_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
        ProductTransMS2_data = pd.DataFrame(ProductTransMS2_data)
        ProductTransMS2_data.index = self.p
        ProductTransMS2_data.index.name = 'p'
        columns = pd.MultiIndex.from_product([self.k,self.d])
        ProductTransMS2_data.columns = columns
        ProductTransMS2_data.columns.names = ['k','d']
        self.ProductTransMS2_data = ProductTransMS2_data
        #print(ProductTransMS2_data.to_string())
        print()
        
# =============================================================================
#         ProductTrans_data = {(k, d, p): value(ProductTrans) for (k, d, p), ProductTrans in model.ProductTrans.items()}
#         ProductTrans_data = pd.DataFrame.from_dict(ProductTrans_data, orient="index", columns=["variable value"])
#         ProductTrans_data = ProductTrans_data.values.reshape(len(self.k)*len(self.d),len(self.p)).transpose()
#         ProductTrans_data = pd.DataFrame(ProductTrans_data)
#         ProductTrans_data.index = self.p
#         ProductTrans_data.index.name = 'p'
#         columns = pd.MultiIndex.from_product([self.k,self.d])
#         ProductTrans_data.columns = columns
#         ProductTrans_data.columns.names = ['k','d']
#         self.ProductTrans_data = ProductTrans_data
#         print(ProductTrans_data.to_string())
# =============================================================================
        
        Results_data = {(k) : value(Results) for k, Results in model.Results.items()}
        Results_data = pd.DataFrame.from_dict(Results_data, orient="index", columns=["variable value"])
        Results_data = Results_data.values.reshape(len(self.k)).transpose()
        Results_data = pd.DataFrame(Results_data)
        Results_data.index = self.k
        Results_data.index.name = 'k'
        self.Results_data = Results_data
        
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
        
       
        Lambda1_data = {(u) : value(x1) for u, x1 in model.x1.items()}
        Lambda1_data = pd.DataFrame.from_dict(Lambda1_data, orient="index", columns=["variable value"])
        Lambda1_data = Lambda1_data.values.reshape(len(self.u)).transpose()
        Lambda1_data = pd.DataFrame(Lambda1_data)
        Lambda1_data.index = self.u
        Lambda1_data.index.name = 'u'
        self.Lambda1_data = Lambda1_data
        print(Lambda1_data)
        
        Lambda2_data = {(u) : value(x2) for u, x2 in model.x2.items()}
        Lambda2_data = pd.DataFrame.from_dict(Lambda2_data, orient="index", columns=["variable value"])
        Lambda2_data = Lambda2_data.values.reshape(len(self.u)).transpose()
        Lambda2_data = pd.DataFrame(Lambda2_data)
        Lambda2_data.index = self.u
        Lambda2_data.index.name = 'u'
        self.Lambda2_data = Lambda2_data
        print(Lambda2_data)
# =============================================================================
#         Lambda_data = {(u,L) : value(x) for (u, L), x in model.x.items()}
#         Lambda_data = pd.DataFrame.from_dict(Lambda_data, orient="index", columns=["variable value"])
#         Lambda_data = Lambda_data.values.reshape(len(self.u),len(self.L)).transpose()
#         Lambda_data = pd.DataFrame(Lambda_data)
#         Lambda_data.index = self.L
#         Lambda_data.index.name = 'L'
#         Lambda_data.columns = self.u
#         Lambda_data.columns.name = 'u'
#         self.Lambda_data = Lambda_data
#         print(Lambda_data)
# =============================================================================
        
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
        #print()
        #print(Flow1_data.to_string())
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
        
        
        
    
       