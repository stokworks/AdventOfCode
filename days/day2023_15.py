from days import AOCDay, day

from collections import defaultdict


def hash(val):
    acc = 0
    for c in val:
        acc = (acc + ord(c)) * 17 % 256
    return acc


@day(2023, 15)
class Day2023_15(AOCDay):
    test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

    def test(self, input_data):
        assert self.part1(self.test_input) == 1320
        assert self.part2(self.test_input) == 145

    def common(self, input_data):
        pass

    def part1(self, input_data):
        return sum(hash(instr) for instr in input_data.split(','))

    def part2(self, input_data):
        instrs = [(instr[:-1], None) if instr[-1] == '-' else (instr[:-2], int(instr[-1])) for instr in
                  input_data.split(',')]
        boxes = defaultdict(dict)

        for lens, action in instrs:
            box_number = hash(lens)

            if action is None:
                boxes[box_number].pop(lens, None)
            else:
                boxes[box_number][lens] = action

        acc = 0
        for box_number, box in boxes.items():
            lens_number = 1
            for _, focal_length in box.items():
                acc += (box_number + 1) * lens_number * focal_length
                lens_number += 1

        return acc
