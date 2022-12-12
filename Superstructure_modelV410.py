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
    model.L = [1,2,3,4,5,6,7]
    
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
    
    
    #model.M = Param(initialize = 1e8)
    model.G = Param(initialize = 1e9)
    model.K = Param(initialize = 1e9)
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
    model.FuelPrice = Param(initialize = 2.071 , doc = 'Diesel price in the netherlands')
    model.IR = Param(initialize = 0.1, doc = 'Interest rate')
    model.LS = Param(initialize = 20, doc = 'Life span')
    
    "MASS BALANANCE VARIABLES"
    model.flow = Var(model.j, model.k, model.i, bounds = (0.0,None), doc = 'Flow at every equipment for every component')
    model.y = Var(model.j, model.k, domain = Binary, doc = 'Logic variable')
    model.x = Var(model.u, model.L, bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x1 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x2 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x3 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x4 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x5 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x6 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.x7 = Var(model.u,  bounds = (0.0, 1), doc = 'Logic variable u because we need four values')
    model.TECTEST = Var(bounds = (0.0, None), doc = 'Total equipment cost')
    model.BDP = Var(bounds = (0.0, None), doc = 'Biodiesel production')
    model.flowtot = Var(model.j, model.k,  bounds = (0.0, None))
    model.flowstage = Var(model.j, model.i, bounds = (0.0, None))
    model.Waste = Var(model.j, model.k, model.i, bounds=(0.0,None))
    model.Wastestage = Var(model.j, model.i, bounds=(0.0, None))

    model.XP1 = Param(initialize = 0.6)
    model.XP2 = Param(initialize = 0.4)

    model.sumflow1 = Var(bounds = (0.0, None))
    
    "COST VARIABLES"
    model.EQCost = Var(model.j, model.k, bounds=(0.0,None), doc = 'Equipment cost')
    model.EQCostMS = Var(model.j, model.k, model.L, bounds=(0.0,None), doc = 'Equipment cost')
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
    model.Transport1 = Var(model.d, model.p, bounds=(0.0, None))
    model.Transport2 = Var(model.d, model.p, bounds=(0.0, None))
    model.Transport3 = Var(model.d, model.p, bounds=(0.0, None))
    model.TransportCost = Var(model.d, model.p, bounds=(0.0, None))
    model.TotTransportCost  = Var(bounds=(0.0, None))
    model.IntTrans1 = Var(model.j, model.k, bounds=(0.0, None))
    model.IntTrans2 = Var(model.j, model.k, bounds=(0.0, None))
    model.TotInTrans1 = Var(model.j, model.k, bounds=(0.0, None))
    model.TotInTrans2 = Var(model.j, model.k, bounds=(0.0, None))
    model.TotInTrans = Var(bounds=(0.0, None))
    model.ProductTrans11 = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.ProductTrans22 = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.ProductTrans33 = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.ProductTrans1 = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.ProductTrans2 = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.ProductTrans3 = Var(model.k, model.d, model.p,bounds=(0.0, None))
    model.TotProductTrans = Var(bounds=(0.0, None))
    model.IntDist = Var( model.d, model.k, bounds=(0.0, None))
    model.TotIntDist = Var(model.d, bounds=(0.0, None))
    
    "TEST CPLEX"
    model.InTransMS11 = Var( model.d, model.k, bounds=(0.0, None))
    model.InTransMS12 = Var( model.d, model.k, bounds=(0.0, None))
    model.InTransMS13 = Var( model.k, bounds=(0.0, None))
    model.InTransMS141 = Var( model.k, bounds=(0.0, None))
    model.InTransMS142 = Var( model.k, bounds=(0.0, None))
    model.InTransMS151 = Var( model.k, bounds=(0.0, None))
    model.InTransMS152 = Var( model.k, bounds=(0.0, None))
    model.InTransMS161 = Var( model.k, bounds=(0.0, None))
    model.InTransMS162 = Var( model.k, bounds=(0.0, None))
    model.InTransMS171 = Var( model.j, model.k, bounds=(0.0, None))
    model.InTransMS172 = Var( model.j, model.k, bounds=(0.0, None))

    
    model.InTransMS21 = Var( model.d, model.k, bounds=(0.0, None))
    model.InTransMS22 = Var( model.d, model.k, bounds=(0.0, None))
    model.InTransMS23 = Var( model.k, bounds=(0.0, None))
    model.InTransMS24 = Var( model.k, bounds=(0.0, None))
    model.InTransMS25 = Var( bounds=(0.0, None))
    
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
        if j == 3 or j == 5:
            #return model.flow[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) ) * model.SF[j,k,i] + model.M * (1-model.y[j,k])
            return model.flow[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] + model.M * (1-model.y[j,k])
            #return model.flow[j,k,i] <= (model.flowstage[j-1,i]  + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] + model.M * (1-model.y[j,k])
        if j == 4:
            if k == 2 or k == 3 or k == 4:
                return model.flow[j,k,i] <= (model.flowstage[j-1,i] * model.XP1 + (model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.XP1) + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] * model.XP1 / model.MW[1] )) * model.SF[j,k,i] + model.M * (1-model.y[j,k]) 
            if k == 5 or k == 6 or k == 7:
                return model.flow[j,k,i] <= (model.flowstage[j-1,i] * model.XP2 + model.RatiomR[j,k-3,i] * model.flowstage[j-1,1] * model.XP2 + (model.ALPHA[i] * model.MW[i] * model.CF[j,k-3,1] * model.SEL[j,k-3,i] * model.flowstage[j-1,1] * model.XP2 / model.MW[1] )) * model.SF[j,k-3,i] + model.M * (1-model.y[j,k])
            else: 
                return model.flow[j,k,i] == model.Feedflow * model.y[j,k] * model.RatiomR[j,k,i]
        else:
            return model.flow[j,k,i] == model.Feedflow * model.y[j,k] * model.RatiomR[j,k,i]
    
            
    def massbalance_rule2(model, j, k, i):
        if j == 3 or j == 5:
            #return model.flow[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] ) * model.SF[j,k,i] - model.M * (1-model.y[j,k])
            return model.flow[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] - model.M * (1-model.y[j,k])
            #return model.flow[j,k,i] >= (model.flowstage[j-1,i] + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * model.SF[j,k,i] - model.M * (1-model.y[j,k])
        if j == 4:
            if k == 2 or k == 3 or k == 4:
                return model.flow[j,k,i] >= (model.flowstage[j-1,i] * model.XP1 + (model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.XP1) + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] * model.XP1 / model.MW[1] )) * model.SF[j,k,i] - model.M * (1-model.y[j,k]) 
            if k == 5 or k == 6 or k == 7:
                return model.flow[j,k,i] >= (model.flowstage[j-1,i] * model.XP2 + model.RatiomR[j,k-3,i] * model.flowstage[j-1,1] * model.XP2 + (model.ALPHA[i] * model.MW[i] * model.CF[j,k-3,1] * model.SEL[j,k-3,i] * model.flowstage[j-1,1] * model.XP2 / model.MW[1] )) * model.SF[j,k-3,i] - model.M * (1-model.y[j,k])
            else: 
                return Constraint.Skip
        else:
            return Constraint.Skip
    
    def massbalance_rule3(model, j, k, i):
        if 3 <= j <= 4 or j == 5:
            return model.flow[j,k,i] <= model.M * model.y[j,k]
        else:
            return Constraint.Skip        
        
