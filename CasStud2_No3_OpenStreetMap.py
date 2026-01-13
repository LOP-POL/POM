import osmnx as ox
import networkx as nx
import math
import matplotlib.pyplot as plt
import pickle
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
ox.settings.log_console = False
ox.settings.use_cache = True

# 20 largest German cities
GERMAN_CITIES = {
    "Berlin": "Berlin, Germany",
    "Hamburg": "Hamburg, Germany",
    "Munich": "Munich, Germany",
    "Cologne": "Cologne, Germany",
    "Frankfurt": "Frankfurt am Main, Germany",
    "Düsseldorf": "Düsseldorf, Germany",
    "Stuttgart": "Stuttgart, Germany",
    "Leipzig": "Leipzig, Germany",
    "Dortmund": "Dortmund, Germany",
    "Bremen": "Bremen, Germany",
    "Essen": "Essen, Germany",
    "Dresden": "Dresden, Germany",
    "Hanover": "Hanover, Germany",
    "Nuremberg": "Nuremberg, Germany",
    "Duisburg": "Duisburg, Germany",
    "Bochum": "Bochum, Germany",
    "Wuppertal": "Wuppertal, Germany",
    "Bielefeld": "Bielefeld, Germany",
    "Bonn": "Bonn, Germany",
    "Mannheim": "Mannheim, Germany",
    "Karlsruhe": "Karlsruhe, Germany"
}

HIGHWAY_TYPES = {
    "motorway", "motorway_link",
    "trunk", "trunk_link"
}

CACHE_FILE = "germany_highway_graph.pkl"

# -----------------------------
# Haversine Distance
# -----------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def haversine_heuristic(u, v, G):
    return haversine_distance(
        G.nodes[u]["y"], G.nodes[u]["x"],
        G.nodes[v]["y"], G.nodes[v]["x"]
    )

# -----------------------------
# Build Highway-Only Graph (Optimized)
# -----------------------------
def load_highway_graph(force_reload=False):
    cache_path = Path(CACHE_FILE)
    
    # Try to load from cache
    if cache_path.exists() and not force_reload:
        print(f"Loading cached graph from {CACHE_FILE}...")
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    
    print("Downloading Germany highway network...")
    print("This will take 5-20 minutes on first run, but will be cached for future use.")
    print("Strategy: Download motorways only from larger regions")
    
    # Download motorways for major German states (faster than whole country at once)
    states = [
        "Baden-Württemberg, Germany",
        "Bayern, Germany", 
        "Berlin, Germany",
        "Brandenburg, Germany",
        "Bremen, Germany",
        "Hamburg, Germany",
        "Hessen, Germany",
        "Mecklenburg-Vorpommern, Germany",
        "Niedersachsen, Germany",
        "Nordrhein-Westfalen, Germany",
        "Rheinland-Pfalz, Germany",
        "Saarland, Germany",
        "Sachsen, Germany",
        "Sachsen-Anhalt, Germany",
        "Schleswig-Holstein, Germany",
        "Thüringen, Germany"
    ]
    
    # Custom filter for only motorways and trunks
    custom_filter = '["highway"~"motorway|motorway_link|trunk|trunk_link"]'
    
    graphs = []
    for i, state in enumerate(states, 1):
        print(f"  Downloading {state} ({i}/{len(states)})...")
        try:
            G_state = ox.graph_from_place(
                state,
                network_type="drive",
                custom_filter=custom_filter,
                simplify=True
            )
            graphs.append(G_state)
        except Exception as e:
            print(f"    Warning: Could not download {state}: {e}")
    
    # Merge all graphs
    print("Merging state graphs...")
    G = nx.compose_all(graphs)
    
    # Remove isolated components (keep only largest connected component)
    print("Cleaning up graph...")
    if not nx.is_strongly_connected(G):
        largest_cc = max(nx.strongly_connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()
    
    print(f"Final graph has {len(G.nodes)} nodes and {len(G.edges)} edges")
    
    # Cache the graph
    print(f"Caching graph to {CACHE_FILE}...")
    with open(cache_path, "wb") as f:
        pickle.dump(G, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("Download complete! Future runs will load instantly from cache.")
    return G

# -----------------------------
# A* Shortest Highway Path
# -----------------------------
def shortest_highway_path(start_city, end_city, G):
    if start_city not in GERMAN_CITIES or end_city not in GERMAN_CITIES:
        raise ValueError("City must be one of the 20 largest German cities.")

    print(f"Finding route from {start_city} to {end_city}...")
    
    start_point = ox.geocode(GERMAN_CITIES[start_city])
    end_point = ox.geocode(GERMAN_CITIES[end_city])

    start_node = ox.nearest_nodes(G, start_point[1], start_point[0])
    end_node = ox.nearest_nodes(G, end_point[1], end_point[0])

    print("Running A* pathfinding...")
    path = nx.astar_path(
        G,
        start_node,
        end_node,
        heuristic=lambda u, v: haversine_heuristic(u, v, G),
        weight="length"
    )

    distance_m = sum(
        G[u][v][0].get("length", 0)
        for u, v in zip(path[:-1], path[1:])
    )

    return path, distance_m / 1000  # km

# -----------------------------
# Visualization
# -----------------------------
def plot_route(G, route, start_city, end_city):
    fig, ax = ox.plot_graph_route(
        G,
        route,
        route_color="red",
        route_linewidth=4,
        node_size=0,
        bgcolor="white",
        show=False,
        close=False
    )
    ax.set_title(
        f"Shortest Highway Route: {start_city} → {end_city}",
        fontsize=14
    )
    plt.show()

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    # Load graph (will use cache if available)
    G = load_highway_graph(force_reload=False)

    start = "Karlsruhe"
    end = "Berlin"

    route, distance_km = shortest_highway_path(start, end, G)

    print(f"\nShortest highway distance from {start} to {end}: {distance_km:.1f} km")

    plot_route(G, route, start, end)