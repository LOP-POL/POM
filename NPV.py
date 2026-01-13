from functools import reduce
buying = {
"buildingCosts" : 1.5,
"land_costs" : 0.5,
"equipment" : 3,
}   
renting = {
    "buildingLand" : 40000
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
    return ((40000/10**6) * 5) + 3

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
    print(netSales)
    print(netSalesPerYearPerPlant)
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

print([i for i in calcCashFlows().values()])


def calcNPVBuilding(maintainYearly=False):

    cashFlows = [i for i in calcCashFlows().values()]
    initial_investment = calcSumBuilding()
    NPV = -initial_investment
    i = 0
    maintenance = initial_investment * 0.15
    if(maintainYearly):
        while i < 5:
            NPV += (cashFlows[i] - maintenance) / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**i
            i+=1
    else:
        NPV -= maintenance * 5
        while i < 5:
            NPV += cashFlows[i] / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**i
            i+=1
    
    return NPV + RESIDUAL_VALUE_BUILDING * buying["buildingCosts"] + RESIDUAL_VALUE_LAND * buying["land_costs"]
    

def calcNPVRenting():
    cashFlows = [i for i in calcCashFlows().values()]
    initial_investment = calcSumRenting()
    NPV = -initial_investment
    i = 0
    maintenance = initial_investment * 0.15
    while i < 5:
        NPV += (cashFlows[i] - maintenance) / (1 + COMPOUDED_MONTHLY_DISCOUNT_RATE)**i
        i+=1
    return NPV


if __name__ == "__main__":
    print(calcNetSalesPerYear())
    print(calcCashFlows())
    print("building NPV yearly maintenance:", calcNPVBuilding(True))
    print("building NPV initial:", calcNPVBuilding(False))
    print("building NPV renting :", calcNPVRenting())

    with open("records.txt",'a') as myRecords:
        results = f"building NPV yearly maintenance: {calcNPVBuilding(True)}\nbuilding NPV initial: {calcNPVBuilding(False)}\nbuilding NPV renting: {calcNPVRenting()}\n"
        myRecords.write(results)
        myRecords.close()

    
        
            
              

  
