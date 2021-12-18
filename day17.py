# https://adventofcode.com/2021/day/16
from aocd import data, submit

_data = 'target area: x=20..30, y=-10..-5'
_, coords = data.split(': ')
x, y = coords.split(', ')
x_range = sorted([int(i) for i in x[2:].split('..')])
y_range = sorted([int(i) for i in y[2:].split('..')], reverse=True)
print(x_range, y_range)


def step(probe, velocity):
    x, y = probe
    dx, dy = velocity
    x += dx
    y += dy
    dx += -1 if dx > 0 else 1 if dx < 0 else 0
    dy -= 1
    return (x, y), (dx, dy)


def fire(velocity):
    v = velocity
    probe = 0, 0
    while not is_passed_away(probe):
        yield probe, v
        probe, v = step(probe, v)


def is_inside(probe):
    x, y = probe
    x1, x2 = x_range
    y1, y2 = y_range
    return x1 <= x <= x2 and y2 <= y <= y1

def is_passed_away(probe):
    x, y = probe
    x1, x2 = x_range
    y1, y2 = y_range
    return x > x2 or y < y2


def solve1():
    max_y_total = 0
    for x in range(0, 150):
        for y in range(-150, 150):
            max_y_shoot = 0
            for p, _ in fire((x, y)):
                p_x, p_y = p
                max_y_shoot = max(max_y_shoot, p_y)
                if is_inside(p):
                    print('{},{} -> {},{}. ^{}'.format(x, y, p_x, p_y, max_y_shoot))
                    max_y_total = max(max_y_shoot, max_y_total)

    submit(max_y_total, part='a')

def solve2():
    accu = 0
    for x in range(0, x_range[1] * 10):
        for y in range(-1000, 1000):
            for p, v in fire((x, y)):
                if is_inside(p):
                    accu += 1
                    break
    print(accu)

solve2()