# https://adventofcode.com/2021/day/7
from aocd import data, submit
from collections import Counter

_data = '''16,1,2,0,4,2,7,1,2,14'''
numbers = [int(i) for i in data.split(',')]

c = Counter(numbers)
pmin = min(numbers)
pmax = max(numbers)

minf = None
minpos = None
for i in range(pmin, pmax):
    fuel = 0
    for pos, count in c.items():
        # Part 1
        # cost = abs(pos - i)
        # Part 2
        # Movement cost is arithmetic progression from 1 to distance
        dist = abs(pos - i)
        cost = (1 + dist) * dist / 2
        fuel += cost * count
    if minf is None or fuel < minf:
        minpos = i
        minf = fuel


submit(int(minf))