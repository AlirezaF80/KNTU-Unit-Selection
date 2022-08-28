import datetime
import time

from excelSubjectsParser import ExcelSubjectsParser
from subject import Subject
from unitSelector import UnitSelector


def write_results(file_name):
    results_file = open(file_name, 'w', encoding='UTF-8')
    for comb in possible_combs:
        units = sum([sub.units for sub in comb])
        score = sum([sub.score for sub in comb])
        results_file.write(f'{units} units, {score} score\n')
        for sub in comb:
            results_file.write(f'{sub.name}, {sub.exam_time}\n')
        for sub in comb:
            results_file.write(f'{sub.id_num}_{sub.group_id}, {sub.capacity}\n')
        results_file.write(f"{'_' * 50}\n")


def sort_func(comb):
    score = 0
    for sub in comb:
        # if sub.capacity == 0:
        #     continue
        # score += sub.capacity * sub.score
        # score += sub.units * sub.score
        score += sub.units * 1000 + sub.score
        # score += sub.units
        # score += sub.score
        # score += len(comb)
    return score


def comb_sort_func(subject: Subject):
    if subject.exam_time.day:
        return subject.exam_time.day
    return datetime.date(1400, 1, 1)


if __name__ == '__main__':
    results_file_name = 'results.txt'
    excel_file_name = 'units_example.xls'
    sheet_name = 'Sheet1'

    subjects = ExcelSubjectsParser(excel_file_name, sheet_name).parse()

    start = time.time()
    unit_selector = UnitSelector(subjects, sort_func, comb_sort_func)
    possible_combs = unit_selector.get_possible_combinations()
    print(f'It took {round(time.time() - start)}s.')

    write_results(results_file_name)
