from typing import List


class AOCDays:
    _instance = None

    def __init__(self):
        self.days = {}

    def add_day(self, year, day, cls: 'days.AOCDay') -> None:
        self.days['{}_{:02}'.format(year, day)] = cls

    def get_day(self, year, day) -> 'days.AOCDay':
        classname = '{}_{:02}'.format(year, day)
        return self.days[classname] if classname in self.days else None

    @classmethod
    def get_instance(cls) -> 'AOCDays':
        if not cls._instance:
            cls._instance = AOCDays()
        return cls._instance
