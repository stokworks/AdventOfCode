from days import AOCDay, day


@day(2024, 2)
class Day2024_02(AOCDay):
    test_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".split('\n')

    reports = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 2
        assert self.part2(self.test_input) == 4

    def common(self, input_data):
        self.reports = [list(map(int, line.split())) for line in input_data]

    def part1(self, input_data):
        n_safe = 0

        for report in self.reports:
            diffs = set(map(lambda pair: pair[0] - pair[1], zip(report, report[1:])))
            n_safe += 1 if diffs <= {1, 2, 3} or diffs <= {-1, -2, -3} else 0

        return n_safe

    def part2(self, input_data):
        # This solution is O(n^2) but can be easily optimized to O(n)

        n_safe = 0

        for report in self.reports:
            if all(map(lambda pair: 1 <= pair[1] - pair[0] <= 3, zip(report, report[1:]))) or \
                all(map(lambda pair: 1 <= pair[0] - pair[1] <= 3, zip(report, report[1:]))):
                n_safe += 1
                continue

            for i in range(len(report)):
                report_without_i = report[:i] + report[i+1:]

                if all(map(lambda pair: 1 <= pair[1] - pair[0] <= 3, zip(report_without_i, report_without_i[1:]))) or \
                    all(map(lambda pair: 1 <= pair[0] - pair[1] <= 3, zip(report_without_i, report_without_i[1:]))):
                    n_safe += 1
                    break

        return n_safe
