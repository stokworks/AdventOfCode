from days import AOCDay, day


def find_symmetry_index(seq, exclude=None):
    for i in range(1, len(seq)):
        if i == exclude:
            continue
        if all(a == b for a, b in zip(seq[:i][::-1], seq[i:])):
            return i
    return 0


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
        assert next(self.part2(self.test_input)) == 400

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

        self.patterns = []
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
        summary = 0

        for rows, cols in self.patterns:
            summary += find_symmetry_index([int(col, 2) for col in cols]) + \
                       find_symmetry_index([int(row, 2) for row in rows]) * 100

        yield summary

    def part2(self, input_data):
        summary = 0

        for rows, cols in self.patterns:
            orig_symmetry_col = find_symmetry_index([int(col, 2) for col in cols])
            orig_symmetry_row = find_symmetry_index([int(row, 2) for row in rows])

            found = False
            for y in range(len(rows)):
                for x in range(len(cols)):
                    new_row = rows[y][:x] + ('1' if rows[y][x] == '0' else '0') + rows[y][x + 1:]
                    new_col = cols[x][:y] + ('1' if cols[x][y] == '0' else '0') + cols[x][y + 1:]
                    new_rows = rows[:y] + [new_row] + rows[y + 1:]
                    new_cols = cols[:x] + [new_col] + cols[x + 1:]

                    new_symmetry_col = find_symmetry_index([int(col, 2) for col in new_cols], exclude=orig_symmetry_col)
                    new_symmetry_row = find_symmetry_index([int(row, 2) for row in new_rows], exclude=orig_symmetry_row)

                    if new_symmetry_col != 0 or new_symmetry_row != 0:
                        summary += new_symmetry_col + new_symmetry_row * 100
                        found = True

                    if found:
                        break
                if found:
                    break

        yield summary
