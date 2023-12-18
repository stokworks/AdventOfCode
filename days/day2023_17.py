from days import AOCDay, day

from heapq import heappush, heappop
from math import inf

LEGAL_MOVES = {(0, 0): ((1, 0), (0, 1)),
               (0, -1): ((1, 0), (-1, 0)),
               (1, 0): ((0, -1), (0, 1)),
               (0, 1): ((1, 0), (-1, 0)),
               (-1, 0): ((0, -1), (0, 1))}


def path_find(grid, min_dist, max_dist):
    dest = (len(grid) - 1, len(grid[0]) - 1)
    dest_y, dest_x = dest
    heap = [(0, (0, 0), (0, 0))]
    heat_map = dict()
    visited = set()

    while heap:
        heat_loss, coord, direction = heappop(heap)
        y, x = coord

        if coord == dest:
            break

        if (coord, direction) in visited:
            continue

        visited.add((coord, direction))

        for new_direction in LEGAL_MOVES[direction]:
            dy, dx = new_direction
            new_heat_loss = heat_loss
            for steps in range(1, max_dist + 1):
                new_coord = (y + steps * dy, x + steps * dx)
                new_y, new_x = new_coord

                if new_x < 0 or new_y < 0 or new_x > dest_x or new_y > dest_y:
                    continue

                new_heat_loss = new_heat_loss + grid[new_y][new_x]

                if steps >= min_dist:
                    new_node = (new_coord, new_direction)
                    if heat_map.get(new_node, inf) <= new_heat_loss:
                        continue
                    heat_map[new_node] = new_heat_loss
                    heappush(heap, (new_heat_loss, new_coord, new_direction))

    return min(heat_map.get((dest, (1, 0)), inf), heat_map.get((dest, (0, 1)), inf))


@day(2023, 17)
class Day2023_17(AOCDay):
    test_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split('\n')

    test_input2 = """111111111111
999999999991
999999999991
999999999991
999999999991""".split('\n')

    grid = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 102
        assert self.part2(self.test_input) == 94
        self.common(self.test_input2)
        assert self.part2(self.test_input2) == 71

    def common(self, input_data):
        self.grid = [[int(c) for c in line] for line in input_data]

    def part1(self, input_data):
        return path_find(self.grid, 1, 3)

    def part2(self, input_data):
        return path_find(self.grid, 4, 10)
