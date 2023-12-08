from math import floor, ceil, prod

from days import AOCDay, day


@day(2023, 6)
class Day06(AOCDay):
    test_input = """Time:      7  15   30
Distance:  9  40  200""".split('\n')

    def test(self, input_data):
        assert next(self.part1(self.test_input)) == 288
        assert next(self.part2(self.test_input)) == 71503

    def common(self, input_data):
        pass

    def race_get_nr_winning_strats(self, races):
        for t, d in races:
            upper = (t + (t**2 - 4*d)**0.5) / 2
            lower = (t - (t**2 - 4*d)**0.5) / 2
            offset = int(upper == upper // 1 and lower == lower // 1) * 2
            yield floor(upper) - ceil(lower) - offset + 1

    def part1(self, input_data):
        races = zip(map(int, input_data[0].split()[1:]), map(int, input_data[1].split()[1:]))
        yield prod(list(self.race_get_nr_winning_strats(races)))

    def part2(self, input_data):
        race = int(''.join(input_data[0].replace(' ', '').split(':')[1:])), \
               int(''.join(input_data[1].replace(' ', '').split(':')[1:]))
        yield next(self.race_get_nr_winning_strats([race]))
