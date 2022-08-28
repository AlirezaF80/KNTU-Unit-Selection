import datetime
import re
from typing import List

import xlrd
from xlrd.sheet import Sheet

from subject import Subject, TimeInterval, WeekDay, SubjectTime, ExamTime


class ExcelSubjectsParser:
    def __init__(self, excel_file_path, excel_sheet_name):
        self._file_path = excel_file_path
        self._sheet_name = excel_sheet_name

    def parse(self) -> List[Subject]:
        sheet = self._read_excel_sheet(self._file_path, self._sheet_name)
        return self._parse_excel_file(sheet)

    @staticmethod
    def _read_excel_sheet(file_path, sheet_name):
        workbook = xlrd.open_workbook_xls(file_path)
        sheet = workbook.sheet_by_name(sheet_name)
        return sheet

    @staticmethod
    def _parse_excel_file(sheet: Sheet):
        subjects: List[Subject] = []
        for i in range(1, sheet.nrows):
            row_values = sheet.row_values(i)
            subject = ExcelSubjectsParser._parse_excel_row(row_values)
            if subject.score == 0:
                continue
            subjects.append(subject)
        return subjects

    @staticmethod
    def _parse_excel_row(row):
        # Get Subject's score given by the user
        score = int(row[8])
        # Get Subject's id and group
        sub_id = ExcelSubjectsParser._replace_persian_nums(row[0].split('_')[0])
        sub_group = ExcelSubjectsParser._replace_persian_nums(row[0].split('_')[1])
        # Get Subject's Name
        sub_name = row[1]
        # Get Subject's Units
        units = int(row[2])
        # Get Subject's Master name
        master_name = row[3]
        # Get Subject's Times
        intervals = ExcelSubjectsParser._get_subject_times(row)
        # Get Subject's Exam Time
        exam_time = ExcelSubjectsParser._get_exam_time(row[5])
        # Get Subject's Capacity
        free_capacity = ExcelSubjectsParser._get_free_capacity(row)
        subject = Subject(sub_name, units, sub_id, sub_group, master_name, intervals, exam_time, free_capacity, score)
        return subject

    @staticmethod
    def _get_free_capacity(row) -> float:
        try:
            total_capacity = int(row[6])
            registered_num = int(row[7])
            # registered_num = min(registered_num, total_capacity)
            return 1 - (registered_num / total_capacity)
        except Exception:
            return 1

    @staticmethod
    def _get_subject_times(row) -> List[SubjectTime]:
        times = [t.strip() for t in row[4].split('،')]
        sub_times = []
        for time_string in times:
            subject_time = ExcelSubjectsParser._parse_subject_time(time_string)
            sub_times.append(subject_time)
        return sub_times

    @staticmethod
    def _parse_subject_time(time_string) -> SubjectTime:
        is_theory = None
        if time_string.startswith('درس(ت)'):
            is_theory = True
            time_string = time_string.replace('درس(ت)', '')
        elif time_string.startswith('درس(ع)'):
            is_theory = False
            time_string = time_string.replace('درس(ع)', '')
        weekday: WeekDay = WeekDay.NOT_FOUND
        for day in WeekDay:
            if time_string.find(day.value) != -1:
                weekday = day
        time_string = time_string.replace(weekday.value, '')
        interval = ExcelSubjectsParser._get_time_interval(time_string)
        subject_time = SubjectTime(interval, weekday, is_theory)
        return subject_time

    @staticmethod
    def _get_time_interval(string):
        time = ExcelSubjectsParser._replace_persian_nums(string)
        time = re.findall(r'\d+:\d+\s*-\s*\d+:\d+', string=time)
        if not time:
            return None
        time = time[0]
        start, end = time.split('-')[0].split(':'), time.split('-')[1].split(':')
        start_time = datetime.time(int(start[0]), int(start[1]))
        end_time = datetime.time(int(end[0]), int(end[1]))
        interval = TimeInterval(start_time, end_time)
        return interval

    @staticmethod
    def _get_exam_time(exam_time_str: str):
        interval = ExcelSubjectsParser._get_time_interval(exam_time_str)
        exam_time_str = ExcelSubjectsParser._replace_persian_nums(exam_time_str)

        date_pat = '(\d{4})\/(\d{1,2})\/([0-3]?\d)'
        date = re.findall(date_pat, string=exam_time_str)
        if not date:
            return ExamTime(interval, None)
        date = date[0]
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        return ExamTime(interval, date)

    @staticmethod
    def _replace_persian_nums(string: str):
        new_str = ''
        for c in string:
            if ord('۰') <= ord(c) <= ord('۰') + 9:
                new_str += str(ord(c) - ord('۰'))
            else:
                new_str += c
        return new_str
