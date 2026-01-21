from functools import reduce

buying = {
"buildingCosts" : 1.5,
"land_costs" : 0.5,
"equipment" : 3,
"productionDnP":0.5
}   
renting = {
    "productionDnP":0.5,
    "equipment":3,
}

projectedAnnualSales = {
    "2026":0.1, 
    "2027":0.3,
    "2028":0.8,
    "2029":1.0,
    "2030":1.3,
}

consumablesCost = {
    "D":5000,
    "E":6000,
    "F":4500
}
salesPrice = {
    "D":7500,
    "E":8000,
    "F":6000
}
COMPOUDED_MONTHLY_DISCOUNT_RATE = 0.1
RESIDUAL_VALUE_LAND = 0.8
RESIDUAL_VALUE_BUILDING =0


def calcSumBuilding():
    costs = [i for i in buying.values()]
    totalCosts = reduce(lambda i,j:i + j,costs)
    # adjust for each years maintenance 
    return totalCosts


def calcSumRenting():
    return reduce(lambda i,j: i + j,[i for i in renting.values()])


def calcNetSalesPerYear():
    netSalesPerYear = {

    }
    for k, v in consumablesCost.items():
        netSalesPerYear[k] = salesPrice[k] - v
    return netSalesPerYear

def calcTotalNetSales():
    netSales = calcNetSalesPerYear()
    netSalesPerYearPerPlant = [i for i in netSales.values()]
    totalNetSales = reduce(lambda i,j: i + j,netSalesPerYearPerPlant)
    
    return totalNetSales

calcTotalNetSales()

def calcCashFlows():
    #  Normalize cashFlows so they are in terms of a million
    totalNetSales = calcTotalNetSales()
    cashFlowsPerYear = {

    }
    years =  [i for i in projectedAnnualSales.keys()]
    for k in years:
        cashFlowsPerYear[k] = (totalNetSales * projectedAnnualSales[k]) / 10**6

    return cashFlowsPerYear 

def calcLabour():
    perHour = 20
    hoursPerDay = 16
    DaysAYear = 360
    return (DaysAYear * hoursPerDay * perHour)/10**6

def calcAverageNetSales():
    netSales = calcNetSalesPerYear().values()
    return  sum(netSales) / len(netSales)
     
def calcCashFlowsAverge():
     #  Normalize cashFlows so they are in terms of a million
    averageNetSales = calcAverageNetSales()
    cashFlowsPerYear = {

    }
    years =  [i for i in projectedAnnualSales.keys()]
    for k in years:
        cashFlowsPerYear[k] = (averageNetSales * projectedAnnualSales[k]) / 10**6
    return cashFlowsPerYear 
    
# print([i for i in calcCashFlows().values()])

#  Wrong fomula with residula value in wrong place
def calcNPVBuilding(maintainYearly=False):
    iterations = len(projectedAnnualSales.keys())

    cashFlows = [i for i in calcCashFlows().values()]

    initial_investment = calcSumBuilding()
    NPV = -initial_investment
    i = 0
    maintenance = initial_investment * 0.15
    if(maintainYearly):
        while i < iterations:
            NPV += (cashFlows[i] - maintenance - calcLabour()) / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**i
            i+=1
    else:
        NPV -= maintenance * iterations
        while i < iterations:
            NPV += cashFlows[i] / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**i
            i+=1
    #  Residual value is in the last year so make sure to do the calculation for it at the end.
    return NPV + RESIDUAL_VALUE_BUILDING * buying["buildingCosts"] + RESIDUAL_VALUE_LAND * buying["land_costs"]


# The correct formula with the residual value inside and divided by dicount factor
def calcResidualValue():
    iters = len(projectedAnnualSales.keys())
    return (RESIDUAL_VALUE_BUILDING * buying["buildingCosts"] + RESIDUAL_VALUE_LAND * buying["land_costs"])/(1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**iters


def calcBuildingNPVResInside(maintainYearly=False):
    iterations = len(projectedAnnualSales.keys())

    cashFlows = [i for i in calcCashFlows().values()]

    initial_investment = calcSumBuilding()
    NPV = -initial_investment
    i = 0
    maintenance = buying["buildingCosts"] * 0.15
    if(maintainYearly):
        while i < iterations:
            NPV += (cashFlows[i] - maintenance  - calcLabour()) / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**(i+1)
            i+=1
    else:
        NPV -= maintenance * iterations
        while i < iterations:
            NPV += cashFlows[i] / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**(i+1)
            i+=1
    #  Residual value is in the last year so make sure to do the calculation for it at the end.
    return NPV + (RESIDUAL_VALUE_BUILDING * buying["buildingCosts"] + RESIDUAL_VALUE_LAND * buying["land_costs"])/(1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**iterations
 
#  This calculates the partial values of the NPV for each year 
def calcPVsRenting():
    PVs = []
    cashFlows = calcCashFlows() # Can be switched to average 
    cashOut = ((40000/10**6) * 12) + calcLabour()
    
    for i,v in enumerate(cashFlows.values()):
        PVs.append( (v - cashOut) /(1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**(i + 1))
        print(PVs[i])
    return PVs

#  Used to get the PV for just buying
def calcPVsBuying():
    PVs = []
    maintenance = buying["buildingCosts"] * 0.15
    for i,v in enumerate(calcCashFlows().values()):
        PVs.append((v - maintenance - calcLabour())/(1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**(i+1))
        print(PVs[i])
    return PVs

# Final buying NPV
def calcNPVBuyingIn():
    I_o = calcSumBuilding()
    return reduce(lambda i,j: i +j ,calcPVsBuying()) + calcResidualValue() - I_o

# Final Renting NPV
def calcNPVRentingIn():
    I_o = calcSumRenting()
    return reduce(lambda i,j: i +j ,calcPVsRenting()) - I_o

# Without intermediate logging
def calcNPVRenting():
    cashFlows = [i for i in calcCashFlowsAverge().values()]
    initial_investment = calcSumRenting()
    NPV = -initial_investment
    i = 0
    maintenance = initial_investment * 0.15
    while i < 5:
        NPV += (cashFlows[i] - maintenance - calcLabour()) / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**i
        i+=1
    return NPV

if __name__ == "__main__":
    # print(calcNetSalesPerYear())
    # print(calcCashFlows())
   
    print("building NPV with intermediate logging", calcNPVBuyingIn())
    print("Renting NPV with logging\n", calcNPVRentingIn())

    print("\nWrong results you would get if maintenance calculated at once and residual value without discount rate\n")

    print("building NPV, yearly maintenance initial:", calcNPVBuilding(True))
    print("building NPV, maintenance all calculated in the beginning :",calcNPVBuilding(False))

    with open("records.txt",'a') as myRecords:
        results = f"building NPV yearly maintenance: {calcNPVBuilding(True)}\nbuilding NPV initial: {calcNPVBuilding(False)}\nbuilding NPV renting: {calcNPVRenting()}\n building res inside {calcBuildingNPVResInside(True)}\n"
        myRecords.write(results)
        myRecords.close()

    
        
            
              

  
