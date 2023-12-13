from days import AOCDay, day


@day(2015, 3)
class Day2015_03(AOCDay):
    test_input = ">"
    test_input2 = "^>v<"
    test_input3 = "^v^v^v^v^v"
    test_input4 = "^v"

    def test(self, input_data):
        assert self.part1(self.test_input) == 2
        assert self.part1(self.test_input2) == 4
        assert self.part1(self.test_input3) == 2
        assert self.part2(self.test_input4) == 3
        assert self.part2(self.test_input2) == 3
        assert self.part2(self.test_input3) == 11

    def common(self, input_data):
        pass

    def walk(self, input_data):
        x, y = 0, 0
        visited = {(x, y)}
        for c in input_data:
            if c == 'v':
                y += 1
            elif c == '>':
                x += 1
            elif c == '<':
                x -= 1
            else:
                y -= 1
            visited.add((x, y))
        return visited

    def part1(self, input_data):
        return len(self.walk(input_data))

    def part2(self, input_data):
        return len(self.walk(input_data[::2]) | self.walk(input_data[1::2]))
