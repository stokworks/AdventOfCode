from days import AOCDay, day


@day(2025, 1)
class Day2025_01(AOCDay):
    test_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""".split("\n")

    rotations = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 3
        # assert self.part2(self.test_input) == 6

    def common(self, input_data):
        self.rotations = list(map(lambda rotation: (+1 if rotation[0] == 'R' else -1) * int(rotation[1:]), input_data))

    def part1(self, input_data):
        acc = 0
        dail = 50

        for rotation in self.rotations:
            dail = (dail + rotation) % 100

            acc += 1 if dail == 0 else 0

        return acc

    def part2(self, input_data):
        acc = 0
        dail = 50

        for rotation in self.rotations:
            if rotation < 0:
                limit = 100 if dail == 0 else dail
                move = -min(limit, -rotation)
            else:
                limit = 100 - dail
                move = min(limit, rotation)

            dail = (dail + move) % 100
            rotation -= move

            acc += 1 if dail == 0 else 0
            acc += abs(rotation) // 100

            dail = (dail + rotation) % 100

        return acc