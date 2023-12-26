import time
import networkx as nx

begin = time.time()

###

wire_graph = nx.Graph()
with open("input.txt") as file:
	for line in file.readlines():
		k, vals = line.strip().split(":")
		wire_graph.add_edges_from((k, v) for v in vals.strip().split())

the_three_wires = nx.minimum_edge_cut(wire_graph)
wire_graph.remove_edges_from(the_three_wires)
group_a, group_b = nx.connected_components(wire_graph)

print(f"Part 1: {len(group_a) * len(group_b)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
