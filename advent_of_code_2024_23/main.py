import time
from itertools import combinations
import networkx as nx
from functools import lru_cache


@lru_cache(maxsize=None)
def read_connections(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


# Build the graph as an adjacency list
def build_graph(connections):
    graph = {}
    for conn in connections:
        a, b = conn.split('-')
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


# Find all triangles
def find_triangles(graph):
    triangles = set()
    for a, b, c in combinations(graph.keys(), 3):
        if b in graph[a] and c in graph[a] and c in graph[b]:
            triangles.add(tuple(sorted([a, b, c])))
    return triangles


# Filter triangles where at least one node starts with 't'
def filter_triangles_with_t(triangles):
    return len([triangle for triangle in triangles if any(node.startswith('t') for node in triangle)])


# Build the graph using NetworkX
def build_graph_2(connections):
    graph = nx.Graph()
    for conn in connections:
        a, b = conn.split('-')
        graph.add_edge(a, b)
    return graph


@lru_cache(maxsize=None)
def find_largest_clique(graph):
    cliques = list(nx.find_cliques(graph))
    return max(cliques, key=len)


# Generate the password from the largest clique
def generate_password(clique):
    return ','.join(sorted(clique))


def process_input(file_path):
    start_time = time.time()  # Start timing the execution
    connections = read_connections(file_path)
    graph = build_graph(connections)
    triangles = find_triangles(graph)
    print("Total Triangles with 't':", filter_triangles_with_t(triangles))
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds\n")

    start_time = time.time()  # Start timing the execution
    graph = build_graph_2(connections)
    largest_clique = find_largest_clique(graph)
    password = generate_password(largest_clique)
    print("Password to LAN Party:", password)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds\n")


if __name__ == "__main__":
    for file in ['example_1.txt', 'input.txt']:
        process_input(file)
