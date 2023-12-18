from days import AOCDay, day

from collections import deque


def raytrace(grid, start):
    h = len(grid)
    w = len(grid[0])
    energized = [False] * (h * w)
    seen = set()
    beams = deque([start])

    while len(beams) > 0:
        beam = beams.pop()

        if beam in seen:
            continue

        seen.add(beam)
        y, x, dir = beam

        if x != -1 and x != w and y != -1 and y != h:
            energized[y * w + x] = True

        n_y, n_x = y + dir[0], x + dir[1]
        if n_y < 0 or n_y >= h or n_x < 0 or n_x >= w:
            continue

        item = grid[n_y][n_x]

        if item == '|' and dir[1] != 0:
            beams.append((n_y, n_x, (1, 0)))
            beams.append((n_y, n_x, (-1, 0)))
        elif item == '-' and dir[0] != 0:
            beams.append((n_y, n_x, (0, 1)))
            beams.append((n_y, n_x, (0, -1)))
        elif item == '/':
            beams.append((n_y, n_x, (-dir[1], -dir[0])))
        elif item == '\\':
            beams.append((n_y, n_x, (dir[1], dir[0])))
        else:
            beams.append((n_y, n_x, dir))

    return energized.count(True)

@day(2023, 16)
class Day2023_16(AOCDay):
    test_input = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....""".split('\n')

    def test(self, input_data):
        assert self.part1(self.test_input) == 46
        assert self.part2(self.test_input) == 51

    def common(self, input_data):
        pass

    def part1(self, input_data):
        return raytrace(input_data, (0, -1, (0, 1)))

    def part2(self, input_data):
        # brute force approach
        h = len(input_data)
        w = len(input_data[0])

        highest = 0

        for y in range(h):
            result1 = raytrace(input_data, (y, -1, (0, 1)))
            result2 = raytrace(input_data, (y, w, (0, -1)))
            highest = max(result1, result2, highest)
        for x in range(w):
            result1 = raytrace(input_data, (-1, x, (1, 0)))
            result2 = raytrace(input_data, (h, x, (-1, 0)))
            highest = max(result1, result2, highest)

        return highest
