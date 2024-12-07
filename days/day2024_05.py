from days import AOCDay, day


@day(2024, 5)
class Day2024_05(AOCDay):
    test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".split('\n')

    rules = dict()
    updates = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 143
        assert self.part2(self.test_input) == 123

    def common(self, input_data):
        input_data = '\n'.join(input_data)
        sections = input_data.split('\n\n')
        self.rules = dict()
        self.updates = [list(map(int, update.split(','))) for update in sections[1].split()]

        for a, b in [rule.split('|') for rule in sections[0].split()]:
            a, b = int(a), int(b)
            self.rules[(a, b)] = (a, b)
            self.rules[(b, a)] = (a, b)

    def comp(self, a, b):
        if (a, b) in self.rules:
            return 1 if self.rules[(a, b)] == (a, b) else -1
        else:
            return 0

    def bubble_sort(self, items):
        for n in range(len(items) - 1, 0, -1):
            swapped = False

            for i in range(n):
                if self.comp(items[i], items[i + 1]) == -1:
                    items[i], items[i + 1] = items[i + 1], items[i]
                    swapped = True

            if not swapped:
                break

    def part1(self, input_data):
        result = 0

        for update in self.updates:
            in_order = True
            for i_a, a in enumerate(update):
                for _, b in enumerate(update[i_a + 1:]):
                    if self.comp(a, b) == -1:
                        in_order = False
                        break
                if not in_order:
                    break
            if in_order:
                result += update[len(update) // 2]

        return result

    def part2(self, input_data):
        result = 0

        for update in self.updates:
            update_orig = list(update)
            self.bubble_sort(update)

            if update_orig != update:
                result += update[len(update) // 2]

        return result