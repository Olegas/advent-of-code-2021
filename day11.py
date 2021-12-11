# https://adventofcode.com/2021/day/11
from aocd import data, submit
from itertools import product

_data = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''
d = [[int(i) for i in l] for l in data.splitlines()]
max_x = len(d[0])
max_y = len(d)
steps = set(product((-1, 1, 0), repeat=2)) - {(0, 0)}


def produce_candidates(pt):
    x, y = pt
    return [(x + dx, y + dy) for (dx, dy) in steps if 0 <= x + dx < max_x and 0 <= y + dy < max_y]


def iterate(n, vis=False):
    total_flashes = 0
    i = 0
    while n == -1 or i < n:
        i += 1
        flashed = set()
        will_flash = set()

        # charging
        for y in range(0, max_y):
            for x in range(0, max_x):
                d[y][x] += 1
                if d[y][x] > 9:
                    will_flash.add((x, y))

        # flashing
        while len(will_flash) > 0:
            pt = will_flash.pop()
            if pt not in flashed:
                flashed.add(pt)
                for x, y in produce_candidates(pt):
                    d[y][x] += 1
                    if d[y][x] > 9:
                        will_flash.add((x, y))

        # resetting
        total_flashes += len(flashed)
        for x, y in flashed:
            d[y][x] = 0

        print('At step {} flashed {}. Total flashes: {}'.format(i + 1, len(flashed), total_flashes))
        if len(flashed) == max_x * max_y:
            return i
        if vis:
            for line in d:
                print(''.join([str(i) for i in line]))
            print()

    return total_flashes


def solve1():
    submit(iterate(100, True), part='a')


def solve2():
    submit(iterate(-1), part='b')


solve1()
solve2()
