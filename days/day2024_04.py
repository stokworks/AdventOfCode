from days import AOCDay, day


@day(2024, 4)
class Day2024_04(AOCDay):
    test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split('\n')

    def test(self, input_data):
        assert self.part1(self.test_input) == 18
        assert self.part2(self.test_input) == 9

    def common(self, input_data):
        pass

    def part1(self, input_data):
        result = 0

        for s_y in range(len(input_data)):
            for s_x in range(len(input_data[0])):
                if input_data[s_y][s_x] not in ('X', 'S'):
                    continue

                for dy, dx in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
                    word = ''
                    while True:
                        dist = len(word)
                        y, x = s_y + dy * dist, s_x + dx * dist

                        if not (0 <= y < len(input_data)) or not (0 <= x < len(input_data[0])):
                            break

                        word += input_data[y][x]

                        if len(word) == 4:
                            break

                        if word not in ('XMAS'[:len(word)], 'SAMX'[:len(word)]):
                            break

                    result += 1 if word == 'XMAS' or word == 'SAMX' else 0

        return result

    def part2(self, input_data):
        result = 0

        for s_y in range(1, len(input_data) - 1):
            for s_x in range(1, len(input_data[0]) - 1):
                if input_data[s_y][s_x] != 'A':
                    continue

                word1 = input_data[s_y - 1][s_x - 1] + input_data[s_y][s_x] + input_data[s_y + 1][s_x + 1]
                word2 = input_data[s_y + 1][s_x - 1] + input_data[s_y][s_x] + input_data[s_y - 1][s_x + 1]

                result += 1 if word1 in ('MAS', 'SAM') and word2 in ('MAS', 'SAM') else 0

        return result