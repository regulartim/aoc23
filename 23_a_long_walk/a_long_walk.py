import time
import networkx as nx

begin = time.time()

###

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def build_graph(grid, ignore_slopes):
	result = nx.DiGraph()
	for p in grid:
		neighbour_count = 0
		for *delta, direction in [(0,1,"v"), (1,0,">"), (-1,0,"<"), (0,-1,"^")]:
			n = add_tuples(p, delta)
			if n not in grid:
				continue
			neighbour_count += 1
			if grid[n] == ".":
				result.add_edge(p, n)
			if ignore_slopes or grid[n] == direction:
				result.add_edge(p, n)
	return result

def find_junctions(graph) -> list:
	return [node for node in graph.nodes() if len(list(graph.neighbors(node))) > 2]

def find_adjecent_junctions(graph, node: tuple, junctions: set) -> list:
	result = []
	for neighbor in graph.neighbors(node):
		seen = {node, neighbor}
		current = neighbor
		while current not in junctions:
			neighbors = [n for n in graph.neighbors(current) if n not in seen]
			if len(neighbors) != 1:
				print(node,current,neighbors )
				return []
			current = neighbors[0]
			seen.add(current)
		result.append((current, len(seen)))
	return result

def optimize(graph, junctions: set):
	result = nx.MultiGraph()
	for node in junctions:
		for other, dist in find_adjecent_junctions(graph, node, junctions):
			if result.has_edge(node, other) and result[node][other][0]["weight"] == dist:
				continue
			result.add_edge(node, other, weight=dist)
	return result


hiking_map = {}
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		for col, char in enumerate(line.strip()):
			if char == "#":
				continue
			hiking_map[(col, row)] = char

start, target = min(hiking_map), max(hiking_map)
p1_graph = build_graph(hiking_map, False)
p2_graph = build_graph(hiking_map, True)
trail_junctions = [start] + find_junctions(p2_graph) + [target]
p2_graph = optimize(p2_graph, set(trail_junctions))
p2_path_lenghts = [nx.path_weight(p2_graph, path, "weight") - len(path) + 1
					for path in nx.all_simple_paths(p2_graph, start, target)]

print(f"Part 1: {max([len(path)-1 for path in nx.all_simple_paths(p1_graph, start, target)])}")
print(f"Part 2: {max(p2_path_lenghts)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
