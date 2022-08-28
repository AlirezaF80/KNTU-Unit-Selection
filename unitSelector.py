from typing import List, Set

from subject import Subject


class UnitSelector:
    def __init__(self, subjects: List[Subject], combs_sort_func=None, subject_sort_func=None):
        '''
        :param subjects: list of subjects to choose from
        :param combs_sort_func: function to sort the possible combinations
        :param subject_sort_func: function to sort the subjects in each combination
        '''
        self._subjects = subjects
        self._is_done = False
        self._possible_combs = []
        self._combs_sort_func = combs_sort_func
        self._subs_sort_func = subject_sort_func

    def get_possible_combinations(self) -> List[Set[Subject]]:
        if not self._is_done:
            self._calc_possible_combs(self._subjects, [])
            print(f'Calculated {len(self._possible_combs)} possible combinations.')
            self._possible_combs = self._clean_possible_combs(self._possible_combs)
            if self._combs_sort_func:
                # First sort the possible combinations by the sort function
                self._possible_combs = list(sorted(self._possible_combs, key=self._combs_sort_func))
                # Then sort the subjects in each combination by the sort function
                self._possible_combs = [list(sorted(comb, key=self._subs_sort_func)) for comb in self._possible_combs]
            self._is_done = True
            print(f'Reduced to {len(self._possible_combs)} combinations.')
        return self._possible_combs

    @staticmethod
    def _remove_duplicate_combs(possible_combs):
        possible_combs_set = []
        for comb in possible_combs:
            comb = set(comb)
            is_comb_available = False
            for i in possible_combs_set:
                if i == comb:
                    is_comb_available = True
                    break
            if not is_comb_available:
                possible_combs_set.append(comb)
        return possible_combs_set

    @staticmethod
    def _clean_possible_combs(combs: List[Set[Subject]]):
        combs = UnitSelector._remove_duplicate_combs(combs)
        combs = [c for c in combs if sum([s.units for s in c]) >= 12]
        # Ham Niazi Az OS va OS
        combs = [c for c in combs if
                 not ('1912024' in [s.id_num for s in c] and '1914009' not in [s.id_num for s in c])]
        return combs

    @staticmethod
    def _is_overlapping(sub1: Subject, sub2: Subject):
        for t1 in sub1.times:
            for t2 in sub2.times:
                if t2.week_day == t1.week_day and t1.interval.is_overlapping(t2.interval):
                    return True
        if sub1.exam_time.day is not None and sub2.exam_time.day is not None:
            if sub1.exam_time.day == sub2.exam_time.day and sub1.exam_time.interval.is_overlapping(
                    sub2.exam_time.interval):
                return True
        # To Avoid getting same subject of two different times
        if sub1.id_num == sub2.id_num:
            return True
        # Is both of them "ma-aref"?
        # Note: this doesn't handle the "danesh khanevade" and others not interfering
        if str(sub1.id_num).startswith('5514') and str(sub2.id_num).startswith('5514'):
            return True
        return False

    def _calc_possible_combs(self, subjects: List[Subject], chosen_subs: List[Subject]):
        if len(subjects) == 0:
            self._possible_combs.append(chosen_subs)
            return

        overlap_subs_num = 0
        for sub in subjects:
            do_overlap = False
            for chosen in chosen_subs:
                if self._is_overlapping(sub, chosen):
                    do_overlap = True
                    overlap_subs_num += 1
                    break
            if sub.capacity == 0:
                continue
            if not do_overlap:
                new_subs = subjects.copy()
                new_subs.pop(new_subs.index(sub))
                new_chosen_subs = chosen_subs.copy()
                new_chosen_subs.append(sub)
                self._calc_possible_combs(new_subs, new_chosen_subs)
        if overlap_subs_num == len(subjects):
            self._possible_combs.append(chosen_subs)
            return
