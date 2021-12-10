# https://adventofcode.com/2021/day/10
from aocd import data, submit
from functools import reduce

_data = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''
lines = data.splitlines()
open_bracket = '([<{'
expect = {
    '(': ')',
    '[': ']',
    '<': '>',
    '{': '}'
}


def parse(line):
    buf = []
    for char in line:
        if char in open_bracket:
            buf.append(char)
        else:
            expected = expect[buf.pop()]
            if char != expected:
                return -2, expected, char
    if len(buf) > 0:
        buf.reverse()
        return -1, buf, None
    return 0, None, None


def solve1():
    scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    accu = 0
    for i in lines:
        code, expected, actual = parse(i)
        if code == -2:
            accu += scores[actual]

    submit(accu, part='a')


def solve2():
    score_map = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    scores = []
    for i in lines:
        code, buf, __ = parse(i)
        if code == -1:
            score = reduce(lambda r, j: r * 5 + score_map[j], [expect[i] for i in buf], 0)
            scores.append(score)
    scores.sort()
    middle = scores[int(len(scores) / 2)]
    submit(middle, part='b')


solve1()
solve2()
