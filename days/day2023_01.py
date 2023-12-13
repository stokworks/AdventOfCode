from string import digits

from days import AOCDay, day


@day(2023, 1)
class Day01(AOCDay):
    test_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".split('\n')

    test_input2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".split('\n')

    def test(self, input_data):
        assert self.part1(self.test_input) == 142
        assert self.part2(self.test_input2) == 281

    def common(self, input_data):
        pass

    def find(self, line, words=dict()):
        for i, c in enumerate(line):
            if c in digits:
                return int(c)

            for w in words:
                if len(w) + i > len(line):
                    continue
                if line[i:i + len(w)] == w:
                    return words[line[i:i + len(w)]]

    def part1(self, input_data):
        return sum(int(str(self.find(line)) + str(self.find(line[::-1]))) for line in input_data)

    def part2(self, input_data):
        w = {
            'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
        }

        w_rev = {word[::-1]: val for word, val in w.items()}

        return sum(int(str(self.find(line, words=w)) + str(self.find(line[::-1], words=w_rev))) for line in input_data)
