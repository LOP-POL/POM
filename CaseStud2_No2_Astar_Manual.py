import math
import requests
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# 1. City coordinates
# -----------------------------

CITIES = {
    "Berlin": (52.5200, 13.4050),
    "Hamburg": (53.5511, 9.9937),
    "Munich": (48.1351, 11.5820),
    "Cologne": (50.9375, 6.9603),
    "Frankfurt": (50.1109, 8.6821),
    "Stuttgart": (48.7758, 9.1829),
    "Düsseldorf": (51.2277, 6.7735),
    "Leipzig": (51.3397, 12.3731),
    "Dortmund": (51.5136, 7.4653),
    "Essen": (51.4556, 7.0116),
    "Bremen": (53.0793, 8.8017),
    "Dresden": (51.0504, 13.7373),
    "Hanover": (52.3759, 9.7320),
    "Nuremberg": (49.4521, 11.0767),
    "Duisburg": (51.4344, 6.7623),
    "Bochum": (51.4818, 7.2197),
    "Wuppertal": (51.2562, 7.1508),
    "Bielefeld": (52.0302, 8.5325),
    "Bonn": (50.7374, 7.0982),
    "Münster": (51.9607, 7.6261),
    "Karlsruhe": (49.0094, 8.4044),
}

CITY_NAMES = list(CITIES.keys())

# -----------------------------
# 2. Haversine heuristic
# -----------------------------

def haversine(a, b):
    R = 6371.0
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def heuristic(u, v):
    return haversine(CITIES[u], CITIES[v])

# -----------------------------
# 3. Query OSRM distance matrix
# -----------------------------

base_url = "http://router.project-osrm.org/table/v1/driving/"
coords = ";".join(f"{lon},{lat}" for lat, lon in CITIES.values())
url = f"{base_url}{coords}?annotations=distance"

print("Querying OSRM distance matrix...")
response = requests.get(url)
response.raise_for_status()
data = response.json()

distances = data["distances"]  # meters

# -----------------------------
# 4. Build NetworkX graph
# -----------------------------

G = nx.Graph()

for i, city_from in enumerate(CITY_NAMES):
    for j, city_to in enumerate(CITY_NAMES):
        if i != j:
            G.add_edge(
                city_from,
                city_to,
                weight=distances[i][j] / 1000.0  # km
            )

# -----------------------------
# 5. Run A* search
# -----------------------------

SOURCE = "Berlin"
TARGET = "Munich"

path = nx.astar_path(
    G,
    source=SOURCE,
    target=TARGET,
    heuristic=heuristic,
    weight="weight"
)

path_length = nx.astar_path_length(
    G,
    source=SOURCE,
    target=TARGET,
    heuristic=heuristic,
    weight="weight"
)

print("A* Route:", " → ".join(path))
print(f"Total distance: {path_length:.2f} km")

# -----------------------------
# 6. Visualization
# -----------------------------

# Use geographic positions for layout
pos = {city: (CITIES[city][1], CITIES[city][0]) for city in CITIES}

plt.figure(figsize=(10, 12))

# Draw all nodes and edges
nx.draw(
    G,
    pos,
    node_size=300,
    node_color="lightblue",
    edge_color="lightgray",
    with_labels=True,
    font_size=8
)

# Highlight A* path
path_edges = list(zip(path[:-1], path[1:]))

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=path,
    node_color="red",
    node_size=400
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=path_edges,
    edge_color="red",
    width=2.5
)

# Add edge labels for the A* path showing the distance (km)
path_edge_labels = {(u, v): f"{G[u][v]['weight']:.1f} km" for u, v in path_edges}
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=path_edge_labels,
    font_color="red",
    font_size=8
)

plt.title(f"A* Route from {SOURCE} to {TARGET}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()
