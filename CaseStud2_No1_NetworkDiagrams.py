import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from functools import reduce
# Project activities and Durations
project_activities = {
    "Research on the growing process of the new plants": 20,
    "Specifying the required equipment": 10,
    "Purchase equipment": 32,
    "Equipment commissioning": 10,
    "Hire workers": 26,
    "Train workers": 12,
    "Negotiate contracts with suppliers": 12,
    "Material delivery by suppliers": 36,
    "Ramp up": 16
}

def organizeData():
    descriptions = [i for i in project_activities.keys()]
    designations = [chr(i) for i in range(ord('A'), ord('A') + len(descriptions))]
    print(designations)
    durations = [i for i in project_activities.values()]

    activitiesDataframe = {
        "designations":designations,
        "descriptions":descriptions,
        "durations":durations
    }

    return activitiesDataframe

activitiesDataframe = pd.DataFrame(organizeData())
START = "A"
END = "I"
parallelParts = [""]
# Edges =  {'X': ['Y'], 'C': ['M'], 'M': ['C', 'F', 'Y'], 'Q': ['F'], 'Y': ['X', 'M'], 'F': ['M', 'Q']}
def orderVertices(orderedList: dict,activitiesDataframe):
    weights = {}
    # {('M', 'C'): 44, ('Q', 'F'): 27, ('Y', 'X'): 42, ('X', 'Y'): 42, ('Y', 'M'): 6, ('M', 'F'): 9, ('M', 'Y'): 6, ('F', 'Q'): 27, ('F', 'M'): 9, ('C', 'M'): 44} 
    for k,v in  orderedList.items():
        weight = activitiesDataframe[activitiesDataframe["designations"] == k]["durations"].values[0]
        for i in v:
            weights.update({(k,i):weight})
    return weights

Edges = {"A":["B"],
         "B":["G"],
         "G":["C","E","H"],
         "E":["F"],
         "C":["D"],
         "F":["D"],
         "H":["I"],
         "D":["I"]}

def addToList(currentLine:list,currentKey:str,valueIter:int,paths:list,startKey:str,endKey:str,maxBranches:int):
   
    # print("start",currentLine)
    if currentKey != endKey:
        currentLine.append(currentKey)
        # setting current key
        if (len(Edges[currentKey]) - 1) < valueIter:
           
            currentKey = Edges[currentKey][len(Edges[currentKey])-1]
           
        else:
            currentKey =  Edges[currentKey][valueIter]

        return addToList(currentLine,currentKey,valueIter,paths,startKey,endKey,maxBranches=maxBranches)
    # running the loop and moving to next branch
    else:
        currentLine.append(currentKey)
        currentKey = startKey
        # print(currentLine)
        paths.append(currentLine)
        if valueIter != maxBranches - 1:
            valueIter += 1
            currentLine = []
            return addToList(currentLine,currentKey,valueIter,paths,startKey,endKey,maxBranches=maxBranches)
    return paths
            
def getWeightFromDataframe(item:str):

    return activitiesDataframe[activitiesDataframe["designations"] == item]["durations"].values[0]



def getListOfweights(item:list):
   return [int(getWeightFromDataframe(i)) for i in item]

def addUpWeights(item:list):
    return reduce(lambda x,y: x + y , getListOfweights(item))



def calcPaths():
    keys = [i for i in Edges.keys()]
    branches = reduce(lambda i,j: i if len(i)>len(j) else j,Edges.values() )
    maxBranches = len(branches)
    endKey = Edges[keys[len(keys)-1]][0]
    startKey = keys[0]
    valueIter = 0
    currentKey = ""
    currentLine = []
    currentKey = keys[0]
    paths = []
    paths = addToList(currentLine=currentLine,currentKey=currentKey,valueIter=valueIter,endKey=endKey,maxBranches=maxBranches,paths=paths,startKey=startKey)

    calcs = {}
   

    for i in range(len(paths)):
        print(paths[i])
        calcs[i] = (paths[i],getListOfweights(paths[i]),addUpWeights(paths[i]))
    return calcs

print(calcPaths())

PATHS = calcPaths()

def calcLongestPath():
    return max([v[2] for v in PATHS.values])

def shortestPath():
    return min((v[2] for v in PATHS.values))
    

Weights = orderVertices(Edges,activitiesDataframe=activitiesDataframe)

G = nx.Graph()
# each edge is a tuple of the form (node1, node2, {'weight': weight})
edges = [(k[0], k[1], {'weight': v}) for k, v in Weights.items()]

G.add_edges_from(edges)

pos = nx.spring_layout(G) # positions for all nodes

# nodes
nx.draw_networkx_nodes(G,pos,node_size=700)

# labels
nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

# edges
nx.draw_networkx_edges(G,pos,edgelist=edges, width=6)

# weights
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.show()


