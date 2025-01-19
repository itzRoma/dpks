import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from util import print_props_table, print_topological_properties

SUBCLASTER_PROCESSORS = 10

def create_adjacency_matrix(num_clusters):
    n = SUBCLASTER_PROCESSORS * num_clusters
    adjacency_matrix = np.zeros((n, n), dtype=int)

    for cluster in range(num_clusters):
        base = cluster * SUBCLASTER_PROCESSORS

        connections = [
            (1, 2), (1, 3), (1, 6),
            (2, 7), (2, 8),
            (3, 4), (3, 9), 
            (4, 5), (4, 8),
            (5, 6), (5, 7),
            (6, 10),
            (7, 9),
            (8, 10),
            (9, 10)
        ]
        for u, v in connections:
            adjacency_matrix[base + u - 1, base + v - 1] = 1

        if cluster < num_clusters - 1:
            adjacency_matrix[base, base + SUBCLASTER_PROCESSORS] = 1
            adjacency_matrix[base + 5, base + SUBCLASTER_PROCESSORS + 2] = 1
            adjacency_matrix[base + 9, base + SUBCLASTER_PROCESSORS + 8] = 1
            adjacency_matrix[base + 1, base + SUBCLASTER_PROCESSORS + 1] = 1
            adjacency_matrix[base + 7, base + SUBCLASTER_PROCESSORS + 6] = 1

    if (num_clusters > 1):
        adjacency_matrix[2, SUBCLASTER_PROCESSORS * (num_clusters - 1) + 5] = 1

    return adjacency_matrix + adjacency_matrix.T

def show_graph(adjacency_matrix, n_clusters):
    graph = nx.Graph()
    n = adjacency_matrix.shape[0]

    graph.add_nodes_from(range(1, n + 1))
    edges = [(i + 1, j + 1) for i in range(n) for j in range(i + 1, n) if adjacency_matrix[i, j]]
    graph.add_edges_from(edges)

    pos = {}
    for cluster in range(n_clusters):
        base_x = cluster * (SUBCLASTER_PROCESSORS + 3)
        base_y = 0
        initial_positions = [
            (base_x, base_y + 2),
            (base_x, base_y + 1),
            (base_x - 5, base_y),
            (base_x - 2, base_y),
            (base_x + 2, base_y),
            (base_x + 5, base_y),
            (base_x - 1, base_y - 1),
            (base_x + 1, base_y - 1),
            (base_x - 2, base_y - 2),
            (base_x + 2, base_y - 2)
        ]
        for i, pos_node in enumerate(initial_positions):
            pos[cluster * SUBCLASTER_PROCESSORS + i + 1] = pos_node

    plt.figure(figsize=(18, 3))
    nx.draw(graph, pos, with_labels=True, node_size=300, node_color="skyblue", font_weight="bold")

    if n_clusters > 1:
        x1, y1 = pos[3]
        x2, y2 = pos[n_clusters * SUBCLASTER_PROCESSORS - 4]
        mid_x, mid_y = (x1 + x2) / 64, (y1 + y2) / 64 + 5
        mid_x_2, mid_y_2 = (x1 + x2) - mid_x, (y1 + y2) / 64 + 5

        curve_x = [x1, mid_x, mid_x_2, x2]
        curve_y = [y1, mid_y, mid_y_2, y2]
        plt.plot(curve_x, curve_y, color="blue")

    plt.show()

n = int(input("Enter the number of clusters: "))
adjacency_matrix = create_adjacency_matrix(n)
print_topological_properties(adjacency_matrix)
show_graph(adjacency_matrix, n)

# print_props_table(10, create_adjacency_matrix)
