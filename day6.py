# https://adventofcode.com/2021/day/6
from aocd import data, submit
from collections import defaultdict

_data = '''3,4,3,1,2'''
_numbers = [int(i) for i in data.split(',')]

how_often = 7
max_turn = 80

counts = defaultdict(lambda: 0)
for i in _numbers:
    counts[i] += 1


def fish(offset=0, newborn=0):
    return range(offset + (7 + 2) * newborn, max_turn + 1, how_often)


def simulate(delay):
    # Count initial fish itself
    accu = 1
    prefill = list(fish(delay))
    while len(prefill) > 0:
        offset = prefill.pop(0)
        if offset < max_turn:
            # Fish will actually born on next turn
            accu += 1
        prefill.extend(list(fish(offset, newborn=1)))
    return accu


accu = 0
for (d, count) in counts.items():
    accu += simulate(d) * count

print(accu)

