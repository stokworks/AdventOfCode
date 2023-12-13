import glob
import os
import time
import traceback
from typing import Generator

import requests

from aocdays import AOCDays

modules = filter(lambda x: not x.startswith('_'), glob.glob(os.path.dirname(__file__) + '/*.py'))
__all__ = [os.path.basename(f)[:-3] for f in modules]


def day(year_number, day_number):
    def day_decorator(cls):
        if not str(cls.__module__).replace('days.', '').startswith('_'):
            AOCDays.get_instance().add_day(year_number, day_number, cls)
        return cls

    return day_decorator


class AOCDay:
    def __init__(self, year_number, day_number, session_token):
        self.year_number = year_number
        self.day_number = day_number
        self.session_token = session_token
        self.input_filename = os.path.join(os.path.dirname(__file__),
                                           '../inputs/{}/day{:02}_{}.txt'.format(year_number, day_number, 'input'))
        self.output_filename = os.path.join(os.path.dirname(__file__),
                                            '../outputs/{}/day{:02}_{}.txt'.format(year_number, day_number, 'output'))
        self.input_data = None

    def download_input(self):
        print('Downloading input data for day {}-{}'.format(self.year_number, self.day_number))

        input_url = 'https://adventofcode.com/{}/day/{}/input'.format(self.year_number, self.day_number)
        result = requests.get(input_url, cookies={'session': self.session_token})
        if result.status_code == 200:
            with open(self.input_filename, 'w') as f:
                f.write(result.text)
        else:
            raise ConnectionError('Could not connect to AoC website to download input data.'
                                  'Error code {}: {}'.format(result.status_code, result.text))

    def load_input(self):
        os.makedirs(os.path.dirname(self.input_filename), exist_ok=True)

        if not os.path.isfile(self.input_filename):
            self.download_input()

        with open(self.input_filename, 'r') as f:
            self.input_data = [x.replace('\n', '') for x in f.readlines()]
            if len(self.input_data) == 1:
                self.input_data = self.input_data[0]

    def run(self):
        self.load_input()

        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        if os.path.isfile(self.output_filename):
            os.remove(self.output_filename)

        with open(self.output_filename, 'w') as output_file:
            def dprint(thing):
                print(thing, file=output_file)
                print(thing)

            dprint('= Day {}-{} ='.format(self.year_number, self.day_number))

            input_data = self.input_data

            output = False
            test_exception = False
            try:
                start_time = time.perf_counter_ns()
                test = self.test(input_data)
                test_time = time.perf_counter_ns() - start_time
                if test:
                    dprint('== Tests Output ==')
                    output = True
                    for x in test:
                        dprint(x)
            except Exception as e:
                dprint('== Tests Error ==')
                dprint(''.join(traceback.format_exception(None, e, e.__traceback__)))
                test_exception = True
            if output:
                dprint('== Tests ran in {:.4f} ms =='.format(test_time / 1000000))
                dprint('')

            if test_exception:
                dprint('== NOT RUNNING PARTS BECAUSE OF TEST ERRORS ==')
            else:
                start_time = time.perf_counter_ns()
                common = self.common(input_data)
                common_time = time.perf_counter_ns() - start_time
                if common:
                    dprint('== Common ==')
                    for x in common:
                        dprint(x)
                    dprint('')

                dprint('== Part 1 ==')
                start_time = time.perf_counter_ns()
                part1 = self.part1(input_data)
                printed = False
                if part1:
                    for x in part1:
                        part1_time = time.perf_counter_ns() - start_time
                        if not printed:
                            printed = True
                        dprint(x)

                if not printed:
                    part1_time = time.perf_counter_ns() - start_time
                    dprint('(no output)')
                dprint('== Ran in {:.4f} ms =='.format((common_time + part1_time) / 1000000))
                dprint('')

                start_time = time.perf_counter_ns()
                common = self.common(input_data)
                common_time = time.perf_counter_ns() - start_time
                if common:
                    dprint('== Common ==')
                    for x in common:
                        dprint(x)
                    dprint('')

                dprint('== Part 2 ==')
                start_time = time.perf_counter_ns()
                part2 = self.part2(input_data)
                printed = False
                if part2:
                    for x in part2:
                        part2_time = time.perf_counter_ns() - start_time
                        if not printed:
                            printed = True
                        dprint(x)
                if not printed:
                    part2_time = time.perf_counter_ns() - start_time
                    dprint('(no output)')

                dprint('== Ran in {:.4f} ms =='.format((common_time + part2_time) / 1000000))
                dprint('')

    def test(self, input_data) -> Generator:
        pass

    def common(self, input_data) -> Generator:
        pass

    def part1(self, input_data) -> Generator:
        pass

    def part2(self, input_data) -> Generator:
        pass
