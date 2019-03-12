import sys
import math
import heapq

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
    DEFAULT_LENGTH = 1
    SAFE_DISTANCE = 2

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

    def filter_dijsktra_distances_to_goals(self, dist: dict, prev: dict) -> tuple:
        new_dist = {}
        new_prev = {}

        for g in self.goal_nodes:
            goal_distance = dist.get(g)

            if goal_distance != math.inf:
                new_dist[g] = dist.get(g)
                new_prev[g] = prev.get(g)
        return new_dist, new_prev

    def get_gateway_to_shutdown(self, d: dict, p: dict, previous_from_node: int) -> tuple:
        # This will let us switch between gateway nodes and make sure we have a better chance at catching the agent
        goal_dist, goal_prev = self.filter_dijsktra_distances_to_goals(d, p)

        candidate_gateway = min(goal_dist, key=goal_dist.get)

        min_value = goal_dist[candidate_gateway]

        if min_value < Graph.SAFE_DISTANCE: # The next gateway is not at a safe distance, shut it down ASAP!
            if previous_from_node < 0:
                return p.get(candidate_gateway), candidate_gateway

            other_candidates = {k: v for k, v in goal_dist.items() if v == min_value and k != candidate_gateway}

            for new_candidate in other_candidates.keys():
                if previous_from_node_sever_link != goal_prev[new_candidate]:
                    candidate_gateway = new_candidate
                break
            from_node = p.get(candidate_gateway)

        else:
            # We have leeway to start shutting down problematic nodes that lead to two different gateways
            problem_node_count = self.get_problem_node_count()

            if not problem_node_count: # If there are no problems, return the candidate_gateway
                return p.get(candidate_gateway), candidate_gateway

            problem_distance = math.inf
            most_problematic_node = None
            gateway_connected_to_problem_node = None

            for k in problem_node_count.keys():
                if d[k] < problem_distance:
                    problem_distance = problem_node_count[k][0]
                    most_problematic_node = k
                    gateway_connected_to_problem_node = problem_node_count[k][1]

            candidate_gateway = gateway_connected_to_problem_node
            from_node = most_problematic_node

        return from_node, candidate_gateway

    def get_problem_node_count(self) -> dict:
        problem_node_count = {}

        for g in self.goal_nodes:
            for neighbor in self.edges.get(g):
                if neighbor in problem_node_count:
                    problem_node_count[neighbor][0] += 1
                else:
                    problem_node_count[neighbor] = [1, g] # The second position of the tuple is the gateway
        problem_node_count = {k: v for k, v in problem_node_count.items() if v[0] >= 2}
        return problem_node_count


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
for si in [0, 3, 6, 3, 7]:
    #si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print(str(si), file=sys.stderr)

    distances, previous_nodes = network.dijsktra_distances(si)

    if not network.filter_dijsktra_distances_to_goals(distances, previous_nodes)[0]:
        break

    from_node_sever_link, gateway_to_shutdown = network.get_gateway_to_shutdown(distances,
                                                          previous_nodes,
                                                          previous_from_node_sever_link)

    print(f"{str(from_node_sever_link)} {str(gateway_to_shutdown)}")
    network.sever_link(from_node_sever_link, gateway_to_shutdown)

    previous_from_node_sever_link = from_node_sever_link

