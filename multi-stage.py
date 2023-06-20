#!/usr/bin/env python

# Підрахунок очок і обчислення місць учасників багатоетапних
# змагань зі спортивного орієнтування.

# Запуск:
#  - Експортувати результати етапів у файли e1-results-iof-3.0.xml,…
#  - Задати кількість етапів у змінній stage_count
#  - Запустити ./summary.py
# Таблицю буде надруковано в текстовому вигляді у стандартний вивід stdout

# Система підрахунку очок: 1 місце - 45 очок, 2 місце - 42 очок,
# 3 місце - 40 очок, 4 місце - 38 очок, 5 місце -36 очок,
# 6 місце - 35 очок, ..., 40 місце - 1 очко (Таблиця No 1 Правил змагань).
# У разі рівності очок перевага надається учасникам, які мають менший
# сумарний час проходження трьох кращих дистанцій.


from result_parser import Name, Result, ClassResults
import result_parser
from pg_storage import PgStorage
from course import Course
from rank_table import RankTable
from collections import OrderedDict
from tabulate import tabulate

stage_count: int = 4
storage = PgStorage()
rank_table = RankTable(False)


class TotalResult:
    def __init__(self, name: Name):
        self.name = name
        self.score: int = 0
        self.time: float = 0
        self.stages: list[Result] = [None] * stage_count
        self.best_stages: list[Result] = []
        self.position = None

    def comparison_key(self) -> bool:
        return (len(self.best_stages), self.score, self.time)

    def get_name(self) -> str:
        return self.name.full_name()

    def get_club(self) -> str:
        return self.name.club

    def get_result(self) -> int:
        return self.score

    def get_position(self) -> int:
        return self.position

    def get_status(self) -> str:
        return "OK"


Competitors = dict[Name, TotalResult]
ClassTotalResults = OrderedDict[str, Competitors]
class_results: ClassResults = OrderedDict()

for stage in range(stage_count):
    fname = f"e{stage+1}-results-iof-3.0.xml"
    results: ClassResults = result_parser.Parse(fname)
    for clname, stage_competitors in results.items():
        competitors = class_results.setdefault(clname, {})
        for person_res in stage_competitors:
            name = person_res.name
            try:
                results = competitors[name]
            except KeyError:
                results = competitors[name] = TotalResult(name)
            results.stages[stage] = person_res


def get_score(result: Result) -> int:
    if not result:
        return 0
    position = result.position
    if position == 1:
        return 45
    if position == 2:
        return 42
    if position == 3:
        return 40
    if position == 4:
        return 38
    if not position or position > 40:
        return 0
    return 41 - position


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


for clname, competitors in class_results.items():
    for name, results in competitors.items():
        results.stages.sort(key=lambda k: (get_score(k), get_time(k)),
                            reverse=True)
        best_stages = [r for r in results.stages if r][0:3]
        results.best_stages = best_stages
        results.score = sum((get_score(s) for s in best_stages))
        results.time = sum((get_time(s) for s in best_stages))


final_results = OrderedDict()
for clname, competitors in class_results.items():
    competitors_ranged = sorted([res for res in competitors.values()],
                                key=lambda k: k.comparison_key(),
                                reverse=True)
    final_results[clname] = competitors_ranged

for clname, competitors in final_results.items():
    prev_result = None
    position = 1
    for idx, result in enumerate(competitors):
        if not result.get_result():
            break
        if prev_result and \
                prev_result.comparison_key() > result.comparison_key():
            position = result.position = idx + 1
        else:
            result.position = position
        prev_result = result

headers = ["№", "Ім’я", "Розряд", "Клуб", "К-ть Е", "Час всього", "Бали",
           "Місце", "Виконано"]
for clname, competitors in final_results.items():
    print()
    course = Course(clname)
    course_value = course.calc_value(competitors, storage)
    course_rules = rank_table.get_course_rules(course_value)
    print(f"== {clname} (ранг = {course_value:.1f}) ==")
    table = []
    for idx, result in enumerate(competitors):
        if result.position:
            rank = rank_table.estimate_rank(
                float(result.get_result()) / competitors[0].get_result(),
                course.is_junior, course_rules
            )
        else:
            rank = ""
        table.append([idx + 1, result.get_name(),
                      storage.get_ranking(result.get_name()),
                      result.get_club(),
                      len(result.best_stages),
                      format_time(result),
                      result.get_result(),
                      result.get_position(),
                      rank])
    print(tabulate(table, headers=headers))
