from days import AOCDay, day


def rot90(rows):
    for x in range(len(rows[0])):
        yield tuple(rows[y][x] for y in reversed(range(len(rows))))


def rot270(rows):
    for x in reversed(range(len(rows[0]))):
        yield tuple(rows[y][x] for y in range(len(rows)))


def tilt_west(seq):
    new_seq = ()
    rounded_rocks = 0
    empty_spaces = 0
    for i in range(len(seq)):
        if seq[i] == '.':
            empty_spaces += 1
        elif seq[i] == 'O':
            rounded_rocks += 1
        else:
            new_seq += ('O',) * rounded_rocks + ('.',) * empty_spaces + ('#',)
            rounded_rocks = empty_spaces = 0
    return new_seq + ('O',) * rounded_rocks + ('.',) * empty_spaces


def load_west(rows):
    load = 0
    width = len(rows[0])
    for row in rows:
        for i, c in enumerate(row):
            load += width - i if c == 'O' else 0
    return load


def cycle(rows):
    for _ in range(4):
        rows = list(rot90([tilt_west(row) for row in rows]))

    return rows


def serialize(rows):
    return tuple(int(''.join('1' if c == 'O' else '0' for c in row), 2) for row in rows)


@day(2023, 14)
class Day2023_14(AOCDay):
    test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".split('\n')

    rows = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.rows) == 136
        self.common(self.test_input)
        assert self.part2(self.rows) == 64

    def common(self, input_data):
        self.rows = list(tuple(c for c in row) for row in input_data)

    def part1(self, input_data):
        return load_west([tilt_west(row) for row in rot270(self.rows)])

    def part2(self, input_data):
        rows = list(rot270(self.rows))
        prev_cycle_serialized = serialize(rows)
        history = []
        history_serialized = []
        history_serialized_set = set()
        while prev_cycle_serialized not in history_serialized_set:
            history.append(rows)
            history_serialized.append(prev_cycle_serialized)
            history_serialized_set.add(prev_cycle_serialized)
            rows = cycle(rows)
            prev_cycle_serialized = serialize(rows)

        first_occurrence = history_serialized.index(prev_cycle_serialized)
        cycle_length = len(history) - first_occurrence

        rows = history[(1_000_000_000 - first_occurrence) % cycle_length + first_occurrence]
        return load_west(rows)
