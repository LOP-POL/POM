import os
import networkx as nx
import math
import pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patheffects as patheffects
import numpy as np

# --- 1. SETTINGS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_file = os.path.join(script_dir, "autobahn_graph.pickle")

cities = {
    "Berlin": (52.5200, 13.4050), "Hamburg": (53.5511, 9.9937),
    "Munich": (48.1351, 11.5820), "Cologne": (50.9375, 6.9603),
    "Frankfurt": (50.1109, 8.6821), "Stuttgart": (48.7758, 9.1821),
    "Düsseldorf": (51.2277, 6.7735), "Leipzig": (51.3397, 12.3731),
    "Dortmund": (51.5136, 7.4653), "Essen": (51.4556, 7.0116),
    "Bremen": (53.0793, 8.8017), "Dresden": (51.0504, 13.7373),
    "Hanover": (52.3759, 9.7320), "Nuremberg": (49.4521, 11.0767),
    "Duisburg": (51.4344, 6.7623), "Bochum": (51.4818, 7.2162),
    "Wuppertal": (51.2562, 7.1508), "Bielefeld": (52.0204, 8.5322),
    "Bonn": (50.7374, 7.0982), "Münster": (51.9607, 7.6261)
}
karlsruhe_coords = (49.0069, 8.4037)

def haversine(c1, c2):
    lat1, lon1 = c1
    lat2, lon2 = c2
    r = 6371 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlon/2)**2
    return 2 * r * math.asin(math.sqrt(a))

# --- 2. LOAD ---
with open(cache_file, 'rb') as f:
    G = pickle.load(f)

pos = {n: (data['pos'][1], data['pos'][0]) for n, data in G.nodes(data=True)}
start_node = min(G.nodes, key=lambda n: haversine(karlsruhe_coords, G.nodes[n]['pos']))

# --- 3. PLOTTING ---
fig, ax = plt.subplots(figsize=(14, 16))

print("Drawing infrastructure layer (this may take a moment)...")
# Removed zorder from the function call to fix the TypeError
nx.draw_networkx_edges(G, pos, ax=ax, edge_color='black', width=0.1, alpha=1.0)

colors = cm.gist_rainbow(np.linspace(0, 1, len(cities)))

print("Calculating and drawing paths...")
for (city, coord), color in zip(cities.items(), colors):
    end_node = min(G.nodes, key=lambda n: haversine(coord, G.nodes[n]['pos']))
    try:
        path = nx.astar_path(G, start_node, end_node, 
                             heuristic=lambda u, v: haversine(G.nodes[u]['pos'], G.nodes[v]['pos']),
                             weight='weight')
        path_edges = list(zip(path, path[1:]))
        
        # We draw the glow and path. Matplotlib naturally layers things in the order they are called.
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax, edge_color='white', width=3.8)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax, edge_color=[color], width=2.4)
        
        # Scatter and text are always drawn on top of edges by default
        ax.scatter(coord[1], coord[0], color=[color], s=120, edgecolors='black', linewidth=1.5, zorder=10)
        
        txt = ax.text(coord[1] + 0.12, coord[0] + 0.05, city, fontsize=10, fontweight='bold', zorder=11)
        txt.set_path_effects([patheffects.withStroke(linewidth=3, foreground='white')])

    except Exception as e:
        continue

# Karlsruhe Marker
ax.scatter(karlsruhe_coords[1], karlsruhe_coords[0], color='gold', marker='*', s=800, edgecolors='black', zorder=15)
k_txt = ax.text(karlsruhe_coords[1] + 0.15, karlsruhe_coords[0] - 0.15, "KARLSRUHE", 
                 fontsize=12, fontweight='black', color='black', zorder=16)
k_txt.set_path_effects([patheffects.withStroke(linewidth=4, foreground='white')])

ax.set_title("Shortest Autobahn Routes from Karlsruhe\n(A* Search Algorithm)", fontsize=20, fontweight='bold', pad=20)
plt.axis('off')

output_file = os.path.join(script_dir, "final_labeled_autobahn_map.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Success! Map saved to: {output_file}")
plt.show()