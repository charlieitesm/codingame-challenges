import sys
import math
import heapq

from collections import defaultdict
from skynet_revolution.episode2.file_utils import debug_get_info_from_file

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways

# links_map = {}

# n, l, e = [int(i) for i in input().split()]
# print(" ".join([str(n), str(l), str(e)]), file=sys.stderr)
# for i in range(l):
#     # n1: N1 and N2 defines a link between these nodes
#     n1, n2 = [int(j) for j in input().split()]
#     print(" ".join([str(n1), str(n2)]), file=sys.stderr)
#
#     if n1 not in links_map:
#         links_map[n1] = [n2]
#     else:
#         links_map.get(n1).append(n2)
#
#     # Record the reverse vertice for practical purposes
#     if n2 not in links_map:
#         links_map[n2] = [n1]
#     else:
#         links_map.get(n2).append(n1)
#
# gateway_nodes = []
# valid_gateway_links = []
#
# for i in range(e):
#     e1 = int(input())  # the index of a gateway node
#     print(str(e1), file=sys.stderr)
#     gateway_nodes.append(e1)
#     valid_gateway_links.extend([(e1, e2) for e2 in links_map.get(e1, [])])
#
# print(f"Gateway links: {valid_gateway_links}", file=sys.stderr)

n, l, e, links_map, gateway_nodes = debug_get_info_from_file("test_case1.txt")


class Graph:
    def __init__(self, edges: dict, goals: list):
        self.nodes = edges.keys()
        self.goal_nodes = goals
        self.edges = edges
        self.distances = {}

    def sever_link(self, from_node: int, to_node: int):
        pass

    def dijsktra_distances(self, from_node: int):
        distances = [None for _ in range(len(self.nodes))]
        distances[from_node] = 0


network = Graph(links_map, gateway_nodes)


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# Example: 0 1 are the indices of the nodes you wish to sever the link between
# print("0 1")

# Calculate the distance from the nodes that lead to gateways to the agent so that we can
#  shut them down first, this is a Best-First search
# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print(str(si), file=sys.stderr)

    heap = [(abs(gateway_tuple[1] - si), gateway_tuple) for gateway_tuple in valid_gateway_links]
    heapq.heapify(heap)

    print(f"The Agent is at {si}", file=sys.stderr)
    print(f"Heap: {heap}", file=sys.stderr)

    link_to_shutdown = heapq.heappop(heap)[1]
    link_str = " ".join([str(x) for x in link_to_shutdown])
    print(link_str)