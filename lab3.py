import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math

from util import print_topological_properties

SUBCLASTER_PROCESSORS = 8

def create_adjacency_matrix(num_clusters, grid_width):
    num_clusters_vertical = (num_clusters + grid_width - 1) // grid_width
    n = SUBCLASTER_PROCESSORS * num_clusters
    adjacency_matrix = np.zeros((n, n), dtype=int)

    for cluster in range(num_clusters):
        base = cluster * SUBCLASTER_PROCESSORS

        connections = [
            (1, 2), (1, 3), (1, 5), (1, 8),
            (2, 4), (2, 6), (2, 7),
            (3, 4), (3, 6), (3, 7),
            (4, 5), (4, 8),
            (5, 6), (5, 7),
            (6, 8),
            (7, 8)
        ]
        for u, v in connections:
            adjacency_matrix[base + u - 1, base + v - 1] = 1

    for cluster in range(num_clusters):
        row, col = divmod(cluster, grid_width)
        base = cluster * SUBCLASTER_PROCESSORS

        if col < grid_width - 1 and cluster + 1 < num_clusters:
            right_base = base + SUBCLASTER_PROCESSORS
            adjacency_matrix[base + 1, right_base] = 1
            adjacency_matrix[base + 3, right_base + 2] = 1
            adjacency_matrix[base + 5, right_base + 4] = 1
            adjacency_matrix[base + 7, right_base + 6] = 1

        if row < num_clusters_vertical - 1 and cluster + grid_width < num_clusters:
            bottom_base = (cluster + grid_width) * SUBCLASTER_PROCESSORS
            adjacency_matrix[base + 2, bottom_base] = 1
            adjacency_matrix[base + 3, bottom_base + 1] = 1
            adjacency_matrix[base + 6, bottom_base + 4] = 1
            adjacency_matrix[base + 7, bottom_base + 5] = 1

        if row > 0 and col > 0:
            top_left_base = (cluster - grid_width - 1) * SUBCLASTER_PROCESSORS
            adjacency_matrix[base, top_left_base + 3] = 1
            adjacency_matrix[base + 4, top_left_base + 7] = 1

        if row > 0 and col < grid_width - 1 and cluster - grid_width + 1 < num_clusters:
            top_right_base = (cluster - grid_width + 1) * SUBCLASTER_PROCESSORS
            adjacency_matrix[base + 1, top_right_base + 2] = 1
            adjacency_matrix[base + 5, top_right_base + 6] = 1

    return adjacency_matrix + adjacency_matrix.T



def show_graph(adjacency_matrix, num_clusters, grid_width):
    graph = nx.Graph()
    n = adjacency_matrix.shape[0]

    graph.add_nodes_from(range(1, n + 1))
    edges = [(i + 1, j + 1) for i in range(n) for j in range(i + 1, n) if adjacency_matrix[i, j]]
    graph.add_edges_from(edges)

    intra_cluster_edges = []
    inter_cluster_edges = []
    for cluster in range(num_clusters):
        base = cluster * SUBCLASTER_PROCESSORS
        cluster_nodes = set(range(base + 1, base + SUBCLASTER_PROCESSORS + 1))
        for u, v in edges:
            if u in cluster_nodes and v in cluster_nodes:
                intra_cluster_edges.append((u, v))
            elif u in cluster_nodes or v in cluster_nodes:
                inter_cluster_edges.append((u, v))

    pos = {}
    for cluster in range(num_clusters):
        base_x = (cluster % grid_width) * SUBCLASTER_PROCESSORS
        base_y = -(cluster // grid_width) * SUBCLASTER_PROCESSORS / 2
        initial_positions = [
            (base_x - 2, base_y + 1),
            (base_x, base_y + 1),
            (base_x - 2, base_y - 1),
            (base_x, base_y - 1),
            (base_x - 1, base_y + 2),
            (base_x + 1, base_y + 2),
            (base_x - 1, base_y),
            (base_x + 1, base_y)
        ]
        for i, pos_node in enumerate(initial_positions):
            pos[cluster * SUBCLASTER_PROCESSORS + i + 1] = pos_node

    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(graph, pos, node_size=300, node_color="skyblue")
    nx.draw_networkx_labels(graph, pos, font_weight="bold")
    nx.draw_networkx_edges(graph, pos, edgelist=intra_cluster_edges, edge_color="black", width=2, label="Intra-cluster")
    nx.draw_networkx_edges(graph, pos, edgelist=inter_cluster_edges, edge_color="blue", style="dashed", width=2, label="Inter-cluster")
    plt.legend(loc="best")
    plt.show()


n = int(input("Enter the number of clusters: "))
grid_width = int(math.sqrt(n))
adjacency_matrix = create_adjacency_matrix(n, grid_width)
print_topological_properties(adjacency_matrix)
show_graph(adjacency_matrix, n, grid_width)
