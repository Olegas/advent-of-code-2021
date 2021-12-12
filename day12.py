# https://adventofcode.com/2021/day/12
from aocd import data, submit
from collections import Counter
import networkx as nx

_data = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

g = nx.Graph()
for line in data.splitlines():
    b, e = line.split('-')
    g.add_nodes_from([b, e])
    g.add_edge(b, e)


def part1(node, path):
    return node.isupper() or node not in path


def part2(node, path):
    if node == 'start':
        return False
    if node == 'end':
        return True
    if node not in path:
        return True
    if node.islower():
        # Only lowercase nodes count here
        c = Counter([i for i in path if i.islower()])
        if c.get(node) == 1:
            # This node is visited. Is there some node visited twice?
            if 2 in c.values():
                # Yes, there is. So this can not be entered twice
                return False
            else:
                # No there aren't. So this can be entered twice
                return True
        else:
            # node is visited more than once - can't enter
            # zero can't happened here, it is checked above
            return False
    else:
        # Upper case node can be visited multiple times
        return True


def solve(can_enter):
    paths = {tuple(['start'])}
    result = set()
    while len(paths) > 0:
        next_paths = set()
        for p in paths:
            last_node = p[len(p) - 1]
            if last_node != 'end':
                candidates = nx.neighbors(g, last_node)
                for c in candidates:
                    if can_enter(c, p):
                        next_paths.add((*p, c))
            else:
                result.add(p)
        paths = next_paths
    return result


submit(len(solve(part1)), part='a')
submit(len(solve(part2)), part='b')

