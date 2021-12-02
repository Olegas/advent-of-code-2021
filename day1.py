# https://adventofcode.com/2021/day/1
from aocd import numbers, submit

data = '''
199
200
208
210
200
207
240
269
260
263'''

# numbers = [int(i) for i in data.strip().splitlines()]

count = 0
_prev = 0
sums = []
for i in range(0, len(numbers) - 2):
  print(i, i+3)
  items = numbers[i:i+3]
  sums.append(sum(items))
  if len(sums) > 1:
    lastI = len(sums) - 1
    if sums[lastI] > sums[lastI - 1]:
      count += 1

# print(sums)
# print(count)
submit(count, part='b')
exit()

count = 0
_prev = numbers[0]
for i in numbers[1:]:
  if i > _prev:
    count = count + 1
  _prev = i

submit(count, part='a')

