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

n, l, e, links_map, gateway_nodes = debug_get_info_from_file("test_case2.txt")


class Graph:
    DEFAULT_LENGTH = 1

    def __init__(self, edges: dict, goals: list):
        self.nodes = edges.keys()
        self.goal_nodes = goals
        self.edges = edges

    def sever_link(self, from_node: int, to_node: int):
        self.edges.get(from_node).remove(to_node)
        self.edges.get(to_node).remove(from_node)

    def dijsktra_distances(self, from_node: int) -> tuple:
        dist = {}
        prev = {}
        heap_queue = []

        for n1 in self.nodes:
            priority = math.inf if n1 != from_node else 0
            dist[n1] = priority
            prev[n1] = None

            # heapq uses a tuple where the first element is the value to order
            heap_queue.append((priority, n1))

        heapq.heapify(heap_queue)

        while heap_queue:
            u = heapq.heappop(heap_queue)[1]

            for v in self.edges.get(u):
                alt = dist.get(u) + Graph.DEFAULT_LENGTH

                if alt < dist.get(v):
                    dist[v] = alt
                    prev[v] = u

                    # Update value of neighbor v
                    for i in range(len(heap_queue)):
                        priority, n1 = heap_queue[i]

                        if n1 == v:
                            heap_queue[i] = (alt, v)
                            break

            heapq.heapify(heap_queue)

        return dist, prev

    def dijsktra_distances_to_goals(self, from_node: int, goals: list) -> tuple:
        dist, prev = self.dijsktra_distances(from_node)

        new_dist = {}
        new_prev = {}

        for g in goals:
            goal_distance = dist.get(g)

            if goal_distance != math.inf:
                new_dist[g] = dist.get(g)
                new_prev[g] = prev.get(g)
        return new_dist, new_prev

    @staticmethod
    def get_gateway_to_shutdown(candidate_distances: dict, prev_nodes: dict, previous_from_node: int) -> int:
        # This will let us switch between gateway nodes and make sure we have a better chance at catching the agent
        candidate_gateway = min(candidate_distances, key=candidate_distances.get)

        if previous_from_node < 0:
            return candidate_gateway

        min_value = candidate_distances[candidate_gateway]

        other_candidates = {k: v for k, v in candidate_distances.items() if v == min_value and k != candidate_gateway}

        for new_candidate in other_candidates.keys():
            if previous_from_node_sever_link != prev_nodes[new_candidate]:
                candidate_gateway = new_candidate
                break

        return candidate_gateway


network = Graph(links_map, gateway_nodes)
previous_from_node_sever_link = -1

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# Example: 0 1 are the indices of the nodes you wish to sever the link between
# print("0 1")

# Calculate the distance from the nodes that lead to gateways to the agent so that we can
#  shut them down first, this is a Best-First search
# game loop
# while True:
for si in [0, 9, 2, 6]:
    #si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print(str(si), file=sys.stderr)

    distances, previous_nodes = network.dijsktra_distances_to_goals(si, gateway_nodes)

    if not distances:
        break

    gateway_to_shutdown = network.get_gateway_to_shutdown(distances, previous_nodes, previous_from_node_sever_link)

    from_node_sever_link = previous_nodes.get(gateway_to_shutdown)

    print(f"{str(from_node_sever_link)} {str(gateway_to_shutdown)}")
    network.sever_link(from_node_sever_link, gateway_to_shutdown)

    previous_from_node_sever_link = from_node_sever_link

