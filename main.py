import datetime
import time
from typing import Set

from excelResultsWriter import ExcelResultsWriter
from excelSubjectsParser import ExcelSubjectsParser
from subject import Subject
from unitSelector import UnitSelector, Combination


def write_results(file_name):
    results_file = open(file_name, 'w', encoding='UTF-8')
    for comb in possible_combs:
        units = sum([sub.units for sub in comb])
        score = sum([sub.score for sub in comb])
        results_file.write(f'{units} units, {score} score\n')
        for sub in comb:
            results_file.write(f'{sub.name}, {sub.exam_time}\n')
        for sub in comb:
            results_file.write(f'{sub.id_num}_{sub.group_id}, {sub.free_capacity}\n')
        results_file.write(f"{'_' * 50}\n")


def combs_sort_func(comb: Combination):
    return comb.units, comb.score, -comb.spare_times(), -len(comb.days)


def subjects_sort_func(subject: Subject):
    if subject.exam_time.day:
        return subject.exam_time.day
    return datetime.date(1401, 1, 1)


def clean_combs(all_combs: Set[Combination]) -> Set[Combination]:
    # Remove combinations with units less than 12 units.
    all_combs = set(filter(lambda c: c.units >= 12, all_combs))
    return all_combs


if __name__ == '__main__':
    subjects_file_name = 'units_example.xls'
    subs_sheet_name = 'Sheet1'
    combs_file_name = 'results_example.xls'

    subjects = ExcelSubjectsParser(subjects_file_name, subs_sheet_name).parse()
    subjects = set(subjects)
    subjects = set(filter(lambda s: s.free_capacity > 0, subjects))

    for sub in subjects:
        print(sub)
        print("_" * 100)

    start = time.time()
    unit_selector = UnitSelector(subjects, combs_sort_func, clean_combs)
    possible_combs = unit_selector.get_possible_combinations()
    print(f'It took {round(time.time() - start)}s.')

    # write_results(combs_file_name)
    # print(f'Results written to {combs_file_name}.')

    results_writer = ExcelResultsWriter(combs_file_name, subjects_sort_func)

    for i, comb in enumerate(possible_combs):
        results_writer.write_combination(comb, f'{i}-{comb.units}-{comb.score}-{comb.spare_times()}')
    results_writer.save_to_file()
