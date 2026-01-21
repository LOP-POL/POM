import networkx as nx
import math
import matplotlib.pyplot as plt
# goodReceipts
# growingShelves
# plantDrying
# packing
# goodsIssue
# TransportCosts and TransportStations dep TransportWeight

# seeds  -> transported from goodReceipts to growingShelves
# plant -> growingShelves to plantDrying
# driedPlants -> plantDrying to packing
# seeds / plants / driedPlants -> go to goods issue if problem occurs
# boxes -> from goodsReceipt to packing 
# TransportCost / flow matrix between work centers

wc = {
    "designation":["wc1","wc2","wc3","wc4","wc5"],
    "name":["goodsReceipt","shelves","drying","packaging","issues"]
}

Edges = {
    "wc1":[2,5],
    "wc2":[4,5],
    "wc3":[4,5],
    "wc4":[5],
    "wc5":[0],
}

matrix = [
    #1,2,3,4,5
    [0,1,0,0,1],
    [0,0,1,0,1],
    [0,0,0,1,1],
    [0,0,0,0,1],
    [0,0,0,0,0],
]
Edges = {("wc1","wc2"):4, 
         ("wc1","wc5"):4,
         ("wc2","wc4"):4,
         ("wc1","wc2"):4}



# ---ASSUMPTIONS---
# Assume all workcenters have same space and fit in
# building.
# All material is transported in standard crates by
# forklift.
# Transportation costs are $1 to move between
# adjacent workcenters.
# Transportation cost depends on weight 
# Extra $1 for each workcenter in between

# Next Part
cities_by_population = [
"Berlin",
"Hamburg",
"Munich",
"Cologne",
"Frankfurt am Main",
"Düsseldorf",
"Stuttgart",
"Leipzig",
"Dortmund",
"Bremen",
"Essen",
"Dresden",
"Hanover",
"Nuremberg",
"Duisburg",
"Bochum",
"Wuppertal",
"Bielefeld",
"Bonn",
"Mannheim"
]

# longitude and latitiude
city_coordinates = {
    "Berlin": (52.5200, 13.4050),
    "Hamburg": (53.5500, 9.9833),
    "Munich": (48.1333, 11.5667),
    "Cologne": (50.9500, 6.9667),
    "Frankfurt am Main": (50.1167, 8.6833),
    "Düsseldorf": (51.2333, 6.7833),
    "Stuttgart": (48.7767, 9.1775),
    "Leipzig": (51.3333, 12.3833),
    "Dortmund": (51.5167, 7.4667),
    "Bremen": (53.0758, 8.8072),
    "Essen": (51.4500, 7.0167),
    "Dresden": (51.0500, 13.7400),
    "Hanover": (52.3667, 9.7167),
    "Nuremberg": (49.4500, 11.0833),
    "Duisburg": (51.4347, 6.7625),
    "Bochum": (51.4800, 7.2158),
    "Wuppertal": (51.2667, 7.1833),
    "Bielefeld": (52.0211, 8.5347),
    "Bonn": (50.7333, 7.1000),
    "Mannheim": (49.4878, 8.4661),
    "Karlsruhe": (49.0094, 8.4044)
}

cities_info = {
    "Berlin": {"coords": (52.5200, 13.4050), "distance_km": 527},
    "Hamburg": {"coords": (53.5500, 9.9833), "distance_km": 517},
    "Munich": {"coords": (48.1333, 11.5667), "distance_km": 253},
    "Cologne": {"coords": (50.9500, 6.9667), "distance_km": 238},
    "Frankfurt am Main": {"coords": (50.1167, 8.6833), "distance_km": 125},
    "Düsseldorf": {"coords": (51.2333, 6.7833), "distance_km": 272},
    "Stuttgart": {"coords": (48.7767, 9.1775), "distance_km": 62},
    "Leipzig": {"coords": (51.3333, 12.3833), "distance_km": 384},
    "Dortmund": {"coords": (51.5167, 7.4667), "distance_km": 287},
    "Bremen": {"coords": (53.0758, 8.8072), "distance_km": 453},
    "Essen": {"coords": (51.4500, 7.0167), "distance_km": 290},
    "Dresden": {"coords": (51.0500, 13.7400), "distance_km": 444},
    "Hanover": {"coords": (52.3667, 9.7167), "distance_km": 385},
    "Nuremberg": {"coords": (49.4500, 11.0833), "distance_km": 251},
    "Duisburg": {"coords": (51.4347, 6.7625), "distance_km": 294},
    "Bochum": {"coords": (51.4800, 7.2158), "distance_km": 288},
    "Wuppertal": {"coords": (51.2667, 7.1833), "distance_km": 266},
    "Bielefeld": {"coords": (52.0211, 8.5347), "distance_km": 337},
    "Bonn": {"coords": (50.7333, 7.1000), "distance_km": 214},
    "Mannheim": {"coords": (49.4878, 8.4661), "distance_km": 54},
    "Karlsruhe": {"coords": (49.0094, 8.4044), "distance_km": 0}
}

