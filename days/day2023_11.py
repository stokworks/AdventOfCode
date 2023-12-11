import numpy as np
from itertools import combinations
from sortedcollections import SortedList

from days import AOCDay, day


@day(2023, 11)
class Day2023_11(AOCDay):
    test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".split('\n')

    galaxies = []
    empty_rows = SortedList()
    empty_cols = SortedList()

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 374

    def common(self, input_data):
        grid = np.array([[c == '#' for c in line] for line in input_data], dtype=bool)
        self.empty_cols = SortedList(np.where(~grid.any(axis=0))[False])
        self.empty_rows = SortedList(np.where(~grid.any(axis=1))[False])
        self.galaxies = list(zip(*np.where(grid == True)))

    def calculate_total_dists(self, galaxy_size):
        cache1 = dict()
        cache2 = dict()

        def bisect_cache(target_list, coord):
            target_cache = cache1 if target_list else cache2
            if coord not in target_cache:
                target_cache[coord] = max(0, (self.empty_rows if target_list else self.empty_cols).bisect_left(coord))

            return target_cache[coord]

        total_dist = 0

        for (y1, x1), (y2, x2) in combinations(self.galaxies, 2):
            x1, x2 = (x2, x1) if x1 > x2 else (x1, x2)
            y1, y2 = (y2, y1) if y1 > y2 else (y1, y2)

            empty_rows_inbetween = bisect_cache(True, y2) - bisect_cache(True, y1)
            empty_cols_inbetween = bisect_cache(False, x2) - bisect_cache(False, x1)

            total_dist += (x2 - x1) + (y2 - y1) + (empty_rows_inbetween + empty_cols_inbetween) * (galaxy_size - 1)

        return total_dist

    def part1(self, input_data):
        yield self.calculate_total_dists(2)

    def part2(self, input_data):
        yield self.calculate_total_dists(1000000)
