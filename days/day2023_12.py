from functools import cache

from line_profiler_pycharm import profile

from days import AOCDay, day


@cache
def possibilities(groups, numbers):
    if len(groups) == 1 and len(numbers) == 1:
        group, number = groups[0], numbers[0]

        if len(group) < number:
            return 0
        if len(group) == number:
            return 1

        first_pound = group.find('#')
        last_pound = group.rfind('#')
        if first_pound == last_pound == -1:
            return len(group) - number + 1
        if last_pound - first_pound + 1 > number:
            return 0
        if last_pound - first_pound + 1 == number:
            return 1
        else:
            return min(first_pound, len(group) - number) - max(0, last_pound - number + 1) + 1

    groups_containing_pound = tuple(group for group in groups if '#' in group)
    if len(numbers) == len(groups_containing_pound):
        prod = 1
        for group, number in zip(groups_containing_pound, numbers):
            result = possibilities((group,), (number,))
            if result == 0:
                return 0
            prod *= result
        return prod

    it = iter(numbers)
    number, rest_numbers = next(it), tuple(it)
    acc = 0
    for gi, group in enumerate(groups):
        for pos in range(0, len(group) - number + 1):
            if pos > 0 and '#' in group[:pos]:
                break
            if len(group) - (pos + number) >= 1 and group[pos + number] == '#':
                continue

            new_head = (group[pos+number+1:],) if len(group) - (pos + number) >= 2 else ()
            acc += possibilities(new_head + groups[gi+1:], rest_numbers)

        if '#' in group:
            break
    return acc


@day(2023, 12)
class Day2023_12(AOCDay):
    test_input = """???.### 1,1,3""".split('\n')
    test_input2 = """.??..??...?##. 1,1,3""".split('\n')
    test_input3 = """?#?#?#?#?#?#?#? 1,3,1,6""".split('\n')
    test_input4 = """????.#...#... 4,1,1""".split('\n')
    test_input5 = """????.######..#####. 1,6,5""".split('\n')
    test_input6 = """?###???????? 3,2,1""".split('\n')
    test_input7 = """??#?# 4""".split('\n')
    test_input8 = """???#??????#.? 2,1,1,2""".split('\n')
    test_input9 = """#??????# 1,1,2""".split('\n')

    def test(self, input_data):
        assert next(self.part1(self.test_input)) == 1
        assert next(self.part1(self.test_input2)) == 4
        assert next(self.part1(self.test_input3)) == 1
        assert next(self.part1(self.test_input4)) == 1
        assert next(self.part1(self.test_input5)) == 4
        assert next(self.part1(self.test_input6)) == 10
        assert next(self.part1(self.test_input7)) == 1
        assert next(self.part1(self.test_input8)) == 4
        assert next(self.part1(self.test_input9)) == 3
        assert next(self.part2(self.test_input)) == 1
        assert next(self.part2(self.test_input2)) == 16384
        assert next(self.part2(self.test_input3)) == 1
        assert next(self.part2(self.test_input4)) == 16
        assert next(self.part2(self.test_input5)) == 2500
        assert next(self.part2(self.test_input6)) == 506250

    def common(self, input_data):
        pass

    def part1(self, input_data):
        problems = []
        for line in input_data:
            parts = line.split()
            groups = tuple(s for s in parts[0].split('.') if s)
            numbers = tuple(map(int, parts[1].split(',')))
            problems.append((groups, numbers))

        yield sum(possibilities(groups, numbers) for groups, numbers in problems)

    def part2(self, input_data):
        problems = []
        for line in input_data:
            parts = line.split()
            groups = tuple(s for s in '?'.join([parts[0]] * 5).split('.') if s)
            numbers = tuple(map(int, parts[1].split(',') * 5))
            problems.append((groups, numbers))

        yield sum(possibilities(groups, numbers) for groups, numbers in problems)
