from days import AOCDay, day


@day(2015, 2)
class Day02(AOCDay):
    test_input = """2x3x4""".split('\n')

    boxes = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.input_data) == 58
        assert self.part2(self.input_data) == 34

    def common(self, input_data):
        self.boxes = [tuple(map(int, box.split('x'))) for box in input_data]

    def part1(self, input_data):
        return sum(l*h*2 + l*w*2 + h*w*2 + min(l*h, l*w, h*w) for l, h, w in self.boxes)

    def part2(self, input_data):
        return sum(min((l+h)*2, (l+w)*2, (h+w)*2) + l*w*h for l, h, w in self.boxes)