# =============================================================================
#     def waste_rule1(model, j, k, i):
#         if 3<=j<=4:
#             #return model.flow[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) ) * (1-model.SF[j,k,i]) + model.M * (1-model.y[j,k])
#             return model.Waste[j,k,i] <= (model.flowstage[j-1,i] + (model.RatiomR[j,k,i] * model.flowstage[j-1,1]) + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * (1-model.SF[j,k,i]) + model.M * (1-model.y[j,k])
#         else:
#             return model.Waste[j,k,i] == 0
#     
#     def waste_rule2(model, j, k, i):
#         if 3<=j<=4:
#             #return model.Waste[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] ) * (1-model.SF[j,k,i]) - model.M * (1-model.y[j,k])
#             return model.Waste[j,k,i] >= (model.flowstage[j-1,i] + model.RatiomR[j,k,i] * model.flowstage[j-1,1] + (model.ALPHA[i] * model.MW[i] * model.CF[j,k,1] * model.SEL[j,k,i] * model.flowstage[j-1,1] / model.MW[1] )) * (1-model.SF[j,k,i]) - model.M * (1-model.y[j,k])
#         else:
#             return Constraint.Skip
#     
#     def waste_rule3(model, j, k, i):
#         if 3<=j<=4:
#             return model.Waste[j,k,i] <= model.M * model.y[j,k]
#         else:
#             return Constraint.Skip
#         
# =============================================================================
    model.massrule1 = Constraint(model.j, model.k, model.i, rule = massbalance_rule1)
    model.massrule2 = Constraint(model.j, model.k, model.i, rule = massbalance_rule2)
    model.massrule3 = Constraint(model.j, model.k, model.i, rule = massbalance_rule3)

