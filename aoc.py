import json
import os
import pytz
import shutil
import sys
import traceback
from datetime import datetime, timedelta

from days import *
from aocdays import AOCDays

days: AOCDays = AOCDays.get_instance()

SETTINGS = json.loads(''.join(open('settings.json').readlines()))
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
        instance.run()
    except ConnectionError as e:
        print(e, file=sys.stderr)
    except Exception:
        traceback.print_exc()


def command_help(*args):
    print('{} - runs given year, day'.format(sys.argv[0]))
    print('Usage:')
    print('\t{} init (all | [year] [day] | [day] | [year])'.format(sys.argv[0]))
    print('\t{} run (all | [year] [day] | [day] | [year])'.format(sys.argv[0]))
    print('\t{} help - prints this message'.format(sys.argv[0]))
    sys.exit(1)


COMMANDS = {
    'init': command_init,
    'run': command_run,
    'help': command_help,
}


def main():
    command = None
    years = []
    days = []
    today = datetime.utcnow() - timedelta(hours=5)

    if len(sys.argv) >= 2:
        command = COMMANDS[sys.argv[1]] if sys.argv[1] in COMMANDS else None
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
