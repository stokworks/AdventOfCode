import math

from days import AOCDay, day


@day(2023, 4)
class Day04(AOCDay):
    test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".split('\n')

    def test(self, input_data):
        assert self.part1(self.test_input) == 13
        assert self.part2(self.test_input) == 30

    def common(self, input_data):
        pass

    def parse(self, input_data):
        bar_pos = None
        n_nrs = None

        for line in input_data:
            sliced = line.split()

            if bar_pos is None:
                bar_pos = sliced.index('|')
                n_nrs = len(sliced) - 3

            nrs = sliced[2:bar_pos] + sliced[bar_pos + 1:]
            yield n_nrs - len(set(nrs))

    def part1(self, input_data):
        return sum(map(lambda card: int(2 ** (card - 1)), self.parse(input_data)))

    def part2(self, input_data):
        card_ns = [1] * len(input_data)

        for i, card in enumerate(self.parse(input_data)):
            for j in range(card):
                card_ns[i + j + 1] += card_ns[i]

        return sum(card_ns)
