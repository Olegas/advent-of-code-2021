# https://adventofcode.com/2021/day/16
from aocd import data, submit
from math import floor
import progressbar
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class _colors:
    HEADER = ''
    OKBLUE = ''
    OKCYAN = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''


class SnailfishNumber:
    def __init__(self, left, right, /, parent=None, level=0):
        self.left = left
        self.right = right
        self.parent = parent
        self.level = level

    def __add__(self, other):
        n = SnailfishNumber(self, other, level=self.level)
        self.increase_level()
        other.increase_level()
        self.parent = n
        other.parent = n
        return n

    def fmt_n(self, n):
        if n > 9:
            return '{}{}{}'.format(bcolors.OKGREEN, n, bcolors.ENDC if self.level < 4 else bcolors.WARNING)
        else:
            return str(n)

    def __str__(self):
        pref = bcolors.WARNING if self.level >= 4 else ''
        postf = bcolors.ENDC if self.level >= 4 else ''
        return "{}[{},{}]{}".format(
            pref,
            self.fmt_n(self.left) if isinstance(self.left, int) else self.left,
            self.fmt_n(self.right) if isinstance(self.right, int) else self.right,
            postf)

    def __getitem__(self, item):
        assert item == 'left' or item == 'right'
        if item == 'left':
            return self.left
        if item == 'right':
            return self.right

    def __setitem__(self, key, value):
        assert key == 'left' or key == 'right'
        if key == 'left':
            self.left = value
        if key == 'right':
            self.right = value

    def get_with_regular_number_at_left(self):
        p = SnailfishAlgo.search_parent_for_direction(self, 'left')
        if p is None:
            return None, None
        if isinstance(p.left, int):
            return p, 'left'
        else:
            return SnailfishAlgo.search_for_regular_at(p.left, 'right'), 'right'

    def get_with_regular_number_at_right(self):
        p = SnailfishAlgo.search_parent_for_direction(self, 'right')
        if p is None:
            return None, None
        if isinstance(p.right, int):
            return p, 'right'
        else:
            return SnailfishAlgo.search_for_regular_at(p.right, 'left'), 'left'

    def explode(self):
        if self.level == 4:
            pl, l_direction = self.get_with_regular_number_at_left()
            pr, r_direction = self.get_with_regular_number_at_right()
            if pl is not None:
                pl[l_direction] += self.left
            if pr is not None:
                pr[r_direction] += self.right
            if self.parent is not None:
                self.parent.child_exploded(self)
            return True

    def child_exploded(self, child):
        if self.left == child:
            self.left = 0
        elif self.right == child:
            self.right = 0

    def increase_level(self):
        self.level += 1
        if isinstance(self.left, SnailfishNumber):
            self.left.increase_level()
        if isinstance(self.right, SnailfishNumber):
            self.right.increase_level()

    def split(self, where='left'):
        if where == 'left' and isinstance(self.left, int) and self.left >= 10:
            a2 = floor(self.left / 2)
            b2 = self.left - a2
            self.left = SnailfishNumber(a2, b2, parent=self, level=self.level + 1)
            return True
        elif where == 'right' and isinstance(self.right, int) and self.right >= 10:
            a2 = floor(self.right / 2)
            b2 = self.right - a2
            self.right = SnailfishNumber(a2, b2, parent=self, level=self.level + 1)
            return True

    def magnitude(self):
        lm = self.left if isinstance(self.left, int) else self.left.magnitude()
        rm = self.right if isinstance(self.right, int) else self.right.magnitude()
        return 3 * lm + 2 * rm


class SnailfishAlgo:

    @staticmethod
    def explode_phase(n):
        if isinstance(n, int):
            return False
        return n.explode() or SnailfishAlgo.explode_phase(n.left) or SnailfishAlgo.explode_phase(n.right)

    @staticmethod
    def split_phase(n):
        if isinstance(n, int):
            return False
        return n.split('left') or SnailfishAlgo.split_phase(n.left) or n.split('right') or SnailfishAlgo.split_phase(
            n.right)

    @staticmethod
    def reduce(n):
        return SnailfishAlgo.explode_phase(n) or SnailfishAlgo.split_phase(n)

    @staticmethod
    def search_parent_for_direction(i, want_dir):
        c = i
        p = i.parent
        while p[want_dir] == c:
            c = p
            p = p.parent
            if p is None:
                return None
        return p

    @staticmethod
    def search_for_regular_at(n, want_dir):
        if isinstance(n[want_dir], int):
            return n
        else:
            return SnailfishAlgo.search_for_regular_at(n[want_dir], want_dir)

    @staticmethod
    def parse(s):
        stack = []
        accu = ''
        for c in s:
            if not c.isnumeric() and accu:
                stack.append(int(accu))
                accu = ''
            if c == '[':
                stack.append(c)
            elif c.isnumeric():
                accu += c
            elif c == ']':
                right = stack.pop()
                left = stack.pop()
                open_bracket = stack.pop()
                assert open_bracket == '['
                n = SnailfishNumber(left, right)
                if isinstance(left, SnailfishNumber):
                    left.parent = n
                    left.increase_level()
                if isinstance(right, SnailfishNumber):
                    right.parent = n
                    right.increase_level()
                stack.append(n)
        assert len(stack) == 1
        return stack.pop()


_ = '''[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]'''
_ = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]'''
_ = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''
samples = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

for line in samples.splitlines():
    assert str(SnailfishAlgo.parse(line)) == line

assert SnailfishAlgo.parse('[1,1]').level == 0
nested = SnailfishAlgo.parse('[[1,1],[2,2]]')
assert nested.left.level == 1 and nested.right.level == 1
assert isinstance(nested.left.left, int)

reduce_test = SnailfishAlgo.parse('[[9,10],20]')
while SnailfishAlgo.reduce(reduce_test):
    pass
assert str(reduce_test) == '[[9,[5,5]],[[5,5],[5,5]]]'

assert SnailfishAlgo.parse('[9,1]').magnitude() == 29
assert SnailfishAlgo.parse('[[9,1],[1,9]]').magnitude() == 129
assert SnailfishAlgo.parse('[[[[1,1],[2,2]],[3,3]],[4,4]]').magnitude() == 445
assert SnailfishAlgo.parse('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').magnitude() == 3488

p_none = SnailfishAlgo.parse('[[8,8],[[9,7],[[[8,6],3],[8,[0,2]]]]]')
while SnailfishAlgo.reduce(p_none):
    pass


def solve1():
    input_numbers = [SnailfishAlgo.parse(line) for line in data.splitlines()]
    a = input_numbers[0]
    for b in input_numbers[1:]:
        c = a + b
        while SnailfishAlgo.reduce(c):
            pass
        a = c

    submit(a.magnitude(), part='a')


def solve2():
    input_numbers = data.splitlines()
    max_magni = 0
    count_n = len(input_numbers)
    with progressbar.ProgressBar(max_value=count_n * count_n) as bar:
        for i in range(0, count_n):
            time.sleep(0.1)
            for j in range(0, count_n):
                if i != j:
                    a = SnailfishAlgo.parse(input_numbers[i])
                    #print('  {}'.format(a))
                    b = SnailfishAlgo.parse(input_numbers[j])
                    #print('+ {}'.format(b))
                    c = a + b
                    #print('= {}'.format(c))
                    while SnailfishAlgo.reduce(c):
                        pass
                    max_magni = max(max_magni, c.magnitude())
                bar.update(i * count_n + j)
    submit(max_magni, part='b')


solve2()