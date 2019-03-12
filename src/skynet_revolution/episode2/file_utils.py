
# n, l, e, links_map, gateway_nodes, valid_gateway_links


def debug_get_info_from_file(filename: str) -> tuple:

    with open(filename) as f:
        lines = f.readlines()

    lines = [li.strip() for li in lines]

    links_map = {}

    n, l, e = [int(i) for i in lines[0].split()]
    print(" ".join([str(n), str(l), str(e)]))

    for i in range(1, l + 1):
        # n1: N1 and N2 defines a link between these nodes
        n1, n2 = [int(j) for j in lines[i].split()]
        print(" ".join([str(n1), str(n2)]))

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

    for i in lines[l + 1:]:
        e1 = int(i)  # the index of a gateway node
        print(str(e1))
        gateway_nodes.append(e1)

    return n, l, e, links_map, gateway_nodes



