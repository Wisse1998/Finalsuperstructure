# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:37:16 2022

@author: Gebruiker
"""


from pyomo.environ import *



def Superstructure_model(Superstructure):
    model = ConcreteModel()
    
    model.j = Set(initialize = Superstructure.j, doc = 'process stages')
    model.k = Set(initialize = Superstructure.k, doc = 'Technology options')
    model.i = Set(initialize = Superstructure.i, doc = 'Species in reaction mixture')
    model.a = Set(initialize = Superstructure.a, doc = 'range')
    model.u = Set(initialize = Superstructure.u, doc = 'Utility')
    model.s = Set(initialize = Superstructure.s, doc = 'Supply')
    model.d = Set(initialize = Superstructure.d, doc = 'Demand')
    model.p = Set(initialize = Superstructure.p, doc = 'Products')
    model.g = [1,2,3,4,5,6,7,8,9,10]    
    
    model.SF = Param(model.j, model.k, model.i, initialize = Superstructure.SF_data, doc = 'Split factor data for equipment types')
    model.EC = Param(model.j, model.k, initialize = Superstructure.EC_data, doc = 'Cost data for process types')
    model.flow0   = Param(model.i, initialize = Superstructure.F0_data, doc = 'Flow coming in process')
    model.RatiomR = Param(model.j, model.k, model.i, initialize = Superstructure.RatiomR_data, doc = 'Ratio to glycerol(j-1) to secondary stream')
    model.CF = Param(model.j, model.k, model.i, initialize = Superstructure.CF_data, doc = 'Conversion glycerol')
    model.SEL     = Param(model.j, model.k, model.i, initialize = Superstructure.SEL_data, doc = 'Selectivity towards glycerol')
    model.MW      = Param(model.i, initialize = Superstructure.MW_data, doc = 'Molar weight component i')
    model.ALPHA   = Param(model.i, initialize = Superstructure.ALPHA_data, doc = 'Stochiometry component i towards glycerol')
    model.Marketdist = Param(model.d, model.k, initialize = Superstructure.Marketdis_data, doc = 'Distances markets')
    
    model.LB   = Param(model.a , initialize = Superstructure.LB_data, doc = 'Lower bound eqpuipment cost')
    model.Slope   = Param(model.j, model.k, model.a, initialize = Superstructure.Slope_data, doc = 'slope value eqpuipment cost')
    model.Constant   = Param(model.j, model.k, model.a , initialize = Superstructure.constant_data, doc = 'Constant value eqpuipment cost')
    model.UB   = Param(model.a , initialize = Superstructure.UB_data, doc = 'Upper bound eqpuipment cost')  
    
    model.Tau = Param(model.j, model.k, model.u, initialize=Superstructure.Tau_data)
    model.Uprice = Param(model.u, initialize=Superstructure.Uprice_data)
    
    model.CCost = Param(model.i, initialize=Superstructure.CCost_data)
    
    model.SupplyLoad = Param(model.s, initialize= Superstructure.SupplyLoad_data)
    model.Distance = Param(model.j, model.k, model.s, initialize= Superstructure.Distance_data)
    model.Demand = Param(model.d, model.p, initialize= Superstructure.Demand_data)
    
    
    #model.M = Param(initialize = 1e7)
    model.M = Param(initialize = 1e7)
    model.N = Param(initialize = 1e9)
    model.TGpurity = Param(initialize = 0.95, doc = 'Weight fraction m/m %')
    model.CGpurity = Param(initialize = 0.6)
    model.WGpurity = Param(initialize = 0.2)
    model.WGprice = Param(initialize = -0.02)
    model.TGprice = Param(initialize = 0.9, doc = 'dollar/kg')
    model.CGprice = Param(initialize = 0.17)
    model.PGprice = Param(initialize = 1.28)
    model.Feedflow = Param(initialize = 115289.286, doc = ' Total feed flow fixed value kg/hr (sum of supply load')
    #model.Feedflow = Param(initialize = 57644.64, doc = ' 50% of Total feed flow fixed value kg/hr (sum of supply load')
    model.H = Param(initialize=(8400), doc = 'Yearly operating hours')
    model.TankLoad = Param(initialize = 25, doc = 'Average lorry load capacity in tonnes')
    model.FuelCon = Param(initialize = 0.38 , doc = 'Lorry fuel (diesel) consumption per L/km average load 25 tonnes')
    model.FuelPrice = Param(initialize = 2.071, doc = 'Diesel price in the netherlands')
    model.IR = Param(initialize = 0.1, doc = 'Interest rate')
    model.LS = Param(initialize = 20, doc = 'Life span')
    
    "MASS BALANANCE VARIABLES"
    model.flow = Var(model.j, model.k, model.i, bounds = (0.0,None), doc = 'Flow at every equipment for every component')
    model.y = Var(model.j, model.k, domain = Binary, doc = 'Logic variable')
    model.x = Var(model.u, bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.TECTEST = Var(bounds = (0.0, None), doc = 'Total equipment cost')
    model.BDP = Var(bounds = (0.0, None), doc = 'Biodiesel production')
    model.flowtot = Var(model.j, model.k,  bounds = (0.0, None))
    model.flowstage = Var(model.j, model.i, bounds = (0.0, None))
    model.Waste = Var(model.j, model.k, model.i, bounds=(0.0,None))
    model.Wastestage = Var(model.j, model.i, bounds=(0.0, None))
    model.flowstage3 = Var(bounds = (0.0, None))
    
    "COST VARIABLES"
    model.EQCost = Var(model.j, model.k, bounds=(0.0,None), doc = 'Equipment cost')
    model.TEC = Var(model.j, bounds=(0.0, None), doc = 'Equipment cost')
    model.TECd = Var(model.j, bounds=(0.0, None), doc = 'Purchased and delivered equipment cost')
    model.RMC = Var(bounds=(0.0, None))
    model.SECCost = Var(model.j, model.k, model.i, bounds=(0.0, None), doc = 'Cost make up stream')
    model.TotSECCost = Var(model.j, model.k, model.i, bounds=(0.0, None))

        
    "Utilities VARIABLES"
    model.Util = Var(model.j, model.k, model.u, bounds=(0.0, None))
    model.TUC = Var(bounds=(0.0, None))
    
    'Total direct plant cost'
    model.PEI = Var(model.j, bounds=(0.0, None), doc = 'Purchased and installation cost')
    model.IC = Var(model.j, bounds=(0.0, None), doc = 'Instrumentation and controls (installed) cost')
    model.Pi = Var(model.j, bounds=(0.0, None), doc = 'Piping cost')
    model.ESi = Var(model.j, bounds=(0.0, None), doc = 'Electrical system (installed) cost')
    model.Build = Var(model.j, bounds=(0.0, None), doc = 'Buildings (including services) cost')
    model.Yi = Var(model.j, bounds=(0.0, None), doc = 'Yard improvements cost')
    model.Sfi = Var(model.j, bounds=(0.0, None), doc = 'Service facilities (installed) cost')
    model.TDC = Var(model.j, bounds=(0.0, None), doc = 'Total direct plant cost')
    model.TotalTDC = Var(bounds=(0.0, None))
    
    'Total indirect plant cost'
    model.ES = Var(model.j, bounds=(0.0, None), doc = 'Engineering and supervision cost')
    model.CONexp = Var(model.j, bounds=(0.0, None), doc = 'Construction expenses')
    model.LE = Var(model.j, bounds=(0.0, None), doc = 'Legal espenses')
    model.Cfee = Var(model.j, bounds=(0.0, None), doc = 'Contractor fee')
    model.CG = Var(model.j, bounds=(0.0, None), doc = 'Contingency cost')
    model.TIC = Var(model.j, bounds=(0.0, None), doc = 'Total indirect plant cost')
    model.TotalTIC = Var(bounds=(0.0, None))
    model.TotalSupply = Var(bounds=(0.0, None))
    
    'Transportation cost'
    model.TrCost = Var(model.j, model.k, model.s, bounds=(0.0, None)) 
    model.TotTrCost = Var(bounds=(0.0, None))
    model.Transport = Var(model.d, model.p, bounds=(0.0, None))
    model.TransportCost = Var(model.d, model.p, bounds=(0.0, None))
    model.TotTransportCost  = Var(bounds=(0.0, None))
    model.IntTrans = Var(model.k, bounds=(0.0, None))
    model.TotInTrans = Var(bounds=(0.0, None))
    model.ProductTrans = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.TotProductTrans = Var(bounds=(0.0, None))
    model.IntDist = Var( model.d, model.k, bounds=(0.0, None))
    model.TotIntDist = Var(model.d, bounds=(0.0, None))
    
    "TEST INTERMEDIATE"
    model.InTrans11 = Var(model.d, model.k, bounds=(0.0, None))
    model.InTrans22 = Var(model.d, model.k, bounds=(0.0, None))
    model.InTrans33 = Var(model.k, bounds=(0.0, None))
    model.InTrans44 = Var(bounds=(0.0, None))
    model.InTrans222 = Var(model.k,  bounds=(0.0, None))
    
    
    'flow Validation variables'
    model.TESTin =  Var(model.j, model.i, bounds=(0.0, None))
    model.TESTout = Var(model.j, model.i, bounds=(0.0, None))
    
    
    'Profit'
    model.Profit = Var(model.j, model.k, model.i, bounds=(0.0, None))
    model.TotProfit = Var(bounds=(0.0, None))
    model.TarProd = Var(model.p, bounds=(0.0, None))
    
    
    'Cost SUM'
    model.FCI = Var(bounds=(0.0, None), doc = 'Fixed-capital investement')
    model.AIC = Var(bounds=(0.0, None), doc = 'Annualized investment cost')
    model.TAR = Var(bounds=(0.0, None), doc = 'Total annualized revenue')
    model.AOC = Var(bounds=(0.0, None), doc = 'Total annualized revenue')
    model.OMC = Var(bounds=(0.0, None), doc = 'Operating management cost')
    model.OBJ = Var(bounds=(0.0, None), doc = 'OBJ variable')
    model.IRCalc = Var(bounds=(0.0, None), doc = 'interest rate calculation')
    model.Results = Var(model.k, bounds=(0.0, None), doc = 'RMC TAR AOC AIC UTC TotTrCost')
    
    
    'MASS BALANCE FUNCTIONS (PROCESS FLOW AND WASTE STREAM------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    """3 massbalance rules for big M implementation:
            It calculates flow[j,k,i] = flow at previous stage * Separation factor * logic_variable
            This equation is an MINLP so it is converted using the big M notation for performance"""
            
    def massbalance_rule1(model, j, k, i):
        if j >= 3:
            #return model.flow[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) ) * model.SF[j,k,i] + model.M * (1-model.y[j,k])
            return model.flow[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] + model.M * (1-model.y[j,k])
            #return model.flow[j,k,i] <= (model.flowstage[j-1,i]  + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] + model.M * (1-model.y[j,k])
        else:
            return model.flow[j,k,i] == model.Feedflow * model.y[j,k] * model.RatiomR[j,k,i]
        
    def massbalance_rule2(model, j, k, i):
        if j >= 3:
            #return model.flow[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] ) * model.SF[j,k,i] - model.M * (1-model.y[j,k])
            return model.flow[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] - model.M * (1-model.y[j,k])
            #return model.flow[j,k,i] >= (model.flowstage[j-1,i] + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] - model.M * (1-model.y[j,k])
        else:
            return Constraint.Skip
    
    def massbalance_rule3(model, j, k, i):
        if j >= 3:
            return model.flow[j,k,i] <= model.M * model.y[j,k]
        else:
            return Constraint.Skip
        
    def waste_rule1(model, j, k, i):
        if 3<=j<=4:
            #return model.flow[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) ) * (1-model.SF[j,k,i]) + model.M * (1-model.y[j,k])
            return model.Waste[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * (1-model.SF[j,k,i]) + model.M * (1-model.y[j,k])
        else:
            return model.Waste[j,k,i] == 0
    
    def waste_rule2(model, j, k, i):
        if 3<=j<=4:
            #return model.Waste[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] ) * (1-model.SF[j,k,i]) - model.M * (1-model.y[j,k])
            return model.Waste[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * (1-model.SF[j,k,i]) - model.M * (1-model.y[j,k])
        else:
            return Constraint.Skip
    
    def waste_rule3(model, j, k, i):
        if 3<=j<=4:
            return model.Waste[j,k,i] <= model.M * model.y[j,k]
        else:
            return Constraint.Skip
        
    model.massrule1 = Constraint(model.j, model.k, model.i, rule = massbalance_rule1)
    model.massrule2 = Constraint(model.j, model.k, model.i, rule = massbalance_rule2)
    model.massrule3 = Constraint(model.j, model.k, model.i, rule = massbalance_rule3)
    model.waste_rule1 = Constraint(model.j, model.k, model.i, rule = waste_rule1)
    model.waste_rule2 = Constraint(model.j, model.k, model.i, rule = waste_rule2)
    model.waste_rule3 = Constraint(model.j, model.k, model.i, rule = waste_rule3)
    
    def flowstage_rule(model, j, i):
        return model.flowstage[j,i] == sum(model.flow[j,k,i] for k in model.k)
    
    def Wastestage_rule(model, j, i):
        return model.flowstage[j,i] == sum(model.flow[j,k,i] for k in model.k)
    
    def flowtot_rule(model, j,k):
        return model.flowtot[j,k] == sum(model.flow[j,k,i] for i in model.i) 
    
    model.flowstage_rule = Constraint(model.j, model.i, rule = flowstage_rule)
    model.Wastestage_rule = Constraint(model.j, model.i, rule = Wastestage_rule)
    model.flowtot_rule = Constraint(model.j, model.k, rule = flowtot_rule)

 
    'Flow Validation functions-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    def TESTin_rule(model, j, i):
        if 3<=j<=4:
            return model.TESTin[j,i] == sum(model.flow[j-1,k,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) for k in model.k)
        else:
            return model.TESTin[j,i] == 0
    
    
    def TESTout_rule(model, j, i):
        if 3<=j<=4:
            return model.TESTout[j,i] == sum(model.flow[j,k,i] + model.Waste[j,k,i] for k in model.k)
        else:
            return model.TESTout[j,i] == 0
        
    model.TESTin_rule = Constraint(model.j, model.i, rule = TESTin_rule)
    model.TESTout_rule = Constraint(model.j, model.i, rule = TESTout_rule)
   
    
    'Logic constraint equations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    def logic_rule(model, j):
        if j<=4 or j == 7:
            return sum(model.y[j,k] for k in model.k) == 1
        else:
            return Constraint.Skip
    
    model.logic = Constraint(model.j, rule = logic_rule, doc = 'One option per stage') 
    
    
    def logic_rule1(model):
       return model.y[1,1] + model.y[1,2] + model.y[1,3] + model.y[1,4] + model.y[1,5] + model.y[1,6] + model.y[1,7] + model.y[1,8] - model.y[2,1] - model.y[2,2] - model.y[2,3] == 0
    
    def logic_rule2(model):
       return model.y[2,1] + model.y[2,2] - model.y[3,1] - model.y[3,2] - model.y[3,3] == 0
   
    def logic_rule3(model):
       return model.y[2,3] - model.y[3,4] == 0
   
    def logic_rule4(model):
       return model.y[3,1] - model.y[4,1]  == 0
   
    def logic_rule5(model):
       return model.y[3,2]+ model.y[3,3] + model.y[3,4] - model.y[4,2]  - model.y[4,3] - model.y[4,4] == 0

    def logic_rule6(model):
       return 3*model.y[4,1] - model.y[5,1] - model.y[5,2] - model.y[5,3]  == 0
    
    def logic_rule7(model):
       return 2*model.y[4,2] - model.y[5,4] - model.y[5,5]  == 0

    def logic_rule8(model):
       return 2*model.y[4,3] - model.y[5,6] - model.y[5,7]  == 0

    def logic_rule9(model):
       return 2*model.y[4,4] - model.y[5,8] - model.y[5,9]  == 0

    def logic_rule20(model):
       return model.y[1,6] + model.y[2,2] + model.y[7,6] - 3  == 0
   
    def logic_rule21(model):
        return model.y[4,2] - 1 == 0
    
    def logic_rule31(model):
        return model.y[1,1] + model.y[7,1] <= 1
    
    def logic_rule38(model):
        return model.y[1,2] + model.y[7,2] <= 1
    
    def logic_rule32(model):
        return model.y[1,3] + model.y[7,3] <= 1
    
    def logic_rule33(model):
        return model.y[1,4] + model.y[7,4] <= 1
    
    def logic_rule34(model):
        return model.y[1,5] + model.y[7,5] <= 1
    
    def logic_rule35(model):
        return model.y[1,6] + model.y[7,6] <= 1
    
    def logic_rule36(model):
        return model.y[1,7] + model.y[7,7] <= 1
    
    def logic_rule37(model):
        return model.y[1,8] + model.y[7,8] <= 1
   
    model.logic1 = Constraint(rule = logic_rule1)
    model.logic2 = Constraint(rule = logic_rule2)
    model.logic3 = Constraint(rule = logic_rule3)
    model.logic4 = Constraint(rule = logic_rule4)
    model.logic5 = Constraint(rule = logic_rule5)
    model.logic6 = Constraint(rule = logic_rule6)
    model.logic7 = Constraint(rule = logic_rule7)
    model.logic8 = Constraint(rule = logic_rule8)
    model.logic9 = Constraint(rule = logic_rule9)
    model.logic20 = Constraint(rule = logic_rule20)
    #model.logic21 = Constraint(rule = logic_rule21)
# =============================================================================
#     model.logic31 = Constraint(rule = logic_rule31)
#     model.logic32 = Constraint(rule = logic_rule32)
#     model.logic33 = Constraint(rule = logic_rule33)
#     model.logic34 = Constraint(rule = logic_rule34)
#     model.logic35 = Constraint(rule = logic_rule35)
#     model.logic36 = Constraint(rule = logic_rule36)
#     model.logic37 = Constraint(rule = logic_rule37)
#     model.logic38 = Constraint(rule = logic_rule38)
# =============================================================================

 
    "Transportation constraints------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    def Transport_rule1(model, p, j):
        if p==1:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,7] * 8400 / 1000000
        if p==2:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,2] * 8400 / 1000000
        if p==3:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,1] * 8400 / 1000000
        if p==4:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,8] * 8400 / 1000000
        if p==5:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,11] * 8400 / 1000000
        if p==6:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,9] * 8400 / 1000000
        if p==7:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,19] * 8400 / 1000000
        if p==8:
            return sum(model.Transport[d,p] for d in model.d) <= model.flowstage[5,10] * 8400 / 1000000
        if p==9:
            return sum(model.Transport[d,p] for d in model.d) == 0
        else:
            return Constraint.Skip
    
    def Transport_rule2(model,d,p):
        return model.Transport[d,p] <= model.Demand[d,p]
        
    def Transport_rule3(model):
            return model.TotTransportCost == model.TotProductTrans + model.InTrans44
            #return model.TotTransportCost == model.TotInTrans + model.TotProductTrans + model.InTrans44
    
    model.Transport_rule1 = Constraint(model.p, model.j , rule = Transport_rule1)
    model.Transport_rule2 = Constraint(model.d, model.p , rule = Transport_rule2)
    model.Transport_rule3 = Constraint(rule = Transport_rule3)


    'Transportation Cost of supply load glycerol feedstock to purifcation station------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    def Transport_rule(model, j, k, s):
        if j==1:
            return model.TrCost[j,k,s] == 2 * model.Distance[j,k,s] * model.FuelCon * model.FuelPrice * (model.SupplyLoad[s] / model.TankLoad) * model.y[j,k]
        else:
            return model.TrCost[j,k,s] == 0
    
    model.Transport_rule = Constraint(model.j, model.k, model.s, rule = Transport_rule)  


    def TotTransport_rule(model):
        return model.TotTrCost == sum(model.TrCost[j,k,s] for j in model.j for k in model.k for s in model.s)
    
    model.TotTransport_rule = Constraint(rule = TotTransport_rule)


    "'Transportation Cost of intermediate purfied glycerol and product to markets------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
    
    
    
    def Int_transport11(model, k, d):
        return model.InTrans11[d,k] == (sum(model.flowstage[3,i] for i in model.i) * model.H / 1000) / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice
        
    def Int_transport22(model, j, k, d):
        if j == 1:
            if k == 9:
                return model.InTrans22[d,k] <=  model.N
            else:    
                return model.InTrans22[d,k] <= model.InTrans11[d,k] + model.N * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport222(model, j, k, d):
        if j == 1:
            if k == 9:
                return Constraint.Skip
            else:
                return model.InTrans22[d,k] >= model.InTrans11[d,k] - model.N * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport2222(model, j, k, d):
        if k == 1:
            return model.InTrans222[k] == sum(model.InTrans22[1,k] for k in model.k)
        if k == 2:
            return model.InTrans222[k] == sum(model.InTrans22[2,k] for k in model.k)
        if k == 3:
            return model.InTrans222[k] == sum(model.InTrans22[3,k] for k in model.k)
        if k == 4:
            return model.InTrans222[k] == sum(model.InTrans22[4,k] for k in model.k)
        if k == 5:
            return model.InTrans222[k] == sum(model.InTrans22[5,k] for k in model.k)
        if k == 6:
            return model.InTrans222[k] == sum(model.InTrans22[6,k] for k in model.k)
        if k == 7:
            return model.InTrans222[k] == sum(model.InTrans22[7,k] for k in model.k)
        if k == 8:
            return model.InTrans222[k] == sum(model.InTrans22[8,k] for k in model.k)
        if k == 9: 
            return model.InTrans222[k] == 10e7

        
    def Int_transport33(model, j, k, d):
        if j == 7:
            if k == 1:
                return model.InTrans33[k] <= model.InTrans222[1] + model.N * (1-model.y[j,k])
            if k == 2:
                return model.InTrans33[k] <= model.InTrans222[2] + model.N * (1-model.y[j,k])
            if k == 3:
                return model.InTrans33[k] <= model.InTrans222[3] + model.N * (1-model.y[j,k])
            if k == 4:
                return model.InTrans33[k] <= model.InTrans222[4] + model.N * (1-model.y[j,k])
            if k == 5:
                return model.InTrans33[k] <= model.InTrans222[5] + model.N * (1-model.y[j,k])
            if k == 6:
                return model.InTrans33[k] <= model.InTrans222[6] + model.N * (1-model.y[j,k])
            if k == 7:
                return model.InTrans33[k] <= model.InTrans222[7] + model.N * (1-model.y[j,k])
            if k == 8:
                return model.InTrans33[k] <= model.InTrans222[8] + model.N * (1-model.y[j,k])
            if k == 9:
                return model.InTrans33[k] == model.N * (model.y[j,k])   
        else:
            return Constraint.Skip
        
    def Int_transport333(model, j, k, d):
        if j == 7:
            if k == 1:
                return model.InTrans33[k] >= model.InTrans222[1] - model.N * (1-model.y[j,k])
            if k == 2:
                return model.InTrans33[k] >= model.InTrans222[2] - model.N * (1-model.y[j,k])
            if k == 3:
                return model.InTrans33[k] >= model.InTrans222[3] - model.N * (1-model.y[j,k])
            if k == 4:
                return model.InTrans33[k] >= model.InTrans222[4] - model.N * (1-model.y[j,k])
            if k == 5:
                return model.InTrans33[k] >= model.InTrans222[5] - model.N * (1-model.y[j,k])
            if k == 6:
                return model.InTrans33[k] >= model.InTrans222[6] - model.N * (1-model.y[j,k])
            if k == 7:
                return model.InTrans33[k] >= model.InTrans222[7] - model.N * (1-model.y[j,k])
            if k == 8:
                return model.InTrans33[k] >= model.InTrans222[8] - model.N * (1-model.y[j,k])
            if k == 9:
                return Constraint.Skip   
        else:
            return Constraint.Skip
        
        
    def Int_transport44(model):
        return model.InTrans44 == sum(model.InTrans33[k] for k in model.k)
            
        
        
    model.IntermediateTrans11 = Constraint(model.k, model.d, rule = Int_transport11 )
    model.IntermediateTrans22 = Constraint(model.j, model.k, model.d, rule = Int_transport22 )
    model.IntermediateTrans222 = Constraint(model.j, model.k, model.d, rule = Int_transport222 )
    model.IntermediateTrans2222 = Constraint(model.j, model.k, model.d, rule = Int_transport2222 )
    model.IntermediateTrans33 = Constraint(model.j, model.k, model.d, rule = Int_transport33 )
    model.IntermediateTrans333 = Constraint(model.j, model.k, model.d, rule = Int_transport333 )
    model.IntermediateTrans44 = Constraint(rule = Int_transport44 )

    

    def Prod_transport(model, j, k, d, p):
        if j == 7:
            return model.ProductTrans[k,d,p] <=  model.Transport[d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice + 10e9 * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Prod_transport1(model, j, k, d, p):
        if j == 7:
            return model.ProductTrans[k,d,p] >=  model.Transport[d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice - 10e9 * (1-model.y[j,k])
        else:
            return Constraint.Skip

    model.ProdTrans = Constraint(model.j, model.k, model.d, model.p, rule = Prod_transport )
    model.ProdTrans1 = Constraint(model.j, model.k, model.d, model.p, rule = Prod_transport1 )


    def TotProd_transport(model):
        return model.TotProductTrans == sum(model.ProductTrans[k,d,p] for k in model.k for d in model.d for p in model.p)
    
    model.TotProdTrans = Constraint(rule = TotProd_transport)






    
    'Equipment Cost calcuations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'

    def EQ_rule1(model, j, k, i, a):
        """This part of the code deals with economy of scale. The exponential
            function is linearized over 3 different domains to approximate and keep the model
            as an MILP problem 
            This part of the code deals with economy of scale. The exponential
            function is linearized over 3 different domains to approximate and keep the model
            as an MILP problem. The total supplied feed is used for the economic of scale rule that is applied for
            the purification stage. Since python does not accept variables on both sides of the constraint, an assumption 
            is made regarding the ingoing flow of the conversion processes due to the different feedstock compositions.
            
            Example:
            For processing station 1 it is assumed that all the glycerol and methanol is purified therefore the sum of the composition values 
            of glycerol in WG and CG is calculated and used for the ingoing flow (0,77 + 0,8)/2 = 0,785. The total amount of added 
            components is based on the amount of glycerol entering the process. For this case the ratio of glycerol : water = 1 : 0,084
            considering the average amount of glycerol entering (0,3 + 0,6)/2 = 0.45
            
            The purfication processes before the conversion processes 2, 3, 4 do have a complete separation and purity of almost
            100% for both values. That's why the average glycerol composition is considered from all the three feed classifications.
            """
        
        if j==3 :
             if model.LB[a] <= model.Feedflow <= model.UB[a]:
                 return model.EQCost[j,k] == (model.Slope[j,k,a] * model.Feedflow + model.Constant[j,k,a]) * model.y[j,k] 
             else:
                 return Constraint.Skip
        if j==1 or j==2 or j==5 or j==6:
            return model.EQCost[j,k] == 0
        else:
            return Constraint.Skip
        
    def EQ_rule2(model, u):
        return sum(model.x[u] for u in model.u) == 1
        #return model.x[1] + (1 - model.x[1]) + model.x[2] + (1 - model.x[2]) + model.x[3] + (1 - model.x[3]) == 1
    
    def EQ_rule3(model, u, j ,i,k):
        if j==4:
            if k==1:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 <=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.084) + model.M * (1-model.y[j,k])
            if k==2:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 <=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.2185) + model.M * (1-model.y[j,k])
            if k==3:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 <=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 1.1765) + model.M * (1-model.y[j,k])
            if k==4:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 <=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.9781) + model.M * (1-model.y[j,k])
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
    
    def EQ_rule5(model, u, j ,i,k):
        if j==4:
            if k==1:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 >=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.084) - model.M * (1-model.y[j,k])
            if k==2:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 >=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.2185) - model.M * (1-model.y[j,k])
            if k==3:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 >=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 1.1765) - model.M * (1-model.y[j,k])
            if k==4:
                return model.x[1] * 0 + model.x[2] * 100000 + model.x[3] * 400000 + model.x[4] * 600000 >=  (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.9781) - model.M * (1-model.y[j,k])
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
    
    def EQ_rule4(model, j, k, u):
        if j == 4:
            if k == 1:
                #return model.EQCost[j,k] == model.x[1] * 0 + model.x[2] * 10912000 + model.x[3] * 30863000 + model.x[4] * 4.1831e+07
                #return model.EQCost[j,k] == model.x[1] * (0.1146e6 * (0/230) ** 0.75) + model.x[2] * (0.1146e6 * (100000/230) **0.75) + model.x[3] * (0.1146e6 * (400000/230) ** 0.75) + model.x[4] * (0.1146e6 * (600000/230) ** 0.75)
                return model.EQCost[j,k] <= (model.x[1] * (0.1146e6 * (0/230) ** (0.75)) + model.x[2] * (0.1146e6 * (100000/230) **(0.75)) + model.x[3] * (0.1146e6 * (400000/230) ** (0.75)) + model.x[4] * (0.1146e6 * (600000/230) ** (0.75)))  + model.N *(1-model.y[j,k])
            if k == 2:
                return model.EQCost[j,k] <= (model.x[1] * (1.5543e6 * (0/3296) ** (0.75)) + model.x[2] * (1.5543e6 * (100000/3296) **(0.75)) + model.x[3] * (1.5543e6 * (400000/3296) ** (0.75)) + model.x[4] * (1.5543e6 * (600000/3296) ** (0.75))) + model.N *(1-model.y[j,k])
            if k == 3:
                return model.EQCost[j,k] <= (model.x[1] * (1.3485e6 * (0/4600) ** (0.75)) + model.x[2] * (1.3485e6 * (100000/4600) **(0.75)) + model.x[3] * (1.3485e6 * (400000/4600) ** (0.75)) + model.x[4] * (1.3485e6 * (600000/4600) ** (0.75))) + model.N *(1-model.y[j,k])
            if k == 4:
                return model.EQCost[j,k] <= (model.x[1] * (4.8155e6 * (0/8500) ** (0.75)) + model.x[2] * (4.8155e6 * (100000/8500) **(0.75)) + model.x[3] * (4.8155e6 * (400000/8500) ** (0.75)) + model.x[4] * (4.8155e6 * (600000/8500) ** (0.75))) + model.N *(1-model.y[j,k])
            else:
                return model.EQCost[j,k] == 0
        else:
            return Constraint.Skip
        
    def EQ_rule44(model, j, k, u):
        if j == 4:
            if k == 1:
                #return model.EQCost[j,k] == model.x[1] * 0 + model.x[2] * 10912000 + model.x[3] * 30863000 + model.x[4] * 4.1831e+07
                #return model.EQCost[j,k] == model.x[1] * (0.1146e6 * (0/230) ** 0.75) + model.x[2] * (0.1146e6 * (100000/230) **0.75) + model.x[3] * (0.1146e6 * (400000/230) ** 0.75) + model.x[4] * (0.1146e6 * (600000/230) ** 0.75)
                return model.EQCost[j,k] >= (model.x[1] * (0.1146e6 * (0/230) ** (0.75)) + model.x[2] * (0.1146e6 * (100000/230) **(0.75)) + model.x[3] * (0.1146e6 * (400000/230) ** (0.75)) + model.x[4] * (0.1146e6 * (600000/230) ** (0.75)))  - model.N *(1-model.y[j,k])
            if k == 2:
                return model.EQCost[j,k] >= (model.x[1] * (1.5543e6 * (0/3296) ** (0.75)) + model.x[2] * (1.5543e6 * (100000/3296) **(0.75)) + model.x[3] * (1.5543e6 * (400000/3296) ** (0.75)) + model.x[4] * (1.5543e6 * (600000/3296) ** (0.75))) - model.N *(1-model.y[j,k])
            if k == 3:
                return model.EQCost[j,k] >= (model.x[1] * (1.3485e6 * (0/4600) ** (0.75)) + model.x[2] * (1.3485e6 * (100000/4600) **(0.75)) + model.x[3] * (1.3485e6 * (400000/4600) ** (0.75)) + model.x[4] * (1.3485e6 * (600000/4600) ** (0.75))) - model.N *(1-model.y[j,k])
            if k == 4:
                return model.EQCost[j,k] >= (model.x[1] * (4.8155e6 * (0/8500) ** (0.75)) + model.x[2] * (4.8155e6 * (100000/8500) **(0.75)) + model.x[3] * (4.8155e6 * (400000/8500) ** (0.75)) + model.x[4] * (4.8155e6 * (600000/8500) ** (0.75))) - model.N *(1-model.y[j,k])
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
        
    model.EQ1 = Constraint(model.j, model.k, model.i, model.a, rule = EQ_rule1)
    model.EQ2 = Constraint(model.u, rule = EQ_rule2)
    model.EQ3 = Constraint(model.u, model.j, model.i, model.k, rule = EQ_rule3)
    model.EQ5 = Constraint(model.u, model.j, model.i, model.k, rule = EQ_rule5)
    model.EQ4 = Constraint(model.j, model.k, model.u, rule = EQ_rule4)
    model.EQ44 = Constraint(model.j, model.k, model.u, rule = EQ_rule44)
    model.EQ6 = SOSConstraint(var=model.x, sos=2)
    
    
    "The factorial method of fixed capital investment calculations based on Equipment investment cost------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
   
    def TEC_rule(model, j):
        return model.TEC[j] == sum(model.EQCost[j,k] for k in model.k)
    
    def TECd_rule(model, j):
        return model.TECd[j] == model.TEC[j] * (1 + 0.1)
    
    def PEI_rule(model,j):
        return model.PEI[j] == model.TECd[j] * 0.47
    
    def IC_rule(model,j):
        return model.IC[j] == model.TECd[j] * 0.36
    
    def Pi_rule(model,j):
        return model.Pi[j] == model.TECd[j] * 0.68
    
    def ESi_rule(model,j):
        return model.ESi[j] == model.TECd[j] * 0.11
    
    def Build_rule(model,j):
        return model.Build[j] == model.TECd[j] * 0.18
    
    def Yi_rule(model,j):
        return model.Yi[j] == model.TECd[j] * 0.1
    
    def Sfi_rule(model,j):
        return model.Sfi[j] == model.TECd[j] * 0.7
    
    def TDC_rule(model,j):
        return model.TDC[j] == model.TECd[j] + model.PEI[j] + model.IC[j] + model.Pi[j] + model.ESi[j] + model.Build[j] + model.Yi[j] + model.Sfi[j] 

    def TotalTDC_rule(model):
        return model.TotalTDC == sum(model.TDC[j] for j in model.j)

    def ES_rule(model, j):
        return model.ES[j] == model.TECd[j] * 0.33
    
    def CONexp_rule(model, j):
        return model.CONexp[j] == model.CONexp[j] * 0.41
    
    def LE_rule(model,j):
        return model.LE[j] == model.TECd[j] * 0.04
    
    def Cfee_rule(model,j):
        return model.Cfee[j] == model.TECd[j] * 0.22
    
    def CG_rule(model,j):
        return model.CG[j] == model.TECd[j] * 0.44
    
    def TIC_rule(model,j):
        return model.TIC[j] == model.ES[j] + model.CONexp[j] + model.LE[j] + model.Cfee[j] + model.CG[j]

    def TotalTIC_rule(model):
        return model.TotalTIC == sum(model.TIC[j] for j in model.j)    


    model.TEC_rule = Constraint(model.j, rule = TEC_rule)
    model.TECd_rule = Constraint(model.j, rule = TECd_rule)
    model.PEI_rule = Constraint(model.j, rule = PEI_rule)
    model.IC_rule = Constraint(model.j, rule = IC_rule)
    model.Pi_rule = Constraint(model.j, rule = Pi_rule)
    model.ESi_rule = Constraint(model.j, rule = ESi_rule)
    model.Build_rule = Constraint(model.j, rule = Build_rule)
    model.Yi_rule = Constraint(model.j, rule = Yi_rule)
    model.Sfi_rule = Constraint(model.j, rule = Sfi_rule)
    model.TDC_rule = Constraint(model.j, rule = TDC_rule)
    model.TotalTDC_rule = Constraint(rule = TotalTDC_rule)
    model.ES_rule = Constraint(model.j, rule = ES_rule)
    model.CONexp_rule = Constraint(model.j, rule = CONexp_rule)
    model.LE_rule = Constraint(model.j, rule = LE_rule)
    model.Cfee_rule = Constraint(model.j, rule = Cfee_rule)
    model.TIC_rule = Constraint(model.j, rule = TIC_rule)
    model.TotalTIC_rule = Constraint(rule = TotalTIC_rule)
    
    
    "Make up stream cost------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
    """The make up stream is programmed in the same way as the 3 massbalances of the flow[j,k,i] calculations with the big M implementation:
            It calculates SECCost[j,k,i] = flow glycerol at previous stage * Ratio of secondary added component * price of comoponent i * logic_variable
            This equation is an MINLP so it is converted using the big M notation for performance"""
    def SECCost_rule1(model, j, k, i):
        if 3<=j<=4:
            return model.SECCost[j,k,i] <= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.CCost[i] + model.M * (1-model.y[j,k])
        else:
            return model.SECCost[j,k,i] == 0
        
    def SECCost_rule2(model, j, k, i):
        if 3<=j<=4:
            return model.SECCost[j,k,i] >= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.CCost[i] - model.M * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def SECCost_rule3(model, j, k, i):
        if 3<=j<=4:
            return model.SECCost[j,k,i] <= model.M * model.y[j,k]
        else:
            return Constraint.Skip
        
    def TotSECCost_rule(model, j,k,i):
        if i<= 20 or i == 25: 
            return model.TotSECCost[j,k,i] == model.SECCost[j,k,i] * model.H
        else:
            return model.TotSECCost[j,k,i] == model.SECCost[j,k,i]
        
        
    model.SECCost_rule1 = Constraint(model.j, model.k, model.i, rule = SECCost_rule1)
    model.SECCost_rule2 = Constraint(model.j, model.k, model.i, rule = SECCost_rule2)
    model.SECCost_rule3 = Constraint(model.j, model.k, model.i, rule = SECCost_rule3)
    model.TotSECCost_rule = Constraint(model.j, model.k, model.i, rule = TotSECCost_rule)
    
    
    
    
    "Raw material cost including the make up stream cost + solvent------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
    def RMC_rule(model):
        return model.RMC == model.H * (model.y[2,1] * model.Feedflow * model.WGprice + model.y[2,2] * model.Feedflow * model.CGprice + model.y[2,3] * model.Feedflow * model.TGprice) + sum(model.TotSECCost[j,k,i] for j in model.j for k in model.k for i in model.i)
    
    model.RMC_rule = Constraint(rule = RMC_rule)
    
    
    "Operating management cost------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
    def OMC_rule(model):
        return model.OMC == 0.02 * model.AIC
    
    model.OMC_rule = Constraint(rule = OMC_rule)
    
    
    "Utilities cost calcuations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'" 
    def Util_rule(model, j, k, u):
        if j == 3:
            if k == 2 or k == 3:
                return model.Util[j,k,u] <= ((model.Feedflow - model.flowstage[j-1,1]) * model.Tau[j,k,u] / 1000) + 10e5 * (1 - model.y[j,k])
            else:
                return model.Util[j,k,u] <= (model.Feedflow * model.Tau[j,k,u] / 1000 ) + 10e5 * (1 - model.y[j,k])
        if j == 4:
            return model.Util[j,k,u] <= (sum(model.flowstage[j-1,i] for i in model.i) * model.Tau[j,k,u] / 1000 )+ 10e5 * (1 - model.y[j,k])
        else:
            return model.Util[j,k,u] == 0
            
    def Util_rule1(model, j, k, u):
        if j == 3:
            if k == 2 or k == 3:
                return model.Util[j,k,u] >= ((model.Feedflow - model.flowstage[j-1,1]) * model.Tau[j,k,u] / 1000) - 10e5 * (1 - model.y[j,k])
            else:
                return model.Util[j,k,u] >= (model.Feedflow * model.Tau[j,k,u] / 1000 ) - model.M * (1 - model.y[j,k])
        if j == 4:
            return model.Util[j,k,u] >= (sum(model.flowstage[j-1,i] for i in model.i) * model.Tau[j,k,u] / 1000 )- 10e5 * (1 - model.y[j,k])
        else:
            return Constraint.Skip
    
    model.Util_rule = Constraint(model.j, model.k, model.u, rule = Util_rule)
    model.Util_rule1 = Constraint(model.j, model.k, model.u, rule = Util_rule1)
    
    
    def TUC_rule(model):
        return model.TUC == model.H * sum(model.Util[j,k,u] * model.Uprice[u] for j in model.j for k in model.k for u in model.u)
    
    model.TUC_rule = Constraint(rule = TUC_rule)
    
    
    
    
    
    "Profit calculation------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
    def TarProd_rule(model, p):
        if p == 1:
            return model.TarProd[p] == sum(model.Transport[d,1] for d in model.d) * 0.493 * 1000000
        if p == 2:
            return model.TarProd[p] == sum(model.Transport[d,2] for d in model.d) * 0.485 * 1000000
        if p == 3:
            return model.TarProd[p] == sum(model.Transport[d,3] for d in model.d) * 0.895 * 1000000
        if p == 4:
            return model.TarProd[p] == sum(model.Transport[d,4] for d in model.d) * 1.2 * 1000000
        if p == 5:
            return model.TarProd[p] == sum(model.Transport[d,5] for d in model.d) * 0.761*1000000
        if p == 6:
            return model.TarProd[p] == sum(model.Transport[d,6] for d in model.d) * 1.1 * 1000000
        if p == 7:
            return model.TarProd[p] == sum(model.Transport[d,7] for d in model.d) * 0.485 * 1000000 
        if p == 8:
            return model.TarProd[p] ==  sum(model.Transport[d,8] for d in model.d) * 1.1 * 1000000
        if p == 9:
            return model.TarProd[p] == 0
        else:
            return Constraint.Skip
      
    model.TarProd_rule = Constraint(model.p, rule = TarProd_rule)
    
    
    'AOC AIC Calculations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    def IRCalc_rule(model):
        return model.IRCalc == (model.IR * (model.IR + 1)**model.LS)/((model.IR + 1)**model.LS - 1)
    
    model.IRCalc_rule = Constraint(rule = IRCalc_rule)
    
    def TAR_rule(model):
        return model.TAR == sum(model.TarProd[p] for p in model.p)
    
    def AIC_rule(model):
        IRCalc = (model.IR * (model.IR + 1)**model.LS)/((model.IR + 1)** model.LS - 1)
        return model.AIC == (model.TotalTIC + model.TotalTDC)/ model.LS * IRCalc
        #return model.AIC == (model.TotalTIC + model.TotalTDC) / model.LS * model.IRCalc
    
    def AOC_rule(model):
        return model.AOC == model.RMC + model.TotTrCost + model.TUC + model.OMC + model.TotTransportCost
    
    model.TAR_rule = Constraint(rule = TAR_rule)
    model.AIC_rule = Constraint(rule = AIC_rule)
    model.AOC_rule = Constraint(rule = AOC_rule)    
    
    
    'RMC TAR AOC AIC UTC TotTrCost------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    def Results_rule(model, k):
        if k == 1:
            return model.Results[k] == model.AOC 
        elif k == 2:
            return model.Results[k] == model.AIC 
        elif k == 3:
            return model.Results[k] == model.TAR 
        elif k == 4:
            return model.Results[k] == model.RMC
        elif k == 5:
            return model.Results[k] == model.TUC 
        elif k == 6:
            return model.Results[k] == model.TotTrCost + model.TotTransportCost
        elif k == 7:
            return model.Results[k] == model.TotalTIC 
        elif k == 8:
            return model.Results[k] == model.TotalTDC 
        elif k == 9:
            return model.Results[k] == model.OMC
    
    model.Results_rule = Constraint( model.k, rule = Results_rule)
    
    
    'Objective Function------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    
    def OBJ_rule(model):
        #return model.OBJ ==  model.AIC + model.AOC - model.TAR
        return model.OBJ == model.TAR - model.AIC - model.AOC
        #return model.OBJ == sum(model.y[j,k] * model.EC[j,k] for k in model.k for j in model.j)\
        
    model.OBJ_rule = Constraint(rule = OBJ_rule)

   

# =============================================================================
#     def TECTEST_rule(model):
#         #return model.TEC == sum(model.EC[j,k] * model.flowtot[j,k] for j in model.j for k in model.k)
#         return model.TECTEST == sum(model.EC[j,k]*model.y[j,k] for j in model.j for k in model.k)
#     
#     model.TECTEST_rule = Constraint(rule = TECTEST_rule)
# =============================================================================
    
    
    
    
    def objective_rule(model):
        return model.OBJ
    
    model.objective = Objective(rule = objective_rule, sense = maximize)
    
    
    
    
    def pyomo_postprocess(options=None, instance=None, results=None):
      model.flow.display()
      model.y.display()
      model.flowtot.display()
    
    
    
    from pyomo.opt import SolverFactory
    import pyomo.environ
    #opt = SolverFactory("glpk")
    opt = SolverFactory("cplex")
    results = opt.solve(model, tee = True)
    #sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    #pyomo_postprocess(None, model, results)
    
# =============================================================================
#     from pyomo.opt import SolverFactory
#     import pyomo.environ
#     opt = SolverFactory("gurobi",solver_io="python")
#     opt.options['NonConvex'] = 2   
#     results = opt.solve(model, tee = True)
#     #sends results to stdout
#     results.write()
#     print("\nDisplaying Solution\n" + '-'*60)
# =============================================================================
    
    return model