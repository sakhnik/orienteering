#!/usr/bin/env python

from pg_storage import PgStorage
from result_parser import Result, ClassResults
import result_parser
from course import Course
from time_table import TimeTable
from tabulate import tabulate

storage = PgStorage()
rank_table = TimeTable()


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
            rank = rank_table.estimate_rank(result.time, competitors[0].time,
                                            course.is_junior, course_rules)
        else:
            rank = ""
        table.append([idx + 1,
                      name.full_name(),
                      storage.get_ranking(name.id),
                      name.club,
                      format_time(result),
                      result.position,
                      rank])
    print(tabulate(table, headers=headers))
