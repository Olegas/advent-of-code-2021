# https://adventofcode.com/2021/day/13
from aocd import data, submit

_data = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''


points = set()
folds = []
for line in data.splitlines():
    if ',' in line:
        item = tuple([int(i) for i in line.split(',')])
        points.add(item)
    elif '=' in line:
        line = line[11:]
        i, j = line.split('=')
        folds.append((i, int(j)))


class TransparentSheet:
    data = set()
    w = 0
    h = 0

    def __init__(self, data: set, dim: tuple = None):
        if data:
            self.data = data
            w, h = dim or (None, None)
            self.w = w or max(x for x, y in self.data)
            self.h = h or max(y for x, y in self.data)

    def __str__(self):
        result = ''
        for y in range(0, self.h + 1):
            for x in range(0, self.w + 1):
                result += '#' if (x, y) in self.data else '.'
            result += '\n'
        return result

    def __len__(self):
        return len(self.data)

    def tear(self, axis, position):
        part1 = set()
        part2 = set()
        for k in self.data:
            (x, y) = k
            if axis == 'x':
                if x < position:
                    part1.add(k)
                elif x > position:
                    part2.add((x - position - 1, y))
            else:
                if y < position:
                    part1.add(k)
                elif y > position:
                    part2.add((x, y - position - 1))
        dim = (position - 1, self.h) if axis == 'x' else (self.w, position - 1)
        return TransparentSheet(part1, dim), TransparentSheet(part2, dim)

    def flip(self, axis):
        new_data = set()
        for pos in self.data:
            x, y = pos
            new_data.add((self.w - x, y) if axis == 'x' else (x, self.h - y))
        self.data = new_data

    def merge(self, sheet):
        self.data.update(sheet.data)
        return self


def solve(f):
    s = TransparentSheet(points)
    for axis, pos in f:
        a, b = s.tear(axis, pos)
        b.flip(axis)
        a.merge(b)
        s = a
    return s


submit(len(solve(folds[:1])), part='a')
print(solve(folds))
