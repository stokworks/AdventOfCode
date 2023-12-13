from collections import Counter
from days import AOCDay, day


@day(2023, 7)
class Day07(AOCDay):
    test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split('\n')

    hands = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 6440
        self.common(self.test_input)
        assert self.part2(self.test_input) == 5905

    def common(self, input_data):
        self.hands = [(cards, int(bid)) for cards, bid in map(str.split, input_data)]

    def part1(self, input_data):
        def strength(cards):
            c = sorted(Counter(cards).values(), reverse=True)
            h = max(c) if len(c) > 0 else 0

            if c[0] == 5:
                return 7
            if c[0] == 4:
                return 6
            if c[0] == 3 and c[1] == 2:
                return 5
            if c[0] == 3:
                return 4
            if c[0] == 2 and c[1] == 2:
                return 3
            if h == 2:
                return 2
            return 1

        card_vals = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
                     'A': 14}

        def hand_sort_key(hand):
            return strength(hand[0]), list([card_vals[card] for card in hand[0]])

        return sum((rank + 1) * bid for rank, (_, bid) in enumerate(sorted(self.hands, key=hand_sort_key)))

    def part2(self, input_data):
        def strength(cards):
            counter = Counter(cards)
            js = counter['J']
            del counter['J']
            c = sorted(counter.values())
            h = max(c) if len(c) > 0 else 0

            if h + js == 5:
                return 7
            if h + js == 4:
                return 6
            if c == [2, 3] or c == [2, 2]:
                return 5
            if h + js == 3:
                return 4
            if c == [1, 2, 2]:
                return 3
            if h + js == 2:
                return 2
            return 1

        card_vals = {'J': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'Q': 11, 'K': 12,
                     'A': 13}

        def hand_sort_key(hand):
            return strength(hand[0]), list([card_vals[card] for card in hand[0]])

        return sum((rank + 1) * bid for rank, (_, bid) in enumerate(sorted(self.hands, key=hand_sort_key)))
