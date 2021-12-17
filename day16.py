# https://adventofcode.com/2021/day/16
from aocd import data, submit
from functools import reduce

def hex2bin(hex_str):
    return ''.join(['{0:04b}'.format(int(c, 16)) for c in hex_str])


class Reader:
    def __init__(self, hex_str):
        self.bin_str = hex2bin(hex_str)
        self.ptr = 0

    def consume(self, n):
        i = self.bin_str[self.ptr:self.ptr + n]
        self.ptr += n
        return int(i, 2)

    def tell(self):
        return self.ptr


def read_literal(reader, version):
    bits = ''
    keep_reading = True
    while keep_reading:
        i = reader.consume(5)
        keep_reading = i & 0b10000
        addition = '{0:04b}'.format(i & 0b1111)
        bits += addition
    return 4, version, int(bits, 2)


def process_result(packet_id, sub_packets):
    values = [p[2] for p in sub_packets]
    if packet_id == 0:
        return sum(values)
    elif packet_id == 1:
        return reduce(lambda r, i: r * i, values)
    elif packet_id == 2:
        return min(values)
    elif packet_id == 3:
        return max(values)
    elif packet_id == 5:
        assert len(values) == 2
        return 1 if values[0] > values[1] else 0
    elif packet_id == 6:
        assert len(values) == 2
        return 1 if values[0] < values[1] else 0
    elif packet_id == 7:
        assert len(values) == 2
        return 1 if values[0] == values[1] else 0
    else:
        assert False


def read_packets_by_count(reader, count):
    result = []
    for i in range(0, count):
        result.extend(read_outer_packet(reader))
    return result


def read_packets_by_len(reader, count_bits):
    pos = reader.tell()
    result = []
    while reader.tell() - pos < count_bits:
        result.extend(read_outer_packet(reader))
    return result


def read_outer_packet(reader):
    packets = []
    version = reader.consume(3)
    packet_id = reader.consume(3)
    if packet_id == 4:
        packets.append(read_literal(reader, version))
    else:
        length_type = reader.consume(1)
        if length_type == 0:
            number_of_bits = reader.consume(15)
            res = read_packets_by_len(reader, number_of_bits)
        else:
            number_of_subpackets = reader.consume(11)
            res = read_packets_by_count(reader, number_of_subpackets)
        # For part 2
        packets.append((packet_id, version, process_result(packet_id, res)))
        # For part 1
        # packets.append((packet_id, version, None))
        # packets.extend(res)
    return packets


def solve1():
    reader = Reader(data)
    res = read_outer_packet(reader)
    accu = 0
    for p in res:
        pkt_id, version, _ = p
        accu += version
    submit(accu, part='a')


def solve2():
    reader = Reader(data)
    res = read_outer_packet(reader)
    answer = res[0][2]
    submit(answer, part='b')
    print(res)

solve2()