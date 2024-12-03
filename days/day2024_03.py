from days import AOCDay, day

import re


@day(2024, 3)
class Day2024_03(AOCDay):
    test_input = ["""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""]
    test_input2 = ["""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""]

    def test(self, input_data):
        assert self.part1(self.test_input) == 161
        assert self.part2(self.test_input2) == 48

    def common(self, input_data):
        pass

    def part1(self, input_data):
        acc = 0
        for a, b in re.findall(r"mul\((\d+),(\d+)\)", '\n'.join(input_data)):
            acc += int(a) * int(b)
        return acc

    def part2(self, input_data):
        acc = 0
        do = 1
        for i, a, b in re.findall(r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))", '\n'.join(input_data)):
            if i == "do()":
                do = 1
            elif i == "don't()":
                do = 0
            else:
                acc += do * int(a) * int(b)
        return acc
