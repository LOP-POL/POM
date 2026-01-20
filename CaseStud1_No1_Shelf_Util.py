from math import ceil
from functools import reduce
import sys
data_yield = [
    ["A", 0.5],
    ["B", 0.3],
    ["C", 0.4],
]
years = [2026, 2027, 2028, 2029, 2030]

# Projected Sales per year
plant_a = [1.5, 1.1, 0.8, 0.5, 0.0]
plant_b = [0.0, 0.1, 0.3, 0.5, 0.6]
plant_c = [0.6, 1.2, 0.6, 1.2, 0.6]

year_shelves = []

year_profits_losses = []

# information about the previous year 
shelvesSwitched = False
transition = 3
pastTransition = transition


def calcShelvesForAYear(pro_year,yield_p_shelf):
   return ceil(pro_year/yield_p_shelf)

# value is a list of the shelves allocated to plant A B and C eg [3,0,2]
# idx is and index referencing the years e.g 2026 - 0 


def calcProjectedShelvesSize(idx):
    p_resA = calcShelvesForAYear(pro_year=plant_a[idx],yield_p_shelf=data_yield[0][1])
    p_resB = calcShelvesForAYear(pro_year=plant_b[idx],yield_p_shelf=data_yield[1][1])
    p_resC = calcShelvesForAYear(pro_year=plant_c[idx],yield_p_shelf=data_yield[2][1])

    return [p_resA,p_resB,p_resC]

def calcYields(value):
    yieldA = value[0]*data_yield[0][1]
    yieldB = value[1]*data_yield[1][1]
    yieldC = value[2]*data_yield[2][1]
    print(f"yields {[yieldA,yieldB,yieldC]}")
    return [yieldA,yieldB,yieldC]
    
def calcProfitsAndLosses(value,idx):
    prof_loss_A = round(value[0]*data_yield[0][1] - plant_a[idx],2)
    prof_loss_B = round(value[1]*data_yield[1][1] - plant_b[idx],2)
    prof_loss_C = round(value[2]*data_yield[2][1] - plant_c[idx],2)

    print([prof_loss_A,prof_loss_B,prof_loss_C])
    return [prof_loss_A,prof_loss_B,prof_loss_C]

# Growing requires one worker per 0.1 tons of annual yield. Each
# used shelf needs one team leader for management and one technician per produced plant type. A

def calcWorkers(value):
    yields = calcYields(value=value)
    workersPerPlant = []
    for idx,shelves in enumerate(value):
        workers = 0
        technicians = 3
        leaders = 0

        leaders += shelves
        if(shelves>0):
            technicians +=1

        workers += yields[idx]/0.1

        workersPerPlant.append([int(workers), int(technicians) ,int(leaders)])
    print(f"workers per plant:{workersPerPlant}")
    return workersPerPlant

def calcShelvesAuto():
    return

def collectInputs():
    result = []
    for year in years:
        result.append([int(x) for x in input(f"Shelves for {year}: ").split()])
    return result
    
def main():
    mode = "m"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = ""
    
    # shelfA=int(sys.argv[1]),shelfB=int(sys.argv[2]),shelfC=int(sys.argv[3]), year=int(sys.argv[4])
    # print(sys.argv[1])
    # print(sys.argv)
    # print(shelfA)``
    # print(type(shelfA))

    # collect inputs
    inputs = []
    if mode == "m":
        inputs = collectInputs()
        print(input)
    elif mode == "s":
        inputs.append([int(x) for x in input(f"Shelves for year (spaces between numbers, 3 0 2 0 , A B C year[idx]):\n ").split()])
    else:
        inputs = [
        [3, 0, 2 ,0],
        [1,1, 2, 1],
        [1 ,1 ,2, 2],
        [1 ,2, 1, 3],
        [0, 2, 2, 4]]
        print(input)

    totalProfitsAndLoss = 0
   
    for i in inputs:
        value = [i[0],i[1],i[2]]
        year = i[3]
        print(years[i[3]])
        print(value[:3])

        totalNumberOfGivenShelfs = reduce(lambda x,y : x + y, value )
        projectedShelvesForThatYear = calcProjectedShelvesSize(year)

        # print(f"Total Numbe of shelves you will use:{totalNumberOfGivenShelfs} \n")
        # print(f" Number of shelves needed to meet projected target:{reduce(lambda x,y : x + y,projectedShelvesForThatYear)} ")

        prof_Loss = calcProfitsAndLosses(value=value,idx=year)
        
        totalProfitsAndLoss += round(reduce(lambda x,y:x + y,prof_Loss),3)


        workers = calcWorkers(value=value)
        print(workers)

        with open("records.txt",'a') as record:
            record.write("\nA B C \n ")
            record.write(f"Shelves \n {''.join(str(x) for x in value)}")
            record.write(f"\nProfits and losses relative to projected \n {' '.join(str(x) for x in prof_Loss)}")
            record.write("\nworkers technicians leaders\n")
            record.write(f"{' '.join(str(x) for x in workers[0])} \n" + f"{' '.join(str(x) for x in workers[1])} \n" + f"{' '.join(str(x) for x in workers[2])}" )
            record.close()
    print("Total Loss and Profit",totalProfitsAndLoss)
if __name__ == '__main__':
    main()

        
       

    




         