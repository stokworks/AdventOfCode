import numpy as np

from days import AOCDay, day


@day(2015, 6)
class Day2015_06(AOCDay):
    test_input = """turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500""".split('\n')

    instrs = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 1000*1000 - 1000 - 4
        self.common(self.test_input)
        assert self.part2(self.test_input) == 1000*1000 + 2000 - 4

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
        size = 1000
        grid = np.full((size, size), False, dtype=bool)

        for i, (s_x, s_y), (e_x, e_y) in self.instrs:
            grid[s_x:e_x+1, s_y:e_y+1] = (True if i == '+' else False if i == '-' else np.invert(grid[s_x:e_x+1, s_y:e_y+1]))

        return np.count_nonzero(grid)

    def part2(self, input_data):
        # naive method
        size = 1000
        grid = np.full((size, size), False, dtype=int)

        for i, (s_x, s_y), (e_x, e_y) in self.instrs:
            grid_slice = grid[s_x:e_x + 1, s_y:e_y + 1]
            grid_slice += (2 if i == 't' else 1 if i == '+' else -1)
            grid_slice = np.maximum(grid_slice, np.zeros(grid_slice.shape, dtype=grid_slice.dtype))
            grid[s_x:e_x + 1, s_y:e_y + 1] = grid_slice

        return np.sum(grid)
