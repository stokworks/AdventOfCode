import math
from collections import deque
from days import AOCDay, day


@day(2023, 8)
class Day08(AOCDay):
    test_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".split('\n')

    test_input2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split('\n')

    test_input3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split('\n')

    path = []
    network = dict()
    starts = []

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 2
        self.common(self.test_input2)
        assert next(self.part1(self.test_input2)) == 6
        self.common(self.test_input3)
        assert next(self.part2(self.test_input3)) == 6

    def common(self, input_data):
        self.path = deque(int(c == 'R') for c in input_data[0])
        self.network = {rule[0:3]: (rule[7:10], rule[12:15]) for rule in input_data[2:]}

    def steps(self, start):
        n = 0
        loc = start
        while loc[2] != 'Z':
            d = self.path.popleft()
            self.path.append(d)
            loc = self.network[loc][d]
            n += 1
        return n

    def part1(self, input_data):
        yield self.steps('AAA')

    def part2(self, input_data):
        starts = map(lambda rule: rule[0:3], filter(lambda rule: rule[2] == 'A', input_data[2:]))
        yield math.lcm(*[self.steps(start) for start in starts])
