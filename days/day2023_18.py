from days import AOCDay, day


def get_area(instrs):
    edge_cells = 0
    pos = (0, 0)
    vertices = []

    # determine border vertices, count edge cells
    for d, dist in instrs:
        dir = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}[d]

        pos = (pos[0] + dir[0] * dist, pos[1] + dir[1] * dist)
        edge_cells += dist

        vertices.append(pos)

    # shoelace inner area
    n = len(vertices)
    area = 0.5 * abs(
        sum(vertices[i][0] * vertices[(i + 1) % n][1] - vertices[(i + 1) % n][0] * vertices[i][1] for i in range(n)))

    # Pick's theorem
    return int(area) + int(edge_cells / 2) + 1


@day(2023, 18)
class Day2023_18(AOCDay):
    test_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".split('\n')

    instrs = []

    def test(self, input_data):
        assert self.part1(self.test_input) == 62
        assert self.part2(self.test_input) == 952408144115

    def common(self, input_data):
        pass

    def part1(self, input_data):
        instrs = [
            (instr[0], int(instr[1]))
            for instr in [line.split() for line in input_data]
        ]
        return get_area(instrs)

    def part2(self, input_data):
        instrs = [
            ({'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[instr[2][-2]], int(instr[2][2:-2], 16))
            for instr in [line.split() for line in input_data]
        ]
        return get_area(instrs)
