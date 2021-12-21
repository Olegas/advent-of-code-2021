# https://adventofcode.com/2021/day/16
# Insipred by https://twitter.com/Brotherluii/status/1473019794005843969
# Idea with +4/-2 was not clear for me...
from aocd import data, submit

_data = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

sym_map, grid = data.split('\n\n')
pic = grid.splitlines()
height = len(pic)
width = len(pic[0])
w = 1
delta = [(-1, -1), (0, -1), (1, -1),
         (-1, 0), (0, 0), (1, 0),
         (-1, 1), (0, 1), (1, 1)]


def print_mem(m):
    xs = [i for i, _ in m]
    ys = [i for _, i in m]
    x_range = range(min(xs), max(xs) + 1)
    y_range = range(min(ys), max(ys) + 1)
    for y in y_range:
        print('')
        for x in x_range:
            print('#' if (x, y) in m else '.', end='')
    print()


def iterate(n, image):
    mem = set()
    offset = 4
    for y, l in enumerate(image):
        for x, c in enumerate(l):
            if c == '#':
                mem.add((x, y))
    # print_mem(mem)
    for n in range(n):
        mem2 = set()
        for x in range(-offset, width + offset):
            for y in range(-offset, height + offset):
                buffer = ''
                for d in delta:
                    dx, dy = d
                    buffer += '1' if (x + dx, y + dy) in mem else '0'
                if sym_map[int(buffer, 2)] == '#':
                    mem2.add((x, y))
        offset += 4 if n % 2 else -2
        mem = mem2
        # print_mem(mem)
    return len(mem)


print(iterate(2, pic))
print(iterate(50, pic))



