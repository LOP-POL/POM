import pandas as pd
import numpy as np

# Data extraction
data_a = [
    (1, 0, 100), (2, 2, 300), (1, 5, 250), (3, 5, 100), (1, 6, 400),
    (3, 3, 100), (5, 12, 300), (6, 12, 100), (6, 14, 600), (10, 11, 200),
    (12, 13, 100), (10, 15, 400), (14, 1, 300), (13, 3, 200), (14, 3, 100)
]
data_b = [
    (2, 0, 300), (1, 3, 400), (2, 5, 200), (0, 7, 400), (2, 7, 300),
    (5, 11, 500), (7, 11, 600), (6, 13, 200), (11, 12, 200), (11, 14, 400),
    (12, 15, 300), (12, 0, 200), (14, 0, 100), (13, 2, 600)
]
data_c = [
    (0, 1, 100), (3, 1, 500), (2, 4, 50), (0, 5, 400), (3, 6, 100),
    (5, 9, 500), (5, 15, 100), (7, 13, 300), (7, 15, 300), (10, 13, 400),
    (11, 15, 100), (12, 11, 100), (10, 2, 200), (13, 1, 400), (15, 0, 500)
]

cols = ['x', 'y', 'demand']
df_a = pd.DataFrame(data_a, columns=cols)
df_b = pd.DataFrame(data_b, columns=cols)
df_c = pd.DataFrame(data_c, columns=cols)

def get_stats(df, equal_demand=False):
    if equal_demand:
        w = np.ones(len(df))
    else:
        w = df['demand'].values
    
    total_w = w.sum()
    cog_x = (df['x'] * w).sum() / total_w
    cog_y = (df['y'] * w).sum() / total_w
    
    return cog_x, cog_y, total_w

# Function to calculate costs
def calculate_total_cost(df, warehouse_coords, actual_demands=True):
    # Fixed cost
    n_warehouses = len(warehouse_coords)
    fixed_cost = n_warehouses * 100000
    
    # Capacity cost
    total_demand = df['demand'].sum()
    capacity_cost = total_demand * 1000
    
    # Delivery cost
    # For each customer, assign to nearest warehouse
    delivery_cost = 0
    demands = df['demand'].values if actual_demands else [df['demand'].mean()]*len(df)
    
    for i, row in df.iterrows():
        dists = [np.sqrt((row['x']-wx)**2 + (row['y']-wy)**2) for wx, wy in warehouse_coords]
        min_dist = min(dists)
        # 0.10 € per km and ton -> 0.0001 € per km and kg
        delivery_cost += min_dist * demands[i] * 0.0001
        
    return fixed_cost, capacity_cost, delivery_cost

# Task E: Equal Demands
print("--- Task E: Equal Demands ---")
areas = {'A': df_a, 'B': df_b, 'C': df_c}
for name, df in areas.items():
    cx, cy, _ = get_stats(df, equal_demand=True)
    f, c, d = calculate_total_cost(df, [(cx, cy)], actual_demands=False)
    print(f"Area {name}: CoG=({cx:.2f}, {cy:.2f}), Total Demand={df['demand'].sum()}, Costs: Fixed={f}, Cap={c}, Del={d:.4f}")

# Task F: Actual Demands
print("\n--- Task F: Actual Demands ---")
for name, df in areas.items():
    cx, cy, _ = get_stats(df, equal_demand=False)
    f, c, d = calculate_total_cost(df, [(cx, cy)], actual_demands=True)
    print(f"Area {name}: CoG=({cx:.2f}, {cy:.2f}), Total Demand={df['demand'].sum()}, Costs: Fixed={f}, Cap={c}, Del={d:.4f}")

# Comparison Solution: 2 warehouses in Area A (Task F)
# Cluster A into two (North and South)
df_a_n = df_a[df_a['y'] > 8]
df_a_s = df_a[df_a['y'] <= 8]
cx_n, cy_n, _ = get_stats(df_a_n)
cx_s, cy_s, _ = get_stats(df_a_s)
f2, c2, d2 = calculate_total_cost(df_a, [(cx_n, cy_n), (cx_s, cy_s)], actual_demands=True)
print(f"\nArea A (2 warehouses): CoG_N=({cx_n:.2f}, {cy_n:.2f}), CoG_S=({cx_s:.2f}, {cy_s:.2f})")
print(f"Costs: Fixed={f2}, Cap={c2}, Del={d2:.4f}")