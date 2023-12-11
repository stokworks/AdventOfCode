from days import AOCDay, day


@day(2015, 6)
class Day2015_06(AOCDay):
    test_input = """turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500""".split('\n')

    instrs = []

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 1000*1000 - 1000 - 4
        self.common(self.test_input)
        assert next(self.part2(self.test_input)) == 1000*1000 + 2000 - 4

    def common(self, input_data):
        self.instrs = []
        for line in input_data:
            parts = line.split()
            self.instrs.append((
                {'on': '+', 'off': '-', 'toggle': 't'}[parts[-4]],
                tuple(map(int, parts[-3].split(','))),
                tuple(map(int, parts[-1].split(',')))
            ))

    def part1(self, input_data):
        # naive method
        size = 1000
        grid = [False] * size**2

        for i, (s_x, s_y), (e_x, e_y) in self.instrs:
            for x in range(s_x, e_x + 1):
                for y in range(s_y, e_y + 1):
                    grid[x + y * size] = not grid[x + y * size] if i == 't' else i == '+'

        yield grid.count(True)

    def part2(self, input_data):
        # naive method
        size = 1000
        grid = [0] * size**2

        for i, (s_x, s_y), (e_x, e_y) in self.instrs:
            for x in range(s_x, e_x + 1):
                for y in range(s_y, e_y + 1):
                    grid[x + y * size] = max(0, grid[x + y * size] + (2 if i == 't' else 1 if i == '+' else -1))

        yield sum(grid)
