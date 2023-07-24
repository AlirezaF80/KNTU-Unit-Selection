# KNTU Unit Selection

## Introduction

This is a project to help KNTU students select units based on a number of criteria. Using a backtracking algorithm, it will find the best units for each student, based on their input subjects and scores given to each one.

## Requirements

* Python 3.6+
* xlrd (pip install xlrd)
* xlwt (pip install xlwt)

## Usage

First you have to make a xls file with your units details inside.<br>
A sample file is provided, named `sample_units.xls`.

First parse the file and get the subjects' objects.

   ```python
from excelSubjectsParser import ExcelSubjectsParser

sheet_name = 'Sheet1'
parser = ExcelSubjectsParser('sample_units.xls', sheet_name)
subjects = parser.parse()
```

After that you use the units selection algorithm to get the units you want.
You have to provide two sort functions and a combination cleaner function:

* First sort function, sorts the possible combinations.
* Second sort function, sorts the subjects inside each combination.
* Third function, cleans the combinations (for example combinations with less than 12 units).

```python
from unitSelector import UnitSelector

unit_selector = UnitSelector(subjects, combs_sort_func, subjects_sort_func, clean_combs)
possible_combs = unit_selector.get_possible_combinations()
   ```

## Sample File Structure

The structure should be the same as the sample file:<br>

1. Subject's ID and group number are in the first column, separated by an underline.<br>
2. Subject's Name is the second column.<br>
3. Subject's Units is the third column.<br>
4. Teacher is the fourth column.<br>
5. Class Time intervals are in the fifth column, all of which are separated by commas.<br>
6. Exam's day and time are in the sixth column.<br>
7. Max Capacity is the seventh column.<br>
8. Number of Registrations is in the eighth column.<br>
9. Subject's Score is in the ninth column.<br>
   Score is a number you give each subject based on how much you want it. If set to 0, the subject will be skipped.<br>

```
ID_Group|Name|Units|Teacher|Class Times|Exam Time|Capacity|Registrations|Score
```
