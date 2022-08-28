import xlwt

from unitSelector import Combination


class ExcelResultsWriter:
    def __init__(self, excel_file_name: str, sub_sort_func):
        self.excel_file_name = excel_file_name
        self.sub_sort_func = sub_sort_func
        self.wb = xlwt.Workbook()

    def write_combination(self, combination: Combination, sheet_name: str):
        ws = self.wb.add_sheet(sheet_name)
        first_row = ['نام درس', 'واحدها', 'نام استاد', 'زمان ارائه', 'زمان امتحان', 'ثبت نام شده', 'ظرفیت', 'امتیاز']
        for i, cell in enumerate(first_row):
            ws.write(0, i, cell)
        subjects = sorted(combination.subjects, key=self.sub_sort_func)
        for i, s in enumerate(subjects):
            row = [s.name, s.units, s.teacher_name, s.times, s.exam_time, s.registered, s.capacity, s.score]
            for j, cell in enumerate(row):
                ws.write(i + 1, j, str(cell))

    def save_to_file(self):
        self.wb.save(self.excel_file_name)
