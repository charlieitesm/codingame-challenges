"""
The following module is a solution for https://www.codingame.com/ide/puzzle/skynet-revolution-episode-2
"""
import sys
import math
import heapq

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways

links_map = {}

n, l, e = [int(i) for i in input().split()]
print(" ".join([str(n), str(l), str(e)]), file=sys.stderr)
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    print(" ".join([str(n1), str(n2)]), file=sys.stderr)

    if n1 not in links_map:
        links_map[n1] = [n2]
    else:
        links_map.get(n1).append(n2)

    # Record the reverse vertice for practical purposes
    if n2 not in links_map:
        links_map[n2] = [n1]
    else:
        links_map.get(n2).append(n1)

gateway_nodes = []

for i in range(e):
    e1 = int(input())  # the index of a gateway node
    print(str(e1), file=sys.stderr)
    gateway_nodes.append(e1)


class Graph:
    """
    This class provides and abstraction of how the game space looks like
    """

    DEFAULT_LENGTH = 1
    SAFE_DISTANCE = 2

    def __init__(self, edges: dict, goals: list):
        self.nodes = edges.keys()
        self.goal_nodes = goals
        self.edges = edges

    def sever_link(self, from_node: int, to_node: int):
        """This removes the edges between two nodes in this Graph"""
        self.edges.get(from_node).remove(to_node)
        self.edges.get(to_node).remove(from_node)

    def dijsktra_distances(self, from_node: int) -> tuple:
        """
        Calculate the Dijsktra distances from a given node to all of the other nodes in this Graph.
        Dijsktra calculates the shortest path between two nodes, even if there are multiple paths connecting them
        :param from_node: an int representing the ID of the node from which to calculate the distances
        :return: a tuple of dict containing the distances to all the nodes in this Graph with respect to from_node
        """
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
        """
        Filter the distances to show only the distance information related for the Gateway nodes
        :param dist: a dict with the distances for all the nodes
        :param prev: a dict with the information for previous nodes
        :return: a tuple with the dist and prev for goal nodes only
        """
        new_dist = {}
        new_prev = {}

        for g in self.goal_nodes:
            goal_distance = dist.get(g)

            # This asks, is there a path to the goal? Goals with no available path have a distance == INFINITY
            if goal_distance != math.inf:
                new_dist[g] = dist.get(g)
                new_prev[g] = prev.get(g)
        return new_dist, new_prev

    def get_gateway_to_shutdown(self, d: dict, p: dict) -> tuple:
        """
        Calculates the edge to shutdown based on the urgency to do so. This urgency is calculated by how close the agent
        is to the nearest gateway.
        :param d: a dict with the distances to the node the agent is currently in
        :param p: a dict with the predecessors for each of the nodes
        :return: a tuple with the edge represented by two vertex to sever
        """
        # This will let us switch between gateway nodes and make sure we have a better chance at catching the agent
        goal_dist, goal_prev = self.filter_dijsktra_distances_to_goals(d, p)

        # Get the closest Gateway
        candidate_gateway = min(goal_dist, key=goal_dist.get)

        min_value = goal_dist[candidate_gateway]

        if min_value < Graph.SAFE_DISTANCE:  # The next gateway is not at a safe distance, shut it down ASAP!

            from_node = p.get(candidate_gateway)

        elif Graph.SAFE_DISTANCE <= min_value <= Graph.SAFE_DISTANCE:
            # We have leeway to start shutting down problematic nodes that lead to two different gateways
            problem_node_count = self.get_problem_node_count()

            if not problem_node_count:  # If there are no problems, return the candidate_gateway
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

        else:
            # We have leeway to start shutting down problematic nodes that lead to two different gateways
            problem_node_count = self.get_problem_node_count()

            if not problem_node_count:  # If there are no problems, return the candidate_gateway
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
        """
        Get a dict with all of the nodes for which there is more than one edge. This will help us detect double-entry
            gateways
        :return: a dict with Gateway nodes with more than one entry edge
        """
        problem_node_count = {}

        for g in self.goal_nodes:
            for neighbor in self.edges.get(g):
                if neighbor in problem_node_count:
                    problem_node_count[neighbor][0] += 1
                else:
                    problem_node_count[neighbor] = [1, g]  # The second position of the tuple is the gateway
        problem_node_count = {k: v for k, v in problem_node_count.items() if v[0] >= 2}
        return problem_node_count


# Initialize the representation of the game map
network = Graph(links_map, gateway_nodes)
previous_from_node_sever_link = -1

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# Example: 0 1 are the indices of the nodes you wish to sever the link between
# print("0 1")

# Calculate the distance from the nodes that lead to gateways to the agent so that we can
#  shut them down first, this is a Best-First search

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print(f"Agent is at: str(si)", file=sys.stderr)

    # Calculate the Dijsktra distances to all nodes for the current position of the agent
    distances, previous_nodes = network.dijsktra_distances(si)

    # If there is not a path to the Gateways (the goals) then we are done, the Agent can no longer escape!
    if not network.filter_dijsktra_distances_to_goals(distances, previous_nodes)[0]:
        break

    # Get the coordinates for the most urgent edge to sever
    from_node_sever_link, gateway_to_shutdown = network.get_gateway_to_shutdown(distances, previous_nodes)

    # Print the coordinates so that the game engine severs the edge in its own game map
    print(f"{str(from_node_sever_link)} {str(gateway_to_shutdown)}")

    # Sever the link from our own representation of the game map
    network.sever_link(from_node_sever_link, gateway_to_shutdown)