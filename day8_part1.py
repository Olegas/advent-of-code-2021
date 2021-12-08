# https://adventofcode.com/2021/day/8
from aocd import get_data, submit

data = get_data(day=8)
signals_per_digit = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
search_for = [
    signals_per_digit[1],
    signals_per_digit[4],
    signals_per_digit[7],
    signals_per_digit[8],
]

lengths = [0] * 9
for line in data.splitlines():
    codes, result = line.strip().split(' | ')
    for seq in result.split(' '):
        lengths[len(seq)] += 1

result = 0
for pos in search_for:
    result += lengths[pos]

submit(result)