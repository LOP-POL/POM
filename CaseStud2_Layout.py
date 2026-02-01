import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

work_centers = {
    "wc1": "goodsReceipts",
    "wc2": "growingShelves",
    "wc3": "plantDrying",
    "wc4": "packing",
    "wc5": "goodsIssue"
}

transport_costs_wc = {
    ("wc1", "wc2"): 10,  # seeds
    ("wc2", "wc3"): 18,  # fresh plants
    ("wc3", "wc4"): 14,  # dried plants
    ("wc1", "wc4"): 12,  # boxes
    ("wc4","wc5"):  15,  #boxes break maybe 

    # exception flows
    ("wc1", "wc5"): 16,  # rejected seeds
    ("wc2", "wc5"): 20,  # failed plants
    ("wc3", "wc5"): 17   # failed dried plants
}


G = nx.Graph()

# add nodes
G.add_nodes_from(["wc1", "wc2", "wc3", "wc4", "wc5"])

# add weighted edges
for (u, v), w in transport_costs_wc.items():
    G.add_edge(u, v, weight=w)

pos = {
    "wc5": (0, 0),           # wc5 in the middle
    "wc1": (0.5, 0.866),     # top-right of hexagon
    "wc2": (-0.5, 0.866),    # top-left of hexagon
    "wc3": (-0.5, -0.866),   # bottom-left of hexagon
    "wc4": (0.5, -0.866)     # bottom-right of hexagon
}
nx.draw_networkx_nodes(
    G=G,
    pos=pos,
    node_size=1500,
    node_color="lightblue"
)

 # Draw edges
nx.draw_networkx_edges(G, pos, width=2)

# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

# Draw edge labels with weights
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels)


labels = ["wc1", "wc2", "wc3", "wc4", "wc5"]

flow_matrix = pd.DataFrame(
    np.zeros((5, 5), dtype=int),
    index=labels,
    columns=labels
)

for (i, j), w in transport_costs_wc.items():
    flow_matrix.loc[i, j] = round(w,2)

print(flow_matrix.head())

plt.show()

