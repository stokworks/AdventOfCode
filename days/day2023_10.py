from collections import deque

from days import AOCDay, day


@day(2023, 10)
class Day2023_10(AOCDay):
    test_input = """.....
.S-7.
.|.|.
.L-J.
.....""".split('\n')

    test_input2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""".split('\n')

    test_input3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""".split('\n')

    test_input4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".split('\n')

    test_input5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".split('\n')

    grid = []
    start = (-1, -1)
    dists = None

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 4
        self.common(self.test_input2)
        assert self.part1(self.test_input2) == 8
        self.common(self.test_input3)
        self.part1(self.test_input3)
        assert self.part2(self.test_input3) == 4
        self.common(self.test_input4)
        self.part1(self.test_input4)
        assert self.part2(self.test_input4) == 8
        self.common(self.test_input5)
        self.part1(self.test_input5)
        assert self.part2(self.test_input5) == 10

    def common(self, input_data):
        if len(self.grid) > 0 and self.grid[0] == input_data[0]:
            return

        self.grid = input_data

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 'S':
                    self.start = (y, x)
                    self.dists = {self.start: 0}
                    return

    DIR2NEXT = {
        'N': [
            (-1, 0),
            {
                '|': 'N',
                '7': 'W',
                'F': 'E',
                'S': ''
            }
        ],
        'E': [
            (0, 1),
            {
                '-': 'E',
                '7': 'S',
                'J': 'N',
                'S': ''
            }
        ],
        'S': [
            (1, 0),
            {
                '|': 'S',
                'J': 'W',
                'L': 'E',
                'S': ''
            }
        ],
        'W': [
            (0, -1),
            {
                '-': 'W',
                'L': 'N',
                'F': 'S',
                'S': ''
            }
        ]
    }

    S_TYPE = {
        'NW': 'J',
        'NS': '|',
        'NE': 'L',
        'WS': '7',
        'WE': '-',
        'SE': 'F'
    }

    def part1(self, input_data):
        s_type = ''
        s_y, s_x = self.start
        queue = deque([(s_y, s_x, 'N'), (s_y, s_x, 'W'), (s_y, s_x, 'S'), (s_y, s_x, 'E')])

        while len(queue) > 0:
            y, x, dir = queue.popleft()
            (dy, dx), char_map = self.DIR2NEXT[dir]
            next_char = self.grid[y + dy][x + dx]
            if y == s_y and x == s_x and 0 <= y + dy < len(self.grid) and 0 <= x + dx < len(self.grid[0]) \
                    and next_char in char_map or (y != s_y or x != s_x) and (y + dy, x + dx) not in self.dists:
                queue.append((y + dy, x + dx, char_map[next_char]))
                self.dists[(y + dy, x + dx)] = self.dists[(y, x)] + 1
                if y == s_y and x == s_x:
                    s_type += dir

        self.grid[s_y] = self.grid[s_y][:s_x] + self.S_TYPE[s_type] + self.grid[s_y][s_x + 1:]
        return max(self.dists.values())

    def part2(self, input_data):
        n_inside = 0

        for y in range(len(self.grid)):
            inside = False
            prev = None
            for x in range(len(self.grid[0])):
                c = self.grid[y][x]
                if c == '.' or (y, x) not in self.dists:
                    n_inside += 1 if inside else 0
                elif c == '|' or c == '7' and prev == 'L' or c == 'J' and prev == 'F':
                    inside = not inside
                elif c == 'F' or c == 'L':
                    prev = c

        return n_inside
