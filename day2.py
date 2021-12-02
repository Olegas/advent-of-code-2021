# https://adventofcode.com/2021/day/2
from aocd import lines, submit

aim = 0
pos = 0
depth = 0
for i in lines:
    (dir, count) = i.split(' ')
    if dir == 'up':
        aim -= int(count)
    elif dir == 'down':
        aim += int(count)
    elif dir == 'forward':
        v = int(count)
        pos += v
        depth += aim * v

submit(pos * depth, part='b')
exit()

pos = [0, 0]
for i in lines:
    (dir, count) = i.split(' ')
    if dir == 'up':
        pos[1] -= int(count)
    elif dir == 'down':
        pos[1] += int(count)
    elif dir == 'forward':
        pos[0] += int(count)

submit(pos[0] * pos[1]);