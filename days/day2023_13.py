from days import AOCDay, day


@day(2023, 13)
class Day2023_13(AOCDay):
    test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split('\n')

    patterns = []

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 405

    def common(self, input_data):
        def group(seq, sep, include_sep=False):
            g = []
            for el in seq:
                if el == sep:
                    yield g
                    g = []
                    if include_sep:
                        g.append(el)
                else:
                    g.append(el)
            yield g

        patterns = group(input_data, '')

        for pattern in patterns:
            rows = [''] * len(pattern)
            cols = [''] * len(pattern[0])

            for y, row in enumerate(pattern):
                for x, c in enumerate(row):
                    rows[y] += '1' if c == '#' else '0'
                    cols[x] += '1' if c == '#' else '0'

            self.patterns.append((rows, cols))

    def part1(self, input_data):
        def find_symmetry_index(seq):
            for i in range(1, len(seq)):
                if all(a == b for a, b in zip(seq[:i][::-1], seq[i:])):
                    return i
            return 0

        summary = 0

        for rows, cols in self.patterns:
            summary += find_symmetry_index([int(col, 2) for col in cols]) + find_symmetry_index([int(row, 2) for row in rows]) * 100

        yield summary

    def part2(self, input_data):
        pass
