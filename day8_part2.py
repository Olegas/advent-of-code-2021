# https://adventofcode.com/2021/day/8
from aocd import get_data, submit

data = get_data(day=8)
signals_per_digit = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
#   2, 3, 4, [5, 5, 5], [6, 6, 6], 7   <--- number of sectors
#   1, 7, 4,             0  6  9   8   <--- actual numbers
#BL                      +  +  -       <--- BL is bottom left, B is bottom
#B                       +  +  +
#             2, 3, 5
#BL           +  -  -
#B            +  +  +


def solve(line):
    symbols = [None] * 10

    codes, result = line.strip().split(' | ')
    codes = codes.split(' ')
    codes = [tuple(sorted(i)) for i in codes]
    result = result.split(' ')
    result = [tuple(sorted(i)) for i in result]

    # This is the digits which can be found by symbols length
    symbols[1] = digit1 = next(filter(lambda i: len(i) == 2, codes))
    symbols[7] = digit7 = next(filter(lambda i: len(i) == 3, codes))
    symbols[8] = digit8 = next(filter(lambda i: len(i) == 7, codes))
    symbols[4] = digit4 = next(filter(lambda i: len(i) == 4, codes))

    # top present in 7 bot not in 1
    top = set(digit7) - set(digit1)
    # bottom left corner (BL + B) is everything minus digit 4 and minus top
    bottom_left_corner = set(digit8) - set(digit4) - top
    digits069 = list(filter(lambda i: len(i) == 6, codes))
    digits235 = filter(lambda i: len(i) == 5, codes)

    # count signal which is present in bottom-left corner among digits 0, 6 and 9
    counts = {c: 0 for c in bottom_left_corner}
    for d in digits069:
        for s in d:
            if s in bottom_left_corner:
                counts[s] += 1
    # The minimal count is for bottom left signal
    bottom_left = min(counts, key=counts.get)
    # The maximum count is for bottom signal
    bottom = max(counts, key=counts.get)

    # 9 is a symbol among 0, 6 and 9 which is NOT contains bottom_left signal
    symbols[9] = digit9 = next(filter(lambda i: bottom_left not in i, digits069))
    # 2 is a symbol among 2, 3 and 5 which contains bottom_left signal
    symbols[2] = digit2 = next(filter(lambda i: bottom_left in i, digits235))

    # ad so on...
    middle = set(digit2) - set(digit7) - set(bottom_left) - set(bottom)
    symbols[0] = digit0 = tuple(sorted(set(digit8) - set(middle)))
    symbols[3] = digit3 = tuple(sorted(set(digit7).union(middle).union(bottom)))
    top_left = set(digit9) - set(digit7) - set(middle) - set(bottom)
    bottom_right = set(digit9) - set(digit2) - set(top_left)
    symbols[5] = digit5 = tuple(sorted(top_left.union(bottom_right).union(middle, top, bottom)))
    symbols[6] = digit6 = tuple(sorted(set(digit5).union(bottom_left)))

    sym_hash = {}
    for idx, sym in enumerate(symbols):
        sym_hash[sym] = idx

    res_str = ''
    for i in result:
        res_str += str(sym_hash[i])

    return int(res_str)

accu = 0
for line in data.splitlines():
    accu += solve(line)
submit(accu, day=8, part='b')

