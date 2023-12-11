from days import AOCDay, day


@day(2015, 5)
class Day2015_05(AOCDay):
    test_input = """ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb""".split('\n')

    test_input2 = """qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy""".split('\n')

    def test(self, input_data):
        assert next(self.part1(self.test_input)) == 2
        assert next(self.part2(self.test_input2)) == 2

    def common(self, input_data):
        pass

    def part1(self, input_data):
        nice_vowels = {'a', 'e', 'i', 'o', 'u'}
        naughty_combinations = {'ab', 'cd', 'pq', 'xy'}

        n_nice = 0
        for line in input_data:
            n_nice_vowels = 0
            has_double = False
            has_naughty_combination = False

            for i in range(len(line)):
                if n_nice_vowels < 3 and line[i] in nice_vowels:
                    n_nice_vowels += 1

                if not has_double and i < len(line) - 1 and line[i] == line[i + 1]:
                    has_double = True

                if not has_naughty_combination and i < len(line) - 1 and line[i:i + 2] in naughty_combinations:
                    has_naughty_combination = True
                    break

            n_nice += 1 if n_nice_vowels == 3 and has_double and not has_naughty_combination else 0

        yield n_nice

    def part2(self, input_data):
        n_nice = 0
        for line in input_data:
            last_pair = None
            pairs = set()
            has_double_pair = False
            has_3_palindrome = False

            for i in range(len(line)):
                if not has_double_pair and i < len(line) - 1:
                    pair = line[i:i + 2]
                    if pair in pairs:
                        has_double_pair = True
                    if last_pair is not None:
                        pairs.add(last_pair)
                    last_pair = pair

                if not has_3_palindrome and i < len(line) - 2 and line[i] == line[i + 2]:
                    has_3_palindrome = True

            n_nice += 1 if has_double_pair and has_3_palindrome else 0

        yield n_nice
