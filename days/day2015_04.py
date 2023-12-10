from hashlib import md5

from days import AOCDay, day


@day(2015, 4)
class Day2015_04(AOCDay):
    def test(self, input_data):
        assert next(self.part1("abcdef")) == 609043
        assert next(self.part1("pqrstuv")) == 1048970

    def common(self, input_data):
        pass

    def part1(self, input_data):
        n = 0
        while md5((input_data + str(n)).encode()).hexdigest()[0:5] != '00000':
            n += 1

        yield n

    def part2(self, input_data):
        n = 0
        while md5((input_data + str(n)).encode()).hexdigest()[0:6] != '000000':
            n += 1

        yield n
