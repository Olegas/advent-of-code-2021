# https://adventofcode.com/2021/day/9
from aocd import data, submit
from functools import reduce

_data = '''2199943210
3987894921
9856789892
8767896789
9899965678'''
matrix = [[int(i) for i in line] for line in data.splitlines()]
rows = len(matrix)
cols = len(matrix[0])
deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
basins = []


def get(pos):
    x, y = pos
    return matrix[y][x]


def pos_valid(pos):
    x, y = pos
    return 0 <= x < cols and 0 <= y < rows


def move(pos, delta):
    row, col = pos
    dx, dy = delta
    return row + dy, col + dx


def look_around(pos):
    positions = [move(pos, delta) for delta in deltas]
    valid = [i for i in positions if pos_valid(i)]
    return [(i, get(i)) for i in valid]


def solve1():
    res = 0
    for y in range(0, rows):
        for x in range(0, cols):
            p = x, y
            v = get(p)
            around = look_around(p)
            if all([i > v for (_, i) in around]):
                basins.append([(p, v)])
                res += v + 1

    submit(res, part='a')


def solve2():
    sizes = []
    for basin in basins:
        basin_size = 0
        points = set(basin)
        visited = []
        while len(points) > 0:
            basin_size += len(points)
            candidates = set()
            for pos, val in points:
                if pos not in visited:
                    visited.append(pos)
                    around = look_around(pos)
                    update = set(filter(
                            lambda i: val < i[1] < 9 and i[0] not in visited,
                            [(p, get(p)) for (p, v) in around]))
                    candidates.update(update)
            points = candidates
        sizes.append(basin_size)

    sizes = sorted(sizes, reverse=True)
    submit(reduce(lambda r, i: r * i, sizes[:3]))
