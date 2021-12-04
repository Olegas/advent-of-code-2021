# https://adventofcode.com/2021/day/4
from aocd import lines, submit
from functools import reduce
from collections import defaultdict

_lines = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7'''.strip().splitlines()

class Matrix:
    def __init__(self, rows):
        self.rows = [[int(i) for i in row.split(' ') if i] for row in rows]
        self.p = len(rows)
        self.row_hits = [0] * len(rows)
        self.col_hits = [0] * len(rows)
        self.hits = []
        self.index = defaultdict(lambda: [])
        self.done = False

        for r, row in enumerate(self.rows):
            for c, i in enumerate(row):
                self.index[int(i)].append((r, c))

    def hit(self, n):
        if self.done:
            return False
        if n in self.index:
            hits = self.index[n]
            del self.index[n]
            for hit in hits:
                r, c = hit
                self.row_hits[r] += 1
                self.col_hits[c] += 1
                if self.row_hits[r] == self.p or  self.col_hits[c] == self.p:
                    self.done = True
                    return True

    def score(self, n):
        return sum(self.index.keys()) * n


input = [int(i) for i in lines[0].split(',')]
_m = lines[2:]
matrixes = []

while len(_m) >= 5:
    matrixes.append(Matrix(_m[:5]))
    _m = _m[6:]

# Part 1
# for i in input:
#    for m in matrixes:
#        if m.hit(i):
#            print(m.score(i))
#            exit()

last_won_score = None
for i in input:
    for m in matrixes:
        if m.hit(i):
            last_won_score = m.score(i)

submit(last_won_score)






