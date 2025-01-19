import math
import numpy as np

from scipy.sparse.csgraph import floyd_warshall


def rotate(point, center, angle):
    radians = math.radians(angle)
    x, y = point
    cx, cy = center
    return (
        cx + (x - cx) * math.cos(radians) - (y - cy) * math.sin(radians), 
        cy + (x - cx) * math.sin(radians) + (y - cy) * math.cos(radians)
    )


def calculate_angle(center):
    cx, cy = center
    return math.degrees(math.atan2(-cy, -cx))


def calculate_props(adjacency_matrix):
    n = adjacency_matrix.shape[0]
    sh_path = floyd_warshall(adjacency_matrix, directed=False)
    d = np.max(sh_path[sh_path != np.inf])
    ad = np.sum(sh_path[sh_path != np.inf]) / (n * (n - 1))
    s = np.max(np.sum(adjacency_matrix, axis=1))
    c = np.sum(adjacency_matrix) // 2
    t = (2 * ad) / s
    return n, d, ad, s, c, t

def print_topological_properties(adjacency_matrix):
    n, d, ad, s, c, t = calculate_props(adjacency_matrix)
    print(f"""
    N: {n}
    D: {d}
    aD: {ad}
    S: {s}
    C: {c}
    T: {t}
    """)

def print_props_table(max_clusters_number, calc_adj_matrix_fun):
    table_data = [["N", "D", "aD", "S", "C", "T"]]
    for i in range(1, max_clusters_number + 1):
        table_data.append([*calculate_props(calc_adj_matrix_fun(i))])
    
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(*table_data[0]))
    for row in table_data[1:]:
        print("{:<10} {:<10} {:<10.2f} {:<10} {:<10} {:<10.2f}".format(*row))
