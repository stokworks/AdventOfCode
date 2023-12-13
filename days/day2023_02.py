import math

from days import AOCDay, day


@day(2023, 2)
class Day02(AOCDay):
    test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split('\n')

    games = []

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.input_data) == 8
        assert self.part2(self.input_data) == 2286

    def common(self, input_data):
        self.games = []
        for line in input_data:
            draws = []
            for draws_str in line[line.index(':') + 2:].split(';'):
                draw = []
                for draw_str in draws_str.split(','):
                    nr_col_str = draw_str.split(' ')
                    draw.append((int(nr_col_str[-2]), nr_col_str[-1]))
                draws.append(draw)
            self.games.append(draws)

    def part1(self, input_data):
        return sum(
            n + 1 if not any(map(
                lambda draws: list(filter(lambda draw: draw[0] > {'red': 12, 'green': 13, 'blue': 14}[draw[1]], draws)),
                game)
            ) else 0 for n, game in enumerate(self.games)
        )

    def power(self, game):
        balls = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        for draws in game:
            for n, ball in draws:
                balls[ball] = max(n, balls[ball])

        return math.prod(balls.values())

    def part2(self, input_data):
        return sum(map(self.power, self.games))
