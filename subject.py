import datetime
import enum
from typing import List


class WeekDay(enum.Enum):
    SHANBE = 'شنبه'
    YEK_SHANBE = 'يك شنبه'
    DO_SHANBE = 'دو شنبه'
    SE_SHANBE = 'سه شنبه'
    CHAR_SHANBE = 'چهار شنبه'
    NOT_FOUND = 'Not Found'


class TimeInterval:
    def __init__(self, start_time: datetime.time, end_time: datetime.time):
        self.start = start_time
        self.end = end_time

    def is_overlapping(self, other):
        return self.start <= other.start <= self.end or self.start <= other.end <= self.end

    def __str__(self):
        return f'{self.start}-{self.end}'

    def __repr__(self):
        return self.__str__()


class SubjectTime:
    def __init__(self, interval: TimeInterval, day: WeekDay, is_theory: bool = True):
        self.interval: TimeInterval = interval
        self.week_day: WeekDay = day
        self.is_theory = is_theory

    def __repr__(self):
        string = [self.week_day.value, self.interval.__str__()]
        if self.is_theory is not None:
            if self.is_theory:
                string.insert(0, 'درس(ت)')
            else:
                string.insert(0, 'درس(ع)')
        return ' '.join(string)


class ExamTime:
    def __init__(self, interval: TimeInterval, day: datetime.date):
        self.interval: TimeInterval = interval
        self.day: datetime.date = day

    def __repr__(self):
        return f'{self.day} {self.interval}'


class Subject:
    def __init__(self, name, units, id_num, group_id, master, times, exam_time, capacity, score=2):
        self.name: str = name
        self.units: int = units
        self.id_num: int = id_num
        self.group_id: int = group_id
        self.master: str = master
        self.times: List[SubjectTime] = times
        self.exam_time: ExamTime = exam_time
        self.capacity: float = capacity
        self.score: int = score

    def __repr__(self):
        string = f'شماره درس: {self.id_num}_{self.group_id}, نام: {self.name}, استاد: {self.master}'
        string += f'\nزمان: {self.times} , امتحان:{self.exam_time}'
        return string

    def __hash__(self):
        return hash([self.id_num, self.group_id])