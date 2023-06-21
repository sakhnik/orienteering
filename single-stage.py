#!/usr/bin/env python

from csv_storage import CsvStorage
from result_parser import Result, ClassResults
import result_parser
from course import Course
from rank_table import RankTable
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser(description='Multi-stage arguments')
parser.add_argument('--ranks', help='path to the ranks CSV file')
args = parser.parse_args()

storage = CsvStorage(args.ranks)
rank_table = RankTable()
class_results: ClassResults = result_parser.Parse("results-iof-3.0.xml")


def get_time(result: Result) -> int:
    if not result:
        return 0
    return result.time


def format_time(result: Result) -> str:
    seconds = int(result.time) % 60
    minutes = int(result.time // 60)
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"


headers = ["№", "Ім’я", "Розряд", "Клуб", "Час", "Місце", "Виконано"]
for clname, competitors in class_results.items():
    print()
    course = Course(clname)
    course_value = course.calc_value(competitors, storage)
    course_rules = rank_table.get_course_rules(course_value)
    print(f"== {clname} (ранг = {course_value:.1f}) ==")
    table = []
    for idx, result in enumerate(competitors):
        name = result.name
        if result.position:
            rank = rank_table.estimate_rank(
                float(result.time) / competitors[0].time,
                course.is_junior, course_rules
            )
        else:
            rank = ""
        position = result.get_position() if result.get_position() \
            else result.get_status()
        table.append([idx + 1,
                      result.get_name(),
                      storage.get_ranking(name.full_name()),
                      result.get_club(),
                      format_time(result),
                      position,
                      rank])
    print(tabulate(table, headers=headers))
