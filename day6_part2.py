# https://adventofcode.com/2021/day/6
# inspired by https://github.com/SnoozeySleepy/AdventofCode/blob/main/day6.py
from aocd import data, submit
from collections import Counter

_data = '''3,4,3,1,2'''
_numbers = [int(i) for i in data.split(',')]

# number of fish per internal timer value
# 0 1 2 3 4 5 6 7 8
c = [0] * 9
for timer, count in Counter(_numbers).items():
    c[timer] = count


def solve(counters, n):
    for i in range(n):
        c0 = counters[0]
        shifted = counters[1:]
        shifted.append(c0)
        shifted[6] += c0
        counters = shifted
    return sum(counters)


submit(solve(c, 80), part='a')
submit(solve(c, 256), part='b')
