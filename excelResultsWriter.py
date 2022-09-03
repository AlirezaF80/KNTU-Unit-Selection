import xlwt

from subject import WeekDay
from unitSelector import Combination


class ExcelResultsWriter:
    def __init__(self, excel_file_name: str, sub_sort_func):
        self.excel_file_name = excel_file_name
        self.sub_sort_func = sub_sort_func
        self.wb = xlwt.Workbook()

    def write_combination(self, comb: Combination, sheet_name: str):
        ws = self.wb.add_sheet(sheet_name)
        # first_row_titles = ['شماره', 'نام درس', 'واحدها', 'نام استاد', 'زمان ارائه', 'زمان امتحان', 'ثبت نام شده',
        #                     'ظرفیت', 'امتیاز']
        first_row_titles = ['شماره', 'نام درس', 'واحدها', 'نام استاد', 'زمان امتحان', 'ثبت نام شده',
                            'ظرفیت', 'امتیاز']
        for i, title in enumerate(first_row_titles):
            ws.write(0, i, title)
        subjects = sorted(comb.subjects, key=self.sub_sort_func)
        for i, s in enumerate(subjects):
            row = [f'{s.id_num}_{s.group_id}', s.name, s.units, s.teacher_name, s.exam_time, s.registered,
                   s.capacity, s.score]
            # row = [f'{s.id_num}_{s.group_id}', s.name, s.units, s.teacher_name, s.times, s.exam_time, s.registered,
            #        s.capacity, s.score]
            for j, cell in enumerate(row):
                ws.write(i + 1, j, str(cell))
        # Printing Combination's Info
        info_titles = ['زمان تلف شده', 'تعداد روزها', 'تعداد واحدها', 'امتیاز کل', 'میانگین روز های بین امتحانات',
                       'حداقل روز بین امتحانات']
        prep_exam_days = comb.days_between_exams()
        info_cells = [comb.spare_times(), len(comb.days), comb.units, comb.score,
                      sum(prep_exam_days) / len(prep_exam_days), min(prep_exam_days)]
        for i in range(len(info_titles)):
            ws.write(len(subjects) + 2, i, info_titles[i])
            ws.write(len(subjects) + 3, i, info_cells[i])

        # Printing Schedule
        for i, day in enumerate(WeekDay):
            ws.write(len(subjects) + 5, i + 1, str(day))
        subs_schedule = comb.get_schedule()
        intervals = set()
        for day in subs_schedule:
            for s in subs_schedule[day]:
                intervals.add(s.times[0].interval)
        intervals = sorted(intervals, key=lambda i: i.start)
        for i, interval in enumerate(intervals):
            ws.write(len(subjects) + 6 + i, 0, str(interval))
        for i, day in enumerate(WeekDay):
            for s in subs_schedule.get(day, []):
                ws.write(len(subjects) + 6 + intervals.index(s.times[0].interval), i + 1, s.name)

    def save_to_file(self):
        self.wb.save(self.excel_file_name)
