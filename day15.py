# https://adventofcode.com/2021/day/15
from aocd import data, submit
from heapq import heappush, heappop
from itertools import product

_data = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

matrix = [[int(i) for i in line] for line in data.splitlines()]
deltas = list(set(product((-1, 1, 0), repeat=2)) - set(product((-1, 1), repeat=2)) - {(0, 0)})


def get(pos, mat):
    x, y = pos
    return mat[y][x]


def move(pos, delta, mx, my):
    x, y = pos
    dx, dy = delta
    if 0 <= x + dx < mx and 0 <= y + dy < my:
        return x + dx, y + dy
    return None


def solve(mat):
    max_y = len(mat)
    max_x = len(mat[0])
    assert (max_x == max_y)
    start = (0, 0)
    end = (max_x - 1, max_y - 1)
    visited = set()
    h = []
    heappush(h, (0, start))

    while True:
        risk, pos = heappop(h)
        if pos == end:
            return risk
        for delta in deltas:
            next_pos = move(pos, delta, max_x, max_y)
            if next_pos and next_pos not in visited:
                visited.add(next_pos)
                d_risk = get(next_pos, mat)
                heappush(h, (risk + d_risk, next_pos))


def replicate_matrix(mat):
    mx = len(mat)
    my = len(mat[0])
    mx2 = mx * 5
    my2 = my * 5
    new_mat = []
    for y in range(0, my2):
        tile_y = y // my
        l = [0] * mx2
        for x in range(0, mx2):
            tile_x = x // mx
            orig_pos = (x % mx, y % my)
            new_value = (get(orig_pos, mat) + tile_x + tile_y) % 9
            new_value = 9 if new_value == 0 else new_value
            l[x] = new_value
        new_mat.append(l)
    return new_mat


submit(solve(matrix), part='a')
new_m = replicate_matrix(matrix)
submit(solve(new_m), part='b')
