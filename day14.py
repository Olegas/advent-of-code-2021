# https://adventofcode.com/2021/day/14
# Still can't learn the "lanternfish" idea =(
# Inspired by https://github.com/Goldenlion5648/AdventOfCode2021/blob/af4a579ed22b3fba784b8928d0d1b05bac249153/14.py
from aocd import data, submit
from collections import Counter

_data = '''NNCB

CH -> B                         
HH -> N                         
CB -> H                         
NH -> C                         
HB -> C
HC -> B                         
HN -> C                         
NN -> C                         
BH -> H             
NC -> B
NB -> B                         
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''


lines = data.splitlines()
polymer = lines[0]
replacements = {seq: to for seq, to in [line.strip().split(' -> ') for line in lines[2:]]}


def solve(n):
    counter = Counter()
    for i in range(0, len(polymer) - 1):
        j = polymer[i:i+2]
        counter[j] += 1

    for i in range(0, n):
        new_counter = Counter()
        for pair, count in counter.items():
            a, b = pair
            r = replacements[pair]
            new_counter[a + r] += count
            new_counter[r + b] += count
        counter = new_counter

    res = Counter()
    for pair, count in counter.items():
        res[pair[0]] += count
    res[polymer[-1]] += 1
    return res


def solve_part(part, n):
    res = solve(n)
    c = res.most_common()
    print(c)
    mc = c[0][1]
    lc = c.pop()[1]
    submit(mc - lc, part=part)


solve_part('a', 10)
solve_part('b', 40)
