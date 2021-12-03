# https://adventofcode.com/2021/day/3
from aocd import lines, submit
from functools import reduce

data = '''
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''.strip().splitlines()

bit_lines = [[int(k) for k in i] for i in lines]
line_len = len(bit_lines[0])

gamma = [0] * line_len
epsilon = [0] * line_len

mcb = [None] * line_len
lcb = [None] * line_len

def frombin(res, item):
    (index, value) = item
    return res + pow(2, line_len - index - 1) * value

def todec(a):
    return reduce(frombin, enumerate(a), 0)

def calc_ml(lines):
    _mcb = [None] * line_len
    _lcb = [None] * line_len
    for i in range(line_len):
        h = {0: 0, 1: 0}
        for k in lines:
            h[k[i]] += 1
        _mcb[i] = 0 if h[0] > h[1] else 1
        _lcb[i] = 0 if h[0] <= h[1] else 1
    return _mcb, _lcb

for i in range(line_len):
    h = {0: 0, 1: 0}
    for k in bit_lines:
        h[k[i]] += 1
    mcb[i] = 0 if h[0] > h[1] else 1
    lcb[i] = 0 if h[0] <= h[1] else 1
    gamma[i] = mcb[i]
    epsilon[i] = lcb[i]

g = todec(gamma)
e = todec(epsilon)
print(gamma, g)
print(epsilon, e)
print(g * e)
submit(g * e, part = 'a')

def find_by(rvi, items):
    pos = 0
    while len(items) > 1:
        rv = calc_ml(items)
        items = [i for i in items if i[pos] == rv[rvi][pos]]
        pos += 1
    return items[0]

_oxy = find_by(0, bit_lines)
_co2 = find_by(1, bit_lines)
oxy = todec(_oxy)
co2 = todec(_co2)
print(_co2, co2)
print(_oxy, oxy)
submit(oxy * co2, part='b')

# submit(result)