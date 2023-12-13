from days import AOCDay, day


@day(2015, 1)
class Day2015_01(AOCDay):
    test_input = """()())"""

    data = None

    def test(self, input_data):
        assert self.part1(self.test_input) == -1
        assert self.part2(self.test_input) == 5

    def common(self, input_data):
        pass

    def part1(self, input_data):
        return input_data.count('(') - input_data.count(')')

    def part2(self, input_data):
        pos = 0
        for i, c in enumerate(input_data):
            pos += 1 if c == '(' else -1
            if pos == -1:
                return i + 1
