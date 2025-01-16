import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from util import rotate, calculate_angle, print_topological_properties


SUBCLASTER_PROCESSORS = 6


def create_adjacency_matrix(num_clusters):
    n = SUBCLASTER_PROCESSORS * num_clusters
    adjacency_matrix = np.zeros((n, n), dtype=int)

    for cluster in range(num_clusters):
        base = cluster * SUBCLASTER_PROCESSORS

        # inner cluster connections
        connections = [
            (1, 2), (1, 4), (1, 6),
            (2, 3), (2, 5),
            (3, 4),
            (4, 5),
            (5, 6)
        ]
        for u, v in connections:
            adjacency_matrix[base + u - 1, base + v - 1] = 1

        # n-n
        for i in range(SUBCLASTER_PROCESSORS):
            if cluster < num_clusters - 1:
                adjacency_matrix[base + i, base + SUBCLASTER_PROCESSORS + i] = 1
            else:
                adjacency_matrix[base + i, i] = 1

        # 1-1, 2-2
        if num_clusters >= 3:
            try:
                adjacency_matrix[base, base + SUBCLASTER_PROCESSORS * 2] = 1
                adjacency_matrix[base + 1, base + SUBCLASTER_PROCESSORS * 2 + 1] = 1
            except IndexError:
                if cluster not in (num_clusters - 2, num_clusters - 1):
                    adjacency_matrix[base, base + SUBCLASTER_PROCESSORS] = 1
                    adjacency_matrix[base + 1, base + SUBCLASTER_PROCESSORS + 1] = 1

        # 2-1
        if cluster < num_clusters - 1:
            adjacency_matrix[base + 1, base + SUBCLASTER_PROCESSORS] = 1
        else:
            adjacency_matrix[base + 1, 0] = 1

        # 3-6
        if cluster < num_clusters - 1:
            adjacency_matrix[base + 2, base + SUBCLASTER_PROCESSORS + 5] = 1
        else:
            adjacency_matrix[base + 2, 5] = 1

        # 5-4
        if cluster < num_clusters - 1:
            adjacency_matrix[base + 3, base + SUBCLASTER_PROCESSORS + 4] = 1
        else:
            adjacency_matrix[base + 3, 4] = 1

    return adjacency_matrix + adjacency_matrix.T


def show_graph(adjacency_matrix, n_clusters):
    graph = nx.Graph()
    n = adjacency_matrix.shape[0]

    graph.add_nodes_from(range(1, n + 1))
    edges = [(i + 1, j + 1) for i in range(n) for j in range(i + 1, n) if adjacency_matrix[i, j]]
    graph.add_edges_from(edges)

    pos = {}
    angle_offset = 2 * np.pi / n_clusters
    for cluster in range(n_clusters):
        angle = angle_offset * cluster
        base_x, base_y = np.cos(angle) * n_clusters, np.sin(angle) * n_clusters
        center = (base_x, base_y)
        rotation_angle = calculate_angle(center) - 90

        initial_positions = [
            (base_x - 1, base_y + 2),
            (base_x + 1, base_y + 2),
            (base_x + 2, base_y),
            (base_x + 1, base_y - 2),
            (base_x - 1, base_y - 2),
            (base_x - 2, base_y),
        ]
        rotated_positions = [rotate(p, center, rotation_angle) for p in initial_positions]
        for i, pos_node in enumerate(rotated_positions):
            pos[cluster * SUBCLASTER_PROCESSORS + i + 1] = pos_node

    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_size=300, node_color="skyblue", font_weight="bold")
    plt.show()


n = int(input("Enter the number of clusters: "))
adjacency_matrix = create_adjacency_matrix(n)
print_topological_properties(adjacency_matrix)
show_graph(adjacency_matrix, n)