# =============================================================================
#     model.waste_rule1 = Constraint(model.j, model.k, model.i, rule = waste_rule1)
#     model.waste_rule2 = Constraint(model.j, model.k, model.i, rule = waste_rule2)
#     model.waste_rule3 = Constraint(model.j, model.k, model.i, rule = waste_rule3)
# =============================================================================
    
    def flowstage_rule(model, j, i):
        return model.flowstage[j,i] == sum(model.flow[j,k,i] for k in model.k)     
            
    def flowtot_rule(model, j,k):
        return model.flowtot[j,k] == sum(model.flow[j,k,i] for i in model.i) 
    
    model.flowstage_rule = Constraint(model.j, model.i, rule = flowstage_rule)
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
        
    #model.TESTin_rule = Constraint(model.j, model.i, rule = TESTin_rule)
    #model.TESTout_rule = Constraint(model.j, model.i, rule = TESTout_rule)
   
    
    'Logic constraint equations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    def logic_rule(model, j):
        if j<=3:
            return sum(model.y[j,k] for k in model.k) == 1
        else:
            return Constraint.Skip
        
    model.logic = Constraint(model.j, rule = logic_rule, doc = 'One option per stage') 
        
    def logic_ruleLocation1(model, j, k):
        return sum(model.y[7,k] for k in model.k) - model.y[4,2] - model.y[4,5] == 0
    
    def logic_ruleLocation2(model, j, k):
        return sum(model.y[8,k] for k in model.k) - model.y[4,3] - model.y[4,6] == 0
    
    def logic_ruleLocation3(model, j, k):
        return sum(model.y[9,k] for k in model.k) - model.y[4,4] - model.y[4,7] == 0

    model.logicLocation1 = Constraint(model.j, model.k , rule = logic_ruleLocation1, doc = 'Location 1 assigned to process 2') 
    model.logicLocation2 = Constraint(model.j, model.k , rule = logic_ruleLocation2, doc = 'Location 2 assigned to process 3') 
    model.logicLocation3 = Constraint(model.j, model.k , rule = logic_ruleLocation3, doc = 'Location 3 assigned to process 4') 
    
    def logic_ruleMS(model, j):
        if j == 4:
            return sum(model.y[j,k] for k in model.k) == 2
        else:
            return Constraint.Skip
    
    model.logicMS = Constraint(model.j, rule = logic_ruleMS, doc = 'One option per stage') 
    
    def logic_rule1(model):
       return model.y[1,1] + model.y[1,2] + model.y[1,3] + model.y[1,4] + model.y[1,5] + model.y[1,6] + model.y[1,7] + model.y[1,8] - model.y[2,1] - model.y[2,2] - model.y[2,3] == 0
    
    def logic_rule2(model):
       return model.y[2,1] + model.y[2,2] - model.y[3,1] - model.y[3,2] - model.y[3,3] == 0
   
    def logic_rule3(model):
       return model.y[2,3] - model.y[3,4] == 0
   
    def logic_rule4(model):
       return model.y[3,1] - model.y[4,1]  == 0
   
    def logic_rule5(model):
       return 2*model.y[3,2] + 2*model.y[3,3] + 2*model.y[3,4] - model.y[4,2] - model.y[4,3] - model.y[4,4] - model.y[4,5] - model.y[4,6] - model.y[4,7] == 0

    def logic_rule6(model):
       return 3*model.y[4,1] - model.y[5,1] - model.y[5,2] - model.y[5,3]  == 0
    
    def logic_rule7(model):
       return 2*model.y[4,2] + 2*model.y[4,5] - model.y[5,4] - model.y[5,5]  == 0

    def logic_rule8(model):
       return 2*model.y[4,3] + 2*model.y[4,6] - model.y[5,6] - model.y[5,7]  == 0

    def logic_rule9(model):
       return 2*model.y[4,4] + 2*model.y[4,7] - model.y[5,8] - model.y[5,9]  == 0
   
    def logic_rule13(model):
        return model.y[4,2] + model.y[4,3] + model.y[4,4] == 1
    
    def logic_rule14(model):
        return model.y[4,5] + model.y[4,6] + model.y[4,7] == 1
    
    def logic_rule15(model):
        return model.y[4,2] + model.y[4,5] <= 1
    
    def logic_rule16(model):
        return model.y[4,3] + model.y[4,6] <= 1
    
    def logic_rule17(model):
        return model.y[4,4] + model.y[4,7] <= 1
   
    def logic_rule31(model):
       return sum(model.y[6,k] for k in model.k) == 0
   
    def logic_rule32(model):
        return model.y[3,1]  == 0
    
    def logic_rule33(model):
        return model.y[2,1] - 1 == 0
    
    def logic_rule20(model):
       return model.y[7,1] + model.y[8,1] + model.y[9,1]  <= 1 
   
    def logic_rule21(model):
       return model.y[7,2] + model.y[8,2] + model.y[9,2] <= 1 
   
    def logic_rule22(model):
       return model.y[7,3] + model.y[8,3] + model.y[9,3] <= 1 
   
    def logic_rule23(model):
       return model.y[7,4] + model.y[8,4] + model.y[9,4] <= 1 
   
    def logic_rule24(model):
       return model.y[7,5] + model.y[8,5] + model.y[9,5] <= 1 
   
    def logic_rule25(model):
       return model.y[7,6] + model.y[8,6] + model.y[9,6] <= 1 
   
    def logic_rule26(model):
       return model.y[7,7] + model.y[8,7] + model.y[9,7] <= 1 
   
    def logic_rule27(model):
       return model.y[7,8] + model.y[8,8] + model.y[9,8] <= 1
   
    model.logic1 = Constraint(rule = logic_rule1)
    model.logic2 = Constraint(rule = logic_rule2)
    model.logic3 = Constraint(rule = logic_rule3)
    model.logic4 = Constraint(rule = logic_rule4)
    model.logic5 = Constraint(rule = logic_rule5)
    model.logic6 = Constraint(rule = logic_rule6)
    model.logic7 = Constraint(rule = logic_rule7)
    model.logic8 = Constraint(rule = logic_rule8)
    model.logic9 = Constraint(rule = logic_rule9)
    model.logic13 = Constraint(rule = logic_rule13)
    model.logic14 = Constraint(rule = logic_rule14)
    model.logic15 = Constraint(rule = logic_rule15)
    model.logic16 = Constraint(rule = logic_rule16)
    model.logic17 = Constraint(rule = logic_rule17)
    
    model.logic31 = Constraint(rule = logic_rule31)
    model.logic32 = Constraint(rule = logic_rule32)
    #model.logic33 = Constraint(rule = logic_rule33)
    
    model.logic20 = Constraint(rule = logic_rule20)
    model.logic21 = Constraint(rule = logic_rule21)
    model.logic22 = Constraint(rule = logic_rule22)
    model.logic23 = Constraint(rule = logic_rule23)
    model.logic24 = Constraint(rule = logic_rule24)
    model.logic25 = Constraint(rule = logic_rule25)
    model.logic26 = Constraint(rule = logic_rule26)
    model.logic27 = Constraint(rule = logic_rule27)
    
   


 
    "Transportation constraints------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    'Each transport data set is assigned to one of the three processes 2, 3, 4'
    
    def Transport_rule11(model, p):
        if p==1:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        if p==2:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        if p==3:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        if p==4:
            return sum(model.Transport1[d,p] for d in model.d) <= model.flowstage[5,8] * 8400 / 1000000
        if p==5:
            return sum(model.Transport1[d,p] for d in model.d) <= model.flowstage[5,11] * 8400 / 1000000
        if p==6:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        if p==7:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        if p==8:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        if p==9:
            return sum(model.Transport1[d,p] for d in model.d) == 0
        else:
            return Constraint.Skip
    
    def Transport_rule12(model, p):
        if p==1:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        if p==2:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        if p==3:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        if p==4:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        if p==5:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        if p==6:
            return sum(model.Transport2[d,p] for d in model.d) <= model.flowstage[5,9] * 8400 / 1000000
        if p==7:
            return sum(model.Transport2[d,p] for d in model.d) <= model.flowstage[5,19] * 8400 / 1000000
        if p==8:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        if p==9:
            return sum(model.Transport2[d,p] for d in model.d) == 0
        else:
            return Constraint.Skip
    
    def Transport_rule13(model, p):
        if p==1:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        if p==2:
            return sum(model.Transport3[d,p] for d in model.d) <= model.flowstage[5,2] * 8400 / 1000000
        if p==3:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        if p==4:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        if p==5:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        if p==6:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        if p==7:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        if p==8:
            return sum(model.Transport3[d,p] for d in model.d) <= model.flowstage[5,10] * 8400 / 1000000
        if p==9:
            return sum(model.Transport3[d,p] for d in model.d) == 0
        else:
            return Constraint.Skip
    
    def Transport_rule21(model,d,p):
        return model.Transport1[d,p] <= model.Demand[d,p]
    
    def Transport_rule22(model,d,p):
        return model.Transport2[d,p] <= model.Demand[d,p]
    
    def Transport_rule23(model,d,p):
        return model.Transport3[d,p] <= model.Demand[d,p]
        
    def Transport_rule3(model):
            #return model.TotTransportCost == sum(model.TransportCost[d,p] for d in model.d for p in model.p)
            return model.TotTransportCost == model.TotInTrans + model.TotProductTrans
    
    model.Transport_rule11 = Constraint(model.p, rule = Transport_rule11)
    model.Transport_rule12 = Constraint(model.p, rule = Transport_rule12)
    model.Transport_rule13 = Constraint(model.p, rule = Transport_rule13)
    model.Transport_rule21 = Constraint(model.d, model.p , rule = Transport_rule21)
    model.Transport_rule22 = Constraint(model.d, model.p , rule = Transport_rule22)
    model.Transport_rule23 = Constraint(model.d, model.p , rule = Transport_rule23)
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
        return model.InTransMS11[d,k] == (sum(model.flowstage[3,i] for i in model.i) * model.XP1 * model.H / 1000) / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice

    def Int_transport21(model, k, d):
        return model.InTransMS21[d,k] == (sum(model.flowstage[3,i] for i in model.i) * model.XP2 * model.H / 1000) / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice

    def Int_transport121(model, j, k, d):
        if j == 1:
            if k == 9:
                return model.InTransMS12[d,k] <=  model.N
            else:    
                return model.InTransMS12[d,k] <= model.InTransMS11[d,k] + model.N * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport122(model, j, k, d):
        if j == 1:
            if k == 9:
                return Constraint.Skip
            else:
                return model.InTransMS12[d,k] >= model.InTransMS11[d,k] - model.K * (1-model.y[j,k])
        else:
            return Constraint.Skip

    def Int_transport221(model, j, k, d):
        if j == 1:
            if k == 9:
                return model.InTransMS22[d,k] <=  model.K
            else:    
                return model.InTransMS22[d,k] <= model.InTransMS21[d,k] + model.K * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport222(model, j, k, d):
        if j == 1:
            if k == 9:
                return Constraint.Skip
            else:
                return model.InTransMS22[d,k] >= model.InTransMS21[d,k] - model.K * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport13(model, j, k, d):
        if k == 1:
            return model.InTransMS13[k] == sum(model.InTransMS12[1,k] for k in model.k)
        if k == 2:
            return model.InTransMS13[k] == sum(model.InTransMS12[2,k] for k in model.k)
        if k == 3:
            return model.InTransMS13[k] == sum(model.InTransMS12[3,k] for k in model.k)
        if k == 4:
            return model.InTransMS13[k] == sum(model.InTransMS12[4,k] for k in model.k)
        if k == 5:
            return model.InTransMS13[k] == sum(model.InTransMS12[5,k] for k in model.k)
        if k == 6:
            return model.InTransMS13[k] == sum(model.InTransMS12[6,k] for k in model.k)
        if k == 7:
            return model.InTransMS13[k] == sum(model.InTransMS12[7,k] for k in model.k)
        if k == 8:
            return model.InTransMS13[k] == sum(model.InTransMS12[8,k] for k in model.k)
        if k == 9: 
            return model.InTransMS13[k] == 10e7
        
    def Int_transport23(model, j, k, d):
        if k == 1:
            return model.InTransMS23[k] == sum(model.InTransMS22[1,k] for k in model.k)
        if k == 2:
            return model.InTransMS23[k] == sum(model.InTransMS22[2,k] for k in model.k)
        if k == 3:
            return model.InTransMS23[k] == sum(model.InTransMS22[3,k] for k in model.k)
        if k == 4:
            return model.InTransMS23[k] == sum(model.InTransMS22[4,k] for k in model.k)
        if k == 5:
            return model.InTransMS23[k] == sum(model.InTransMS22[5,k] for k in model.k)
        if k == 6:
            return model.InTransMS23[k] == sum(model.InTransMS22[6,k] for k in model.k)
        if k == 7:
            return model.InTransMS23[k] == sum(model.InTransMS22[7,k] for k in model.k)
        if k == 8:
            return model.InTransMS23[k] == sum(model.InTransMS22[8,k] for k in model.k)
        if k == 9: 
            return model.InTransMS23[k] == 10e7
        
    
        
    def Int_transport1711(model, j, k, d):
        if j == 7 or j == 8 or j == 9:
            if k == 1:
                return model.InTransMS171[j,k] <= model.InTransMS13[1] + model.K * (1-model.y[j,k])
            if k == 2:
                return model.InTransMS171[j,k] <= model.InTransMS13[2] + model.K * (1-model.y[j,k])
            if k == 3:
                return model.InTransMS171[j,k] <= model.InTransMS13[3] + model.K * (1-model.y[j,k])
            if k == 4:
                return model.InTransMS171[j,k] <= model.InTransMS13[4] + model.K * (1-model.y[j,k])
            if k == 5:
                return model.InTransMS171[j,k] <= model.InTransMS13[5] + model.K * (1-model.y[j,k])
            if k == 6:
                return model.InTransMS171[j,k] <= model.InTransMS13[6] + model.K * (1-model.y[j,k])
            if k == 7:
                return model.InTransMS171[j,k] <= model.InTransMS13[7] + model.K * (1-model.y[j,k])
            if k == 8:
                return model.InTransMS171[j,k] <= model.InTransMS13[8] + model.K * (1-model.y[j,k])
            if k == 9:
                return model.InTransMS171[j,k] == model.N * (model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport1712(model, j, k, d):
        if j == 7 or j == 8 or j == 9:
            if k == 1:
                return model.InTransMS171[j,k] >= model.InTransMS13[1] - model.K * (1-model.y[j,k])
            if k == 2:
                return model.InTransMS171[j,k] >= model.InTransMS13[2] - model.K * (1-model.y[j,k])
            if k == 3:
                return model.InTransMS171[j,k] >= model.InTransMS13[3] - model.K * (1-model.y[j,k])
            if k == 4:
                return model.InTransMS171[j,k] >= model.InTransMS13[4] - model.K * (1-model.y[j,k])
            if k == 5:
                return model.InTransMS171[j,k] >= model.InTransMS13[5] - model.K * (1-model.y[j,k])
            if k == 6:
                return model.InTransMS171[j,k] >= model.InTransMS13[6] - model.K * (1-model.y[j,k])
            if k == 7:
                return model.InTransMS171[j,k] >= model.InTransMS13[7] - model.K * (1-model.y[j,k])
            if k == 8:
                return model.InTransMS171[j,k] >= model.InTransMS13[8] - model.K * (1-model.y[j,k])
            if k == 9:
                return Constraint.Skip  
        else:
            return Constraint.Skip
        
    def Int_transport1721(model, j, k, d):
        if j == 7 or j == 8 or j == 9:
            if k == 1:
                return model.InTransMS172[j,k] <= model.InTransMS23[1] + model.K * (1-model.y[j,k])
            if k == 2:
                return model.InTransMS172[j,k] <= model.InTransMS23[2] + model.K * (1-model.y[j,k])
            if k == 3:
                return model.InTransMS172[j,k] <= model.InTransMS23[3] + model.K * (1-model.y[j,k])
            if k == 4:
                return model.InTransMS172[j,k] <= model.InTransMS23[4] + model.K * (1-model.y[j,k])
            if k == 5:
                return model.InTransMS172[j,k] <= model.InTransMS23[5] + model.K * (1-model.y[j,k])
            if k == 6:
                return model.InTransMS172[j,k] <= model.InTransMS23[6] + model.K * (1-model.y[j,k])
            if k == 7:
                return model.InTransMS172[j,k] <= model.InTransMS23[7] + model.K * (1-model.y[j,k])
            if k == 8:
                return model.InTransMS172[j,k] <= model.InTransMS23[8] + model.K * (1-model.y[j,k])
            if k == 9:
                return model.InTransMS172[j,k] == model.N * (model.y[j,k])
        else:
            return Constraint.Skip
        
    def Int_transport1722(model, j, k, d):
        if j == 7 or j == 8 or j == 9:
            if k == 1:
                return model.InTransMS172[j,k] >= model.InTransMS23[1] - model.K * (1-model.y[j,k])
            if k == 2:
                return model.InTransMS172[j,k] >= model.InTransMS23[2] - model.K * (1-model.y[j,k])
            if k == 3:
                return model.InTransMS172[j,k] >= model.InTransMS23[3] - model.K * (1-model.y[j,k])
            if k == 4:
                return model.InTransMS172[j,k] >= model.InTransMS23[4] - model.K * (1-model.y[j,k])
            if k == 5:
                return model.InTransMS172[j,k] >= model.InTransMS23[5] - model.K * (1-model.y[j,k])
            if k == 6:
                return model.InTransMS172[j,k] >= model.InTransMS23[6] - model.K * (1-model.y[j,k])
            if k == 7:
                return model.InTransMS172[j,k] >= model.InTransMS23[7] - model.K * (1-model.y[j,k])
            if k == 8:
                return model.InTransMS172[j,k] >= model.InTransMS23[8] - model.K * (1-model.y[j,k])
            if k == 9:
                return Constraint.Skip  
        else:
            return Constraint.Skip
        
    "============================================================================================================================================="   
    
    def TotInt_transport11(model, j, k):
        if j == 7:
            return model.TotInTrans1[j,k] <= model.InTransMS171[j,k] + model.K * (1-model.y[4,2])
        if j == 8:
            return model.TotInTrans1[j,k] <= model.InTransMS171[j,k] + model.K * (1-model.y[4,3])
        if j == 9:
            return model.TotInTrans1[j,k] <= model.InTransMS171[j,k] + model.K * (1-model.y[4,4])
        else:
            return model.TotInTrans1[j,k] == model.InTransMS171[j,k]
        
    def TotInt_transport12(model, j, k):
        if j == 7:
            return model.TotInTrans1[j,k] >= model.InTransMS171[j,k] - model.K * (1-model.y[4,2])
        if j == 8:
            return model.TotInTrans1[j,k] >= model.InTransMS171[j,k] - model.K * (1-model.y[4,3])
        if j == 9:
            return model.TotInTrans1[j,k] >= model.InTransMS171[j,k] - model.K * (1-model.y[4,4])
        else:
            return Constraint.Skip
    
    def TotInt_transport21(model, j, k):
        if j == 7:
            return model.TotInTrans2[j,k] <= model.InTransMS172[j,k] + model.K * (1-model.y[4,5])
        if j == 8:
            return model.TotInTrans2[j,k] <= model.InTransMS172[j,k] + model.K * (1-model.y[4,6])
        if j == 9:
            return model.TotInTrans2[j,k] <= model.InTransMS172[j,k] + model.K * (1-model.y[4,7])
        else:
            return model.TotInTrans2[j,k] == model.InTransMS172[j,k] 
        
    def TotInt_transport22(model, j, k):
        if j == 7:
            return model.TotInTrans2[j,k] >= model.InTransMS172[j,k] - model.K * (1-model.y[4,5])
        if j == 8:
            return model.TotInTrans2[j,k] >= model.InTransMS172[j,k] - model.K * (1-model.y[4,6])
        if j == 9:
            return model.TotInTrans2[j,k] >= model.InTransMS172[j,k] - model.K * (1-model.y[4,7])
        else:
            return Constraint.Skip
    
    def TotInt_transport(model):
        return model.TotInTrans == sum(model.TotInTrans1[j,k] for k in model.k for j in model.j) + sum(model.TotInTrans2[j,k] for k in model.k for j in model.j)

    
    model.IntermediateTrans11MS = Constraint(model.k, model.d, rule = Int_transport11)
    model.IntermediateTrans21MS = Constraint(model.k, model.d, rule = Int_transport21)
    model.IntermediateTrans121MS = Constraint(model.j, model.k, model.d, rule = Int_transport121)
    model.IntermediateTrans122MS = Constraint(model.j, model.k, model.d, rule = Int_transport122)
    model.IntermediateTrans221MS = Constraint(model.j, model.k, model.d, rule = Int_transport221)
    model.IntermediateTrans222MS = Constraint(model.j, model.k, model.d, rule = Int_transport222)
    model.IntermediateTrans13MS = Constraint(model.j, model.k, model.d, rule = Int_transport13)
    model.IntermediateTrans23MS = Constraint(model.j, model.k, model.d, rule = Int_transport23)
    model.IntermediateTrans1711MS = Constraint(model.j, model.k, model.d, rule = Int_transport1711)
    model.IntermediateTrans1712MS = Constraint(model.j, model.k, model.d, rule = Int_transport1712)
    model.IntermediateTrans1721MS = Constraint(model.j, model.k, model.d, rule = Int_transport1721)
    model.IntermediateTrans1722MS = Constraint(model.j, model.k, model.d, rule = Int_transport1722)
    model.TotIntermediateTrans11 = Constraint(model.j, model.k, rule = TotInt_transport11 )
    model.TotIntermediateTrans12 = Constraint(model.j, model.k, rule = TotInt_transport12 )
    model.TotIntermediateTrans21 = Constraint(model.j, model.k, rule = TotInt_transport21 )
    model.TotIntermediateTrans22 = Constraint(model.j, model.k, rule = TotInt_transport22 )
    model.TotIntermediateTrans = Constraint(rule = TotInt_transport )
    

    def Prod_transport(model, j, k, d, p):
        if j == 7:
            return model.ProductTrans1[k,d,p] ==  model.Transport1[d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice * model.y[j,k]
        if j == 8:
            return model.ProductTrans2[k,d,p] ==  model.Transport2[d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice * model.y[j,k]
        if j == 9:
            return model.ProductTrans3[k,d,p] ==  model.Transport3[d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice * model.y[j,k]
        else:
            return Constraint.Skip
    
    def Prod_transport1(model, j, k, d, p):
        if j == 7:
            return model.ProductTrans1[k,d,p] <=  model.Transport1[d,p]  + model.G * (1-model.y[j,k])
        if j == 8:
            return model.ProductTrans2[k,d,p] <=  model.Transport2[d,p]  + model.G * (1-model.y[j,k])
        if j == 9:
            return model.ProductTrans3[k,d,p] <=  model.Transport3[d,p]  + model.G * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Prod_transport2(model, j, k, d, p):
        if j == 7:
            return model.ProductTrans1[k,d,p] >=  model.Transport1[d,p]  - model.G * (1-model.y[j,k]) # 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice
        if j == 8:
            return model.ProductTrans2[k,d,p] >=  model.Transport2[d,p]  - model.G * (1-model.y[j,k])
        if j == 9:
            return model.ProductTrans3[k,d,p] >=  model.Transport3[d,p]  - model.G * (1-model.y[j,k])
        else:
            return Constraint.Skip
        
    def Prod_transport11(model, j, k, d, p):
        if j == 7:
            return model.ProductTrans11[k,d,p] ==  model.ProductTrans1[k,d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice
        if j == 8:
            return model.ProductTrans22[k,d,p] ==  model.ProductTrans2[k,d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice
        if j == 9:
            return model.ProductTrans33[k,d,p] ==  model.ProductTrans3[k,d,p] * 1000 / model.TankLoad * 2 * model.Marketdist[d,k] * model.FuelCon * model.FuelPrice
        else:
            return Constraint.Skip

    #model.ProdTrans = Constraint(model.j, model.k, model.d, model.p, rule = Prod_transport )    
    model.ProdTrans1 = Constraint(model.j, model.k, model.d, model.p, rule = Prod_transport1 )
    model.ProdTrans2 = Constraint(model.j, model.k, model.d, model.p, rule = Prod_transport2 )
    model.ProdTrans11 = Constraint(model.j, model.k, model.d, model.p, rule = Prod_transport11 )
    


    def TotProd_transport(model):
        return model.TotProductTrans == sum(model.ProductTrans11[k,d,p] for k in model.k for d in model.d for p in model.p) + sum(model.ProductTrans22[k,d,p] for k in model.k for d in model.d for p in model.p) + sum(model.ProductTrans33[k,d,p] for k in model.k for d in model.d for p in model.p)
    
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
        
    def EQ_rule2(model, u, L):
        return sum(model.x[u,L] for u in model.u) == 1
        #return model.x[1] + (1 - model.x[1]) + model.x[2] + (1 - model.x[2]) + model.x[3] + (1 - model.x[3]) == 1
    
    def EQ_rule3(model, u, j ,i,k,L):
        if j==4:
            if k==1 and L == 1:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) + model.flowstage[j-1,1] * 0.084)
            if k==2 and L == 2:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) * model.XP1 + model.flowstage[j-1,1] * model.XP1 * 0.2185) 
                #return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 <= 50000 + 50000 * 0.2185 + model.M * (1-model.y[j,k])
            if k==3 and L == 3:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) * model.XP1 + model.flowstage[j-1,1] * model.XP1 * 1.1765)
            if k==4 and L == 4:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) * model.XP1 + model.flowstage[j-1,1] * model.XP1 * 0.9781)
            if k==5 and L == 5:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) * model.XP2 + model.flowstage[j-1,1] * model.XP2 * 0.2185)
            if k==6 and L == 6:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) * model.XP2 + model.flowstage[j-1,1] * model.XP2 * 1.1765)
                #return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 <= 50000 + 50000 * 1.1765 + model.M * (1-model.y[j,k])
            if k==7 and L == 7:
                return model.x[1,L] * 0 + model.x[2,L] * 100000 + model.x[3,L] * 400000 + model.x[4,L] * 600000 == (sum(model.flowstage[j-1,i] for i in model.i) * model.XP2 + model.flowstage[j-1,1] * model.XP2 * 0.9781)
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
   
    def EQ_rule4(model, j, k, u, L):
        if j == 4:
            if k == 1 and L == 1:
                #return model.EQCost[j,k] == model.x[1] * 0 + model.x[2] * 10912000 + model.x[3] * 30863000 + model.x[4] * 4.1831e+07
                #return model.EQCost[j,k] == model.x[1] * (0.1146e6 * (0/230) ** 0.75) + model.x[2] * (0.1146e6 * (100000/230) **0.75) + model.x[3] * (0.1146e6 * (400000/230) ** 0.75) + model.x[4] * (0.1146e6 * (600000/230) ** 0.75)
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (0.1146e6 * (0/230) ** (0.75)) + model.x[2,L] * (0.1146e6 * (100000/230) **(0.75)) + model.x[3,L] * (0.1146e6 * (400000/230) ** (0.75)) + model.x[4,L] * (0.1146e6 * (600000/230) ** (0.75))) + model.N * (1-model.y[j,k]) 
                'Should at binary variable at the end and the additional equations for k == 2 3 4'
                
            if k == 2 and L == 2:
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (1.5543e6 * (0/3296) ** (0.75)) + model.x[2,L] * (1.5543e6 * (100000/3296) **(0.75)) + model.x[3,L] * (1.5543e6 * (400000/3296) ** (0.75)) + model.x[4,L] * (1.5543e6 * (600000/3296) ** (0.75))) + model.N * (1-model.y[j,k]) 
            if k == 3 and L == 3:
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (1.3485e6 * (0/4600) ** (0.75)) + model.x[2,L] * (1.3485e6 * (100000/4600) **(0.75)) + model.x[3,L] * (1.3485e6 * (400000/4600) ** (0.75)) + model.x[4,L] * (1.3485e6 * (600000/4600) ** (0.75))) + model.N * (1-model.y[j,k]) 
            if k == 4 and L == 4:
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (4.8155e6 * (0/8500) ** (0.75)) + model.x[2,L] * (4.8155e6 * (100000/8500) **(0.75)) + model.x[3,L] * (4.8155e6 * (400000/8500) ** (0.75)) + model.x[4,L] * (4.8155e6 * (600000/8500) ** (0.75))) + model.N * (1-model.y[j,k]) 
            if k == 5 and L == 5:
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (1.5543e6 * (0/3296) ** (0.75)) + model.x[2,L] * (1.5543e6 * (100000/3296) **(0.75)) + model.x[3,L] * (1.5543e6 * (400000/3296) ** (0.75)) + model.x[4,L] * (1.5543e6 * (600000/3296) ** (0.75))) + model.N * (1-model.y[j,k]) 
            if k == 6 and L == 6:
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (1.3485e6 * (0/4600) ** (0.75)) + model.x[2,L] * (1.3485e6 * (100000/4600) **(0.75)) + model.x[3,L] * (1.3485e6 * (400000/4600) ** (0.75)) + model.x[4,L] * (1.3485e6 * (600000/4600) ** (0.75))) + model.N * (1-model.y[j,k]) 
            if k == 7 and L == 7:
                return model.EQCostMS[j,k,L] <= (model.x[1,L] * (4.8155e6 * (0/8500) ** (0.75)) + model.x[2,L] * (4.8155e6 * (100000/8500) **(0.75)) + model.x[3,L] * (4.8155e6 * (400000/8500) ** (0.75)) + model.x[4,L] * (4.8155e6 * (600000/8500) ** (0.75))) + model.N * (1-model.y[j,k]) 
            else:
                return model.EQCostMS[j,k,L] == 0
        else:
            return Constraint.Skip
    
    def EQ_rule44(model, j, k, u, L):
        if j == 4:
            if k == 1 and L == 1:
                #return model.EQCost[j,k] == model.x[1] * 0 + model.x[2] * 10912000 + model.x[3] * 30863000 + model.x[4] * 4.1831e+07
                #return model.EQCost[j,k] == model.x[1] * (0.1146e6 * (0/230) ** 0.75) + model.x[2] * (0.1146e6 * (100000/230) **0.75) + model.x[3] * (0.1146e6 * (400000/230) ** 0.75) + model.x[4] * (0.1146e6 * (600000/230) ** 0.75)
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (0.1146e6 * (0/230) ** (0.75)) + model.x[2,L] * (0.1146e6 * (100000/230) **(0.75)) + model.x[3,L] * (0.1146e6 * (400000/230) ** (0.75)) + model.x[4,L] * (0.1146e6 * (600000/230) ** (0.75))) - model.N * (1-model.y[j,k])      
                'Should at binary variable at the end and the additional equations for k == 2 3 4'
                
            if k == 2 and L == 2:
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (1.5543e6 * (0/3296) ** (0.75)) + model.x[2,L] * (1.5543e6 * (100000/3296) **(0.75)) + model.x[3,L] * (1.5543e6 * (400000/3296) ** (0.75)) + model.x[4,L] * (1.5543e6 * (600000/3296) ** (0.75))) - model.N * (1-model.y[j,k])    
            if k == 3 and L == 3:
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (1.3485e6 * (0/4600) ** (0.75)) + model.x[2,L] * (1.3485e6 * (100000/4600) **(0.75)) + model.x[3,L] * (1.3485e6 * (400000/4600) ** (0.75)) + model.x[4,L] * (1.3485e6 * (600000/4600) ** (0.75))) - model.N * (1-model.y[j,k]) 
            if k == 4 and L == 4:
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (4.8155e6 * (0/8500) ** (0.75)) + model.x[2,L] * (4.8155e6 * (100000/8500) **(0.75)) + model.x[3,L] * (4.8155e6 * (400000/8500) ** (0.75)) + model.x[4,L] * (4.8155e6 * (600000/8500) ** (0.75))) - model.N * (1-model.y[j,k]) 
            if k == 5 and L == 5:
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (1.5543e6 * (0/3296) ** (0.75)) + model.x[2,L] * (1.5543e6 * (100000/3296) **(0.75)) + model.x[3,L] * (1.5543e6 * (400000/3296) ** (0.75)) + model.x[4,L] * (1.5543e6 * (600000/3296) ** (0.75))) - model.N * (1-model.y[j,k]) 
            if k == 6 and L == 6:
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (1.3485e6 * (0/4600) ** (0.75)) + model.x[2,L] * (1.3485e6 * (100000/4600) **(0.75)) + model.x[3,L] * (1.3485e6 * (400000/4600) ** (0.75)) + model.x[4,L] * (1.3485e6 * (600000/4600) ** (0.75))) - model.N * (1-model.y[j,k]) 
            if k == 7 and L == 7:
                return model.EQCostMS[j,k,L] >= (model.x[1,L] * (4.8155e6 * (0/8500) ** (0.75)) + model.x[2,L] * (4.8155e6 * (100000/8500) **(0.75)) + model.x[3,L] * (4.8155e6 * (400000/8500) ** (0.75)) + model.x[4,L] * (4.8155e6 * (600000/8500) ** (0.75))) - model.N * (1-model.y[j,k]) 
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
            
    def EQ_rule5(model, j,k):
        if j == 4:
            return model.EQCost[j,k] == sum(model.EQCostMS[j,k,L] for L in model.L)
        else:
            return Constraint.Skip
            
    def EQ_rule6(model, u,L):
        if L == 1:
            return model.x1[u] == model.x[u,L]
        if L == 2:
            return model.x2[u] == model.x[u,L]
        if L == 3:
            return model.x3[u] == model.x[u,L]
        if L == 4:
            return model.x4[u] == model.x[u,L]
        if L == 5:
            return model.x5[u] == model.x[u,L]
        if L == 6:
            return model.x6[u] == model.x[u,L]
        if L == 7:
            return model.x7[u] == model.x[u,L]
        else:
            return Constraint.Skip
    
    model.EQ1 = Constraint(model.j, model.k, model.i, model.a, rule = EQ_rule1)
    model.EQ2 = Constraint(model.u, model.L, rule = EQ_rule2)
    model.EQ3 = Constraint(model.u, model.j, model.i, model.k, model.L , rule = EQ_rule3)
    model.EQ4 = Constraint(model.j, model.k, model.u, model.L, rule = EQ_rule4)
    model.EQ44 = Constraint(model.j, model.k, model.u, model.L, rule = EQ_rule44)
    model.EQ5 = Constraint( model.j,  model.k , rule = EQ_rule5)
    model.EQ6 = Constraint(model.u, model.L, rule = EQ_rule6)
    model.EQ7 = SOSConstraint(var=model.x1, sos=2)
    model.EQ8 = SOSConstraint(var=model.x2, sos=2)
    model.EQ9 = SOSConstraint(var=model.x3, sos=2)
    model.EQ10 = SOSConstraint(var=model.x4, sos=2)
    model.EQ11 = SOSConstraint(var=model.x5, sos=2)
    model.EQ12 = SOSConstraint(var=model.x6, sos=2)
    model.EQ13 = SOSConstraint(var=model.x7, sos=2)

    
    
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
        if j==3:
            return model.SECCost[j,k,i] <= model.RatiomR[j,k,i] * model.flowstage[j-1,1]* model.CCost[i] + model.M * (1-model.y[j,k])
        if j == 4:
            if k == 2 or k == 3 or k == 4:
                return model.SECCost[j,k,i] <= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.XP1 * model.CCost[i] + model.M * (1-model.y[j,k])
            if k == 5 or k == 6 or k == 7:
                return model.SECCost[j,k,i] <= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.XP2 * model.CCost[i] + model.M * (1-model.y[j,k])
            else:
                return model.SECCost[j,k,i] == 0
        else:
            return model.SECCost[j,k,i] == 0
        
    def SECCost_rule2(model, j, k, i):
        if j==3:
            return model.SECCost[j,k,i] >= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.CCost[i] - model.M * (1-model.y[j,k])
        if j == 4:
            if k == 2 or k == 3 or k == 4:
                return model.SECCost[j,k,i] >= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.XP1 * model.CCost[i] - model.M * (1-model.y[j,k])
            if k == 5 or k == 6 or k == 7:
                return model.SECCost[j,k,i] >= model.RatiomR[j,k,i] * model.flowstage[j-1,1] * model.XP2 * model.CCost[i] - model.M * (1-model.y[j,k])
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
        
    def SECCost_rule3(model, j, k, i):
        if 3<=j<=4:
            return model.SECCost[j,k,i] <= model.M * model.y[j,k]
        else:
            return Constraint.Skip
        
    def TotSECCost_rule(model, j,k,i):
        if i<= 20 or i==25: 
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
    def Util_rule1(model, j, k, u):
        if j == 3:
            if k == 2 or k == 3:
                return model.Util[j,k,u] <= ((model.Feedflow - model.flowstage[j-1,1]) * model.Tau[j,k,u] / 1000) + model.M * (1-model.y[j,k])
            else:
                return model.Util[j,k,u] == model.Feedflow * model.Tau[j,k,u] / 1000 * model.y[j,k]
        if j == 4:
            if k == 2 or k == 3 or k == 4:
                return model.Util[j,k,u] <= (sum(model.flowstage[j-1,i] for i in model.i) * model.XP1 * model.Tau[j,k,u] / 1000) + model.M * (1-model.y[j,k])
            if k == 5 or k == 6 or k == 7:
                return model.Util[j,k,u] <= (sum(model.flowstage[j-1,i] for i in model.i) * model.XP2 * model.Tau[j,k,u] / 1000) + model.M * (1-model.y[j,k])
            else:
                return model.Util[j,k,u] == 0
        else:
            return model.Util[j,k,u] == 0
        
    def Util_rule11(model, j, k, u):
        if j == 3:
            if k == 2 or k == 3:
                return model.Util[j,k,u] >= ((model.Feedflow - model.flowstage[j-1,1]) * model.Tau[j,k,u] / 1000) - model.M * (1-model.y[j,k])
            else:
                return Constraint.Skip
        if j == 4:
            if k == 2 or k == 3 or k == 4:
                return model.Util[j,k,u] >= (sum(model.flowstage[j-1,i] for i in model.i) * model.XP1 * model.Tau[j,k,u] / 1000) - model.M * (1-model.y[j,k])
            if k == 5 or k == 6 or k == 7:
                return model.Util[j,k,u] >= (sum(model.flowstage[j-1,i] for i in model.i) * model.XP2 * model.Tau[j,k,u] / 1000) - model.M * (1-model.y[j,k])
            else:
                return Constraint.Skip
        else:
            return Constraint.Skip
            
    
    model.Util_rule1 = Constraint(model.j, model.k, model.u, rule = Util_rule1)
    model.Util_rule11 = Constraint(model.j, model.k, model.u, rule = Util_rule11)
    
    
    def TUC_rule(model):
        return model.TUC == model.H * sum(model.Util[j,k,u] * model.Uprice[u] for j in model.j for k in model.k for u in model.u)
    
    model.TUC_rule = Constraint(rule = TUC_rule)
    
    
    
    
    
    "Profit calculation------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'"
    def TarProd_rule(model, p):
        if p == 1:
            return model.TarProd[p] == (sum(model.Transport1[d,1] for d in model.d) + sum(model.Transport2[d,1] for d in model.d) + sum(model.Transport3[d,1] for d in model.d)) * 0.493 * 1000000
        if p == 2:
            return model.TarProd[p] == (sum(model.Transport1[d,2] for d in model.d) + sum(model.Transport2[d,2] for d in model.d) + sum(model.Transport3[d,2] for d in model.d)) * 0.485 * 1000000
        if p == 3:
            return model.TarProd[p] == (sum(model.Transport1[d,3] for d in model.d) + sum(model.Transport2[d,3] for d in model.d) + sum(model.Transport3[d,3] for d in model.d)) * 0.895 * 1000000
        if p == 4:
            return model.TarProd[p] == (sum(model.Transport1[d,4] for d in model.d) + sum(model.Transport2[d,4] for d in model.d) + sum(model.Transport3[d,4] for d in model.d)) * 1.2 * 1000000
        if p == 5:
            return model.TarProd[p] == (sum(model.Transport1[d,5] for d in model.d) + sum(model.Transport2[d,5] for d in model.d) + sum(model.Transport3[d,5] for d in model.d)) * 0.761*1000000
        if p == 6:
            return model.TarProd[p] == (sum(model.Transport1[d,6] for d in model.d) + sum(model.Transport2[d,6] for d in model.d) + sum(model.Transport3[d,6] for d in model.d)) * 1.1 * 1000000
        if p == 7:
            return model.TarProd[p] == (sum(model.Transport1[d,7] for d in model.d) + sum(model.Transport2[d,7] for d in model.d) + sum(model.Transport3[d,7] for d in model.d)) * 0.485 * 1000000 
        if p == 8:
            return model.TarProd[p] == (sum(model.Transport1[d,8] for d in model.d) + sum(model.Transport2[d,8] for d in model.d) + sum(model.Transport3[d,8] for d in model.d)) * 1.1 * 1000000
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
        #return model.TAR == 0
        return model.TAR == sum(model.TarProd[p] for p in model.p)
    
    def AIC_rule(model):
        IRCalc = (model.IR * (model.IR + 1)**model.LS)/((model.IR + 1)** model.LS - 1)
        return model.AIC == (model.TotalTIC + model.TotalTDC)/ model.LS * IRCalc

    
    def AOC_rule(model):
        return model.AOC == model.RMC + model.TUC + model.OMC + model.TotTransportCost + model.TotTrCost 
    
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
            return model.Results[k] == model.TotTrCost  + model.TotTransportCost
        elif k == 7:
            return model.Results[k] == model.TotalTIC 
        elif k == 8:
            return model.Results[k] == model.TotalTDC 
        elif k == 9:
            return model.Results[k] == model.OMC
