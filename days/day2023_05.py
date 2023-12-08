from days import AOCDay, day


@day(2023, 5)
class Day05(AOCDay):
    test_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split('\n')

    seeds = []
    mappings = []

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.input_data)) == 35
        self.common(self.test_input)
        assert next(self.part2(self.input_data)) == 46

    def common(self, input_data):
        self.seeds = map(int, input_data[0].split()[1:])
        self.mappings = []

        for line in input_data[1:]:
            if line == '':
                continue

            if not line[0].isdigit():
                self.mappings.append([])
                continue

            self.mappings[-1].append(tuple(map(int, line.split())))

    def part1(self, input_data):
        results = []
        for seed in self.seeds:
            for mapping in self.mappings:
                for dst, src, size in mapping:
                    if src <= seed < src + size:
                        seed += dst - src
                        break

            results.append(seed)

        yield min(results)

    def part2(self, input_data):
        seed_ranges_queue = list(zip(self.seeds, self.seeds))

        for mapping in self.mappings:
            next_queue = []

            while not len(seed_ranges_queue) == 0:
                seed_range_start, seed_range_length = seed_ranges_queue.pop()
                seed_range_end = seed_range_start + seed_range_length
                seed_range_overlaps = False

                for mapping_dst, mapping_start, mapping_length in mapping:
                    mapping_delta = mapping_dst - mapping_start
                    mapping_end = mapping_start + mapping_length

                    # all fits
                    if mapping_start <= seed_range_start < mapping_end and mapping_start < seed_range_end <= mapping_end:
                        next_queue.append((seed_range_start + mapping_delta, seed_range_length))
                        seed_range_overlaps = True
                        break
                    # head fits
                    elif mapping_start <= seed_range_start < mapping_end:
                        overlap = mapping_length - (seed_range_start - mapping_start)
                        next_queue.append((seed_range_start + mapping_delta, overlap))
                        seed_ranges_queue.append((mapping_end, seed_range_length - overlap))
                        seed_range_overlaps = True
                        break
                    # tail fits
                    elif mapping_start < seed_range_end <= mapping_end:
                        overlap = mapping_length - (mapping_end - seed_range_end)
                        next_queue.append((mapping_start + mapping_delta, overlap))
                        seed_ranges_queue.append((seed_range_start, seed_range_length - overlap))
                        seed_range_overlaps = True
                        break

                # no overlap with any rule in mapping
                if not seed_range_overlaps:
                    next_queue.append((seed_range_start, seed_range_length))

            seed_ranges_queue = next_queue

        yield min(begin for begin, end in seed_ranges_queue)