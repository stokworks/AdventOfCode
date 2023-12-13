from days import AOCDay, day


@day(2023, 3)
class Day03(AOCDay):
    test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split('\n')

    grid = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.input_data) == 4361
        assert self.part2(self.input_data) == 467835

    def common(self, input_data):
        self.grid = input_data
        self.grid.insert(0, '.' * len(self.grid[0]))
        self.grid.append('.' * len(self.grid[0]))

        self.grid = ['.' + str(line) + '.' for line in self.grid]

    def part1(self, input_data):
        NUMS = list(map(str, range(10)))

        part_numbers = []

        for y, line in enumerate(self.grid):
            reading_numbers = False
            for x, c in enumerate(line):
                if not reading_numbers and c in NUMS:
                    part_numbers.append({'locs': [], 'val': 0, 'str': ''})
                    reading_numbers = True
                if reading_numbers:
                    if c in NUMS:
                        part_numbers[-1]['locs'].append((y, x))
                        part_numbers[-1]['str'] += c
                    else:
                        part_numbers[-1]['val'] = int(part_numbers[-1]['str'])
                        reading_numbers = False

        acc = 0
        for part_number in part_numbers:
            is_valid_part = False
            for y, x in part_number['locs']:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if self.grid[y + dy][x + dx] not in NUMS and self.grid[y + dy][x + dx] != '.':
                            acc += part_number['val']
                            is_valid_part = True
                            break
                    if is_valid_part:
                        break
                if is_valid_part:
                    break
        return acc

    def part2(self, input_data):
        NUMS = list(map(str, range(10)))

        part_numbers = []

        for y, line in enumerate(self.grid):
            reading_numbers = False
            for x, c in enumerate(line):
                if not reading_numbers and c in NUMS:
                    part_numbers.append({'locs': [], 'val': 0, 'str': ''})
                    reading_numbers = True
                if reading_numbers:
                    if c in NUMS:
                        part_numbers[-1]['locs'].append((y, x))
                        part_numbers[-1]['str'] += c
                    else:
                        part_numbers[-1]['val'] = int(part_numbers[-1]['str'])
                        reading_numbers = False

        gears = []

        for y, line in enumerate(self.grid):
            for x, c in enumerate(line):
                if c == '*':
                    gears.append([])
                    for part_number in part_numbers:
                        part_is_in_ratio = False
                        for dy in (-1, 0, 1):
                            for dx in (-1, 0, 1):
                                if (y + dy, x + dx) in part_number['locs']:
                                    gears[-1].append(part_number)
                                    part_is_in_ratio = True
                                    break
                            if part_is_in_ratio:
                                break

        return sum(
            list(map(
                lambda parts: parts[0]['val'] * parts[1]['val'],
                list(filter(
                    lambda gear: len(gear) == 2,
                    gears
                ))
            ))
        )
