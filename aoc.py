import json
import os
import re
import pytz
import requests
import shutil
import sys
import traceback
from datetime import datetime, timedelta

from days import *
from aocdays import AOCDays

days: AOCDays = AOCDays.get_instance()

SETTINGS = json.loads(''.join(open('settings.json').readlines()))
RESULTS_FILENAME = os.path.join(os.path.dirname(__file__), 'outputs/results.json')
MIN_YEAR = 2015


def command_init(year, day):
    template_filename = os.path.join(os.path.dirname(__file__), 'days/_template.py')
    newday_filename = os.path.join(os.path.dirname(__file__), 'days/day{}_{:02}.py'.format(year, day))

    if os.path.isfile(newday_filename):
        return

    shutil.copy(template_filename, newday_filename)
    with open(newday_filename, 'r') as f:
        lines = f.readlines()
    lines = [x.replace('@day(0, 0)', '@day({}, {})'.format(year, day)) for x in lines]
    lines = [x.replace('class DayTemplate(AOCDay):', 'class Day{}_{:02}(AOCDay):'.format(year, day)) for x in lines]
    with open(newday_filename, 'w') as f:
        f.writelines(lines)


def command_run(year, day):
    today = datetime.utcnow() - timedelta(hours=5)
    if year > today.year or year == today.year and day > today.day:
        return

    day_ref = days.get_day(year, day)

    if day_ref is None:
        return

    try:
        instance = day_ref(year, day, SETTINGS['session_token'])
        (p1_ans, p1_time), (p2_ans, p2_time) = instance.run()
    except ConnectionError as e:
        print(e, file=sys.stderr)
        return
    except Exception:
        traceback.print_exc()
        return

    if os.path.isfile(RESULTS_FILENAME):
        results = json.loads(''.join(open(RESULTS_FILENAME).readlines()))
    else:
        results = []

    found = False
    for i, result in enumerate(results):
        if result['year'] == year and result['day'] == day:
            results[i]['part1']['answer'] = p1_ans if p1_ans else result['part1']['answer']
            results[i]['part1']['time'] = p1_time if p1_ans else result['part1']['time']
            results[i]['part1']['verified'] = False
            results[i]['part2']['answer'] = p2_ans if p2_ans else result['part2']['answer']
            results[i]['part2']['time'] = p2_time if p2_ans else result['part2']['time']
            results[i]['part2']['verified'] = False
            found = True
            break
    if not found:
        new_result = {
            'year': year,
            'day': day,
            'name': '',
            'part1': {'answer': p1_ans, 'time': p1_time, 'verified': False},
            'part2': {'answer': p2_ans, 'time': p2_time, 'verified': False}
        }
        results.append(new_result)

    try:
        results_json = json.dumps(results)
        with open(RESULTS_FILENAME, 'w') as f:
            f.write(results_json)
    except Exception:
        traceback.print_exc()
        return


def command_verify(year, day):
    results = json.loads(''.join(open(RESULTS_FILENAME).readlines()))

    for i, result in enumerate(results):
        if result['year'] == year and result['day'] == day:
            if result['part1']['verified'] and result['part2']['verified']:
                break

            print('Verifying answers for day {}-{}'.format(year, day))

            url = 'https://adventofcode.com/{}/day/{}'.format(year, day)
            response = requests.get(url, cookies={'session': SETTINGS['session_token']})
            if response.status_code == 200:
                html = response.text
            else:
                raise ConnectionError('Could not connect to AoC website to download input data.'
                                      'Error code {}: {}'.format(response.status_code, response.text))

            match = re.findall('<p>Your puzzle answer was <code>(.+?)</code>\\.</p>', html)
            results[i]['part1']['verified'] = len(match) > 0 and match[0] == result['part1']['answer']
            results[i]['part2']['verified'] = len(match) > 0 and match[1] == result['part2']['answer']
            print('Part 1:', result['part1']['verified'])
            print('Part 2:', result['part2']['verified'])

            match = re.findall('<h2>--- (.+?) ---</h2>', html)
            results[i]['name'] = match[0]
            break

    try:
        results_json = json.dumps(results)
        with open(RESULTS_FILENAME, 'w') as f:
            f.write(results_json)
    except Exception:
        traceback.print_exc()
        return


