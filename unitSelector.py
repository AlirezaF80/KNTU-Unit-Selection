from typing import Set, List

from subject import Subject


class Combination:
    def __init__(self, subjects: Set[Subject]):
        self._subjects = frozenset(subjects)

    @property
    def subjects(self):
        return self._subjects

    @property
    def units(self):
        return sum(subject.units for subject in self._subjects)

    @property
    def score(self):
        return sum(subject.score for subject in self._subjects)

    def __contains__(self, item):
        return item in self._subjects

    def __iter__(self):
        return iter(self._subjects)

    def __eq__(self, other):
        return self.subjects == other.subjects

    def __len__(self):
        return len(self._subjects)

    def __hash__(self):
        return hash(self._subjects)


class UnitSelector:
    def __init__(self, subjects: Set[Subject], combs_sort_func=None, clean_combs_func=None):
        '''
        :param subjects: list of subjects to choose from
        :param combs_sort_func: function to sort the possible combinations
        '''
        self._subjects: Set[Subject] = subjects
        self._possible_combs: Set[Combination] = set()
        self._combs_sort_func = combs_sort_func
        self._clean_possible_combs = clean_combs_func
        self._is_done = False

    def get_possible_combinations(self) -> List[Combination]:
        if not self._is_done:
            self._calc_possible_combs(self._subjects, set())
            print(f'Calculated {len(self._possible_combs)} possible combinations.')
            self._possible_combs = self._clean_possible_combs(self._possible_combs)
            if self._combs_sort_func:
                # First sort the possible combinations by the sort function
                self._possible_combs = list(sorted(self._possible_combs, key=self._combs_sort_func))
            self._is_done = True
            print(f'Reduced to {len(self._possible_combs)} combinations.')
        return self._possible_combs

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

    def _calc_possible_combs(self, subjects: Set[Subject], chosen_subs: Set[Subject]):
        if len(subjects) == 0:
            self._possible_combs.add(Combination(chosen_subs))
            return

        overlap_subs = set()
        for sub in subjects:
            do_overlap = False
            for chosen in chosen_subs:
                if self._is_overlapping(sub, chosen):
                    do_overlap = True
                    overlap_subs.add(sub)
                    break
            if not do_overlap:
                subs_cpy = subjects.copy()
                subs_cpy.remove(sub)
                chosen_subs_cpy = chosen_subs.copy()
                chosen_subs_cpy.add(sub)
                self._calc_possible_combs(subs_cpy, chosen_subs_cpy)
        if len(overlap_subs) == len(subjects):
            self._possible_combs.add(Combination(chosen_subs))
            return
