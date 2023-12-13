from days import AOCDay, day


@day(2023, 9)
class Day2023_09(AOCDay):
    test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split('\n')

    histories = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 114

    def common(self, input_data):
        self.histories = [list(map(lambda num: int(num), line.split(' '))) for line in input_data]

    def diffs(self, nums):
        for i, num in enumerate(nums[:-1]):
            yield nums[i+1] - num

    def part1(self, input_data):
        nextinline = []
        for history in self.histories:
            futures = [history]
            while not all([future == 0 for future in futures[-1]]):
                futures.append(list(self.diffs(futures[-1])))

            futures = list(reversed(futures))

            for i, future in enumerate(futures[1:]):
                future.append(futures[i][-1] + future[-1])

            nextinline.append(futures[-1][-1])
        return sum(nextinline)

    def part2(self, input_data):
        nextinline = []
        for history in self.histories:
            futures = [history]
            while not all([future == 0 for future in futures[-1]]):
                futures.append(list(self.diffs(futures[-1])))

            futures = list(reversed(futures))

            for i, future in enumerate(futures[1:]):
                future.insert(0, future[0] - futures[i][0])

            nextinline.append(futures[-1][0])
        return sum(nextinline)