# driving_time_hours = distance_km / 80 - estimated driving times
estimated_driving_times = {
    "Berlin": 527/80,
    "Hamburg": 517/80,
    "Munich": 253/80,
    "Cologne": 238/80,
    "Frankfurt am Main": 125/80,
    "Düsseldorf": 272/80,
    "Stuttgart": 62/80,
    "Leipzig": 384/80,
    "Dortmund": 287/80,
    "Bremen": 453/80,
    "Essen": 290/80,
    "Dresden": 444/80,
    "Hanover": 385/80,
    "Nuremberg": 251/80,
    "Duisburg": 294/80,
    "Bochum": 288/80,
    "Wuppertal": 266/80,
    "Bielefeld": 337/80,
    "Bonn": 214/80,
    "Mannheim": 54/80
}


# Coordinates in decimal degrees
city_coords = {
    "Karlsruhe": (49.0094, 8.4044),
    "Berlin": (52.5200, 13.4050),
    "Hamburg": (53.5500, 9.9833),
    "Munich": (48.1333, 11.5667),
    "Cologne": (50.9500, 6.9667),
    "Frankfurt am Main": (50.1167, 8.6833),
    "Düsseldorf": (51.2333, 6.7833),
    "Stuttgart": (48.7767, 9.1775),
    "Leipzig": (51.3333, 12.3833),
    "Dortmund": (51.5167, 7.4667),
    "Bremen": (53.0758, 8.8072),
    "Essen": (51.4500, 7.0167),
    "Dresden": (51.0500, 13.7400),
    "Hanover": (52.3667, 9.7167),
    "Nuremberg": (49.4500, 11.0833),
    "Duisburg": (51.4347, 6.7625),
    "Bochum": (51.4800, 7.2158),
    "Wuppertal": (51.2667, 7.1833),
    "Bielefeld": (52.0211, 8.5347),
    "Bonn": (50.7333, 7.1000),
    "Mannheim": (49.4878, 8.4661)
}

def haversine(coord1, coord2):
    # Earth radius in km
    R = 6371.0
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Example: great circle distances from Karlsruhe
great_circle_from_karlsruhe = {
    city: haversine(city_coords["Karlsruhe"], coords)
    for city, coords in city_coords.items() if city != "Karlsruhe"
}

print(great_circle_from_karlsruhe)

# # Create graph
# G = nx.Graph()

# # Add central node
# G.add_node("Karlsruhe")

# # Add edges from Karlsruhe to each city
# for city, distance in distances_from_karlsruhe.items():
#     G.add_edge("Karlsruhe", city, weight=distance)

# # Spring layout
# pos = nx.spring_layout(G, seed=42)

# # Draw nodes
# plt.figure(figsize=(16, 16))
# nx.draw_networkx_nodes(
#     G, pos,
#     node_size=1500,
#     node_color="lightblue"
# )

# # Highlight Karlsruhe
# nx.draw_networkx_nodes(
#     G, pos,
#     nodelist=["Karlsruhe"],
#     node_size=2500,
#     node_color="orange"
# )

# # Draw edges
# nx.draw_networkx_edges(G, pos, width=2)

# # Draw node labels
# nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

# # Edge labels (distances)
# edge_labels = {
#     ("Karlsruhe", city): f"{dist} km"
#     for city, dist in distances_from_karlsruhe.items()
# }

# nx.draw_networkx_edge_labels(
#     G,
#     pos,
#     edge_labels=edge_labels,
#     font_size=9
# )

# plt.title("Distances from Karlsruhe to Major German Cities", fontsize=16)
# plt.axis("off")
# plt.show()

# Distances from Karlsruhe (km)
distances_from_karlsruhe = {
    "Berlin": 527,
    "Hamburg": 517,
    "Munich": 253,
    "Cologne": 238,
    "Frankfurt am Main": 125,
    "Düsseldorf": 272,
    "Stuttgart": 62,
    "Leipzig": 384,
    "Dortmund": 287,
    "Bremen": 453,
    "Essen": 290,
    "Dresden": 444,
    "Hanover": 385,
    "Nuremberg": 251,
    "Duisburg": 294,
    "Bochum": 288,
    "Wuppertal": 266,
    "Bielefeld": 337,
    "Bonn": 214,
    "Mannheim": 54
}

# Create graph
G = nx.Graph()
G.add_node("Karlsruhe")

for city, dist in distances_from_karlsruhe.items():
    G.add_edge("Karlsruhe", city, weight=dist)

# Normalize distances for plotting
max_distance = max(distances_from_karlsruhe.values())
scale = 10 / max_distance  # controls diagram size

# Assign positions
pos = {"Karlsruhe": (0, 0)}
num_cities = len(distances_from_karlsruhe)

for i, (city, dist) in enumerate(distances_from_karlsruhe.items()):
    angle = 2 * math.pi * i / num_cities
    radius = dist * scale
    pos[city] = (radius * math.cos(angle), radius * math.sin(angle))

# Plot
plt.figure(figsize=(16, 16))

nx.draw_networkx_nodes(G, pos, node_size=1400, node_color="lightblue")
nx.draw_networkx_nodes(G, pos, nodelist=["Karlsruhe"], node_size=2600, node_color="orange")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, font_size=9)

edge_labels = {
    ("Karlsruhe", city): f"{dist} km"
    for city, dist in distances_from_karlsruhe.items()
}

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Radial Distance-Based Layout from Karlsruhe", fontsize=16)
plt.axis("equal")
plt.axis("off")
plt.show()


# THE A* formula
# g(n) = exact cost from the start node to node n
# h(n) = heuristic estimate of the cost from node n to the goal
# f(n) = estimated total cost of the path through n





