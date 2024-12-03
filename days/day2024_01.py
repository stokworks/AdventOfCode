from days import AOCDay, day


@day(2024, 1)
class Day2024_01(AOCDay):
    test_input = """3   4
4   3
2   5
1   3
3   9
3   3""".split('\n')

    lists = []
    list1 = []
    list2 = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 11
        assert self.part2(self.test_input) == 31

    def common(self, input_data):
        self.lists = list(map(sorted, zip(*[map(int, l.split()) for l in input_data])))
        self.list1 = self.lists[0]
        self.list2 = self.lists[1]

    def part1(self, input_data):
        return sum(map(lambda e: abs(e[0]-e[1]), zip(*self.lists)))

    def part2(self, input_data):
        return sum(map(lambda e: e * self.list2.count(e), self.list1))