# =============================================================================
#         elif k == 7:
#             return model.Results[k] == model.TotProductTrans
#         elif k == 8:
#             return model.Results[k] == model.TotInTrans 
#         elif k == 9:
#             return model.Results[k] == model.TotTrCost
# =============================================================================
    
    model.Results_rule = Constraint( model.k, rule = Results_rule)
    
    
    'Objective Function------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    
    def OBJ_rule(model):
        #return model.OBJ ==  model.AIC + model.AOC - model.TAR
        return model.OBJ == model.TAR - model.AIC - model.AOC
        #return model.OBJ == sum(model.y[j,k] * model.EC[j,k] for k in model.k for j in model.j)
        
    model.OBJ_rule = Constraint(rule = OBJ_rule)
    
    
    
# =============================================================================
#     def FCI_rule(model):
#        IRCalc = (model.IR * (model.IR + 1)**model.LS)/((model.IR + 1)** model.LS - 1)
#        #return model.FCI == ((model.TotalTIC + model.TotalTDC)/ model.LS * IRCalc) + model.RMC + model.TotTrCost + model.TUC + model.OMC
#        return model.FCI == model.TAR - ((model.TotalTIC + model.TotalTDC)/ model.LS * IRCalc) - model.RMC - model.TotTrCost - model.TUC - model.OMC
#        #return model.FCI == sum(model.y[j,k] * model.EC[j,k] for k in model.k for j in model.j)
# 
#     model.FCI_rule = Constraint(rule = FCI_rule)
# =============================================================================
   

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
        model.AIC.display()

    
    
# =============================================================================
#     # This emulates what the pyomo command-line tools does
#     from pyomo.opt import SolverFactory
#     import pyomo.environ
#     opt = SolverFactory("glpk")
#     results = opt.solve(model)
#     #sends results to stdout
#     results.write()
#     print("\nDisplaying Solution\n" + '-'*60)
#     #pyomo_postprocess(None, model, results)
# =============================================================================
    
# =============================================================================
#     from pyomo.opt import SolverFactory
#     import pyomo.environ
#     #opt = SolverFactory("glpk")
#     opt = SolverFactory("cplex")
#     results = opt.solve(model)
#     #sends results to stdout
#     results.write()
#     print("\nDisplaying Solution\n" + '-'*60)
#     #pyomo_postprocess(None, model, results)
# =============================================================================
    
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("gurobi",solver_io="python")
    opt.options['NonConvex'] = 2   
    results = opt.solve(model, tee = True)
    #sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, model, results)
    
    return model