import time
import networkx as nx

begin = time.time()

###

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def build_graph(grid: dict, ignore_slopes: bool):
	result = nx.DiGraph()
	for p in grid:
		for *delta, direction in [(0,1,"v"), (1,0,">"), (-1,0,"<"), (0,-1,"^")]:
			n = add_tuples(p, delta)
			if n not in grid:
				continue
			if grid[n] == ".":
				result.add_edge(p, n, weight=1)
			if ignore_slopes or grid[n] == direction:
				result.add_edge(p, n, weight=1)
	return result

def edge_contraction(graph):
	marked_for_removal = [node for node in graph.nodes() if len(graph[node]) == 2]
	for node in marked_for_removal:
		n1, n2 = list(graph[node])
		new_weight = graph[node][n1]["weight"] + graph[node][n2]["weight"]
		graph.add_edge(n1, n2, weight=new_weight)
		graph.remove_node(node)
	return graph

seen = set()
def dfs_longest_path(node: tuple, target: tuple, neighbours: dict) -> int:
	if node == target:
		return 0
	current_max = 0
	seen.add(node)
	for n, weight in neighbours[node]:
		if n in seen:
			continue
		current_max = max(current_max, weight + dfs_longest_path(n, target, neighbours))
	seen.remove(node)
	return current_max


hiking_map = {}
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		for col, char in enumerate(line.strip()):
			if char == "#":
				continue
			hiking_map[(col, row)] = char

top_row_tile, bottom_row_tile = min(hiking_map), max(hiking_map)
p1_graph = build_graph(hiking_map, False)
p2_graph = edge_contraction(build_graph(hiking_map, True).to_undirected())

p2_neighbours = {node: [(n, p2_graph[node][n]["weight"]) for n in p2_graph[node]]
						for node in p2_graph.nodes()}
p1_neighbours = {node: [(n, weight) for n, weight in neighbours if nx.has_path(p1_graph, node, n)]
						for node, neighbours in p2_neighbours.items()}

print(f"Part 1: {dfs_longest_path(top_row_tile, bottom_row_tile, p1_neighbours)}")
print(f"Part 2: {dfs_longest_path(top_row_tile, bottom_row_tile, p2_neighbours)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
