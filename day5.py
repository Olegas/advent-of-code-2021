# https://adventofcode.com/2021/day/5
from aocd import lines, submit
from functools import reduce
from collections import defaultdict

_lines = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''.strip().splitlines()

# _lines = '''0,0 -> 8,8'''.strip().splitlines()


class Line:
    def __init__(self, str):
        parsed = [i.split(',') for i in str.split(' -> ')]
        points = [[int(k) for k in i] for i in parsed]
        (start, end) = points
        self.start = start
        self.end = end

    def is_vertical(self):
        (x1, y1) = self.start
        (x2, y2) = self.end
        return y1 == y2

    def is_horizontal(self):
        (x1, y1) = self.start
        (x2, y2) = self.end
        return x1 == x2

    def __str__(self):
        (x1, y1) = self.start
        (x2, y2) = self.end
        return "{},{} -> {},{}".format(x1, y1, x2, y2)

    def __iter__(self):
        (x0, y0) = self.start
        (x1, y1) = self.end

        r = False
        if abs(x1 - x0) < abs(y1 - y0):
            (x0, x1, y0, y1) = (y0, y1, x0, x1)
            r = True

        if x0 > x1:
            (x1, x0, y1, y0) = (x0, x1, y0, y1)

        for x in range(x0, x1 + 1):
            t = (x - x0) / (x1 - x0)
            y = round(y0 * (1 - t) + y1 * t)
            yield (y, x) if r else (x, y)


field = defaultdict(lambda: 0)
all_lines = [Line(i) for i in lines]
vh_lines = [i for i in all_lines if i.is_vertical() or i.is_horizontal()]

# Part1
# for l in vh_lines:
for l in all_lines:
    for pt in l:
        field[pt] += 1

xs = [x for (x, y) in field.keys()]
ys = [y for (x, y) in field.keys()]
min_x = 0
max_x = max(xs)
min_y = 0
max_y = max(ys)
visualize = False

if visualize:
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            v = field[(x, y)]
            print(v if v > 0 else '.', end='')
        print('')

result = len([i for i in field.values() if i >= 2])
submit(result)