def command_markdown(*args):
    results = json.loads(''.join(open(RESULTS_FILENAME).readlines()))
    results.sort(key=lambda result: (result['year'], result['day']))
    markdown = []

    current_year = None
    year_total_time = 0

    for result in results:
        if result['year'] != current_year:
            if current_year is not None:
                markdown.append('  </tbody>')
                markdown.append('  <tfoot>')
                markdown.append('    <tr>')
                markdown.append('      <th>Total time for year</th>')
                markdown.append('      <th colspan="4" align="right">{:.4f} ms</th>'.format(year_total_time))
                markdown.append('    </tr>')
                markdown.append('  </tfoot>')
                markdown.append('</table>')
                markdown.append('')

            current_year = result['year']
            year_total_time = 0

            markdown.append('## ' + str(current_year))
            markdown.append('<table>')
            markdown.append('  <thead>')
            markdown.append('    <tr>')
            markdown.append('      <th>Name</th>')
            markdown.append('      <th colspan="2">Part 1</th>')
            markdown.append('      <th colspan="2">Part 2</th>')
            markdown.append('      <th colspan="2">Solution</th>')
            markdown.append('    </tr>')
            markdown.append('  </thead>')
            markdown.append('  <tbody>')

        if result['name']:
            year_total_time += result['part1']['time'] + result['part2']['time']

            markdown.append('    <tr>')
            markdown.append('      <td align="left">')
            markdown.append('')
            markdown.append('      [{}](https://adventofcode.com/{}/day/{})'.format(result['name'], result['year'], result['day']))
            markdown.append('')
            markdown.append('      </td>')
            if result['part1']['verified']:
                markdown.append('      <td>⭐</td>')
                markdown.append('      <td align="right">{:.4f} ms</td>'.format(result['part1']['time']))
            else:
                markdown.append('      <td colspan="2"></td>')
            if result['part2']['verified']:
                markdown.append('      <td>⭐</td>')
                markdown.append('      <td align="right">{:.4f} ms</td>'.format(result['part2']['time']))
            else:
                markdown.append('      <td colspan="2"></td>')
            markdown.append('      <td>')
            markdown.append('')
            markdown.append('      [View]({}/blob/main/days/day{}_{}.py)'.format(SETTINGS['repository'], result['year'], result['day']))
            markdown.append('')
            markdown.append('      </td>')
            markdown.append('    </tr>')

    markdown.append('  </tbody>')
    markdown.append('  <tfoot>')
    markdown.append('    <tr>')
    markdown.append('      <th>Total time for year</th>')
    markdown.append('      <th colspan="5" align="right">{:.4f} ms</th>'.format(year_total_time))
    markdown.append('    </tr>')
    markdown.append('  </tfoot>')
    markdown.append('</table>')
    markdown.append('')

    shutil.copy('README.md.template', 'README.md')
    with open('README.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    insert_at = lines.index('<!--- SOLUTIONS --->\n')
    lines = lines[:insert_at] + [line + '\n' for line in markdown] + lines[insert_at + 1:]

    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)


def command_help(*args):
    print('Usage:')
    print('\t{} init (all | [year] [day] | [day] | [year])'.format(sys.argv[0]))
    print('\t{} run (all | [year] [day] | [day] | [year])'.format(sys.argv[0]))
    print('\t{} verify (all | [year] [day] | [day] | [year])'.format(sys.argv[0]))
    print('\t{} markdown'.format(sys.argv[0]))
    print('\t{} help - prints this message'.format(sys.argv[0]))
    sys.exit(1)


COMMANDS = {
    'init': command_init,
    'run': command_run,
    'verify': command_verify,
    'markdown': command_markdown,
    'help': command_help,
}


def main():
    years = []
    days = []
    today = datetime.utcnow() - timedelta(hours=5)

    if len(sys.argv) >= 2:
        command = COMMANDS[sys.argv[1]] if sys.argv[1] in COMMANDS else command_help
    else:
        command = command_help

    if len(sys.argv) == 2:
        years = [today.year]
        days = [today.day]

    if len(sys.argv) == 3:
        try:
            if sys.argv[2] == 'all':
                years = range(MIN_YEAR, today.year + 1)
                days = range(1, 26)
            else:
                num = int(sys.argv[2])
                if num >= MIN_YEAR:
                    years = [num]
                    days = range(1, 26)
                else:
                    years = [today.year]
                    days = [num]
        except ValueError:
            command_help()

    if len(sys.argv) == 4:
        try:
            years = [int(sys.argv[2])]
            days = [int(sys.argv[3])]
        except ValueError:
            command_help()

    for year in years:
        for day in days:
            command(year, day)


if __name__ == '__main__':
    main()
