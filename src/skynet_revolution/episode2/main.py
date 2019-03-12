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
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]

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
valid_gateway_links = []

for i in range(e):
    e1 = int(input())  # the index of a gateway node
    gateway_nodes.append(e1)
    valid_gateway_links.extend([(e1, e2) for e2 in links_map.get(e1, [])])

print(f"Gateway links: {valid_gateway_links}", file=sys.stderr)

# TODO: Build a search Tree and apply A* Search (g = distance from agent to next node, h = 1 if it leads to a Gateway, 0 if not)

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    # print("0 1")

    # Calculate the distance from the nodes that lead to gateways to the agent so that we can
    #  shut them down first, this is a Best-First search
    heap = [(abs(gateway_tuple[1] - si), gateway_tuple) for gateway_tuple in valid_gateway_links]
    heapq.heapify(heap)

    print(f"The Agent is at {si}", file=sys.stderr)
    print(f"Heap: {heap}", file=sys.stderr)

    link_to_shutdown = heapq.heappop(heap)[1]
    link_str = " ".join([str(x) for x in link_to_shutdown])
    print(link_str)

    # The link has been shutdown, no need to keep track of it anymore
    valid_gateway_links.remove(link_to_shutdown)