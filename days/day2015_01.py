from days import AOCDay, day


@day(2015, 1)
class Day2015_01(AOCDay):
    test_input = """()())"""

    data = None

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.input_data)) == -1
        assert next(self.part2(self.input_data)) == 5

    def common(self, input_data):
        self.data = input_data

    def part1(self, input_data):
        yield self.data.count('(') - self.data.count(')')

    def part2(self, input_data):
        pos = 0
        for i, c in enumerate(self.data):
            pos += 1 if c == '(' else -1
            if pos == -1:
                yield i + 1
                return
