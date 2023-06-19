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
from collections import OrderedDict
from tabulate import tabulate

stage_count: int = 4
ns = {"": "http://www.orienteering.org/datastandard/3.0"}


class TotalResult:
    def __init__(self, name: Name):
        self.name = name
        self.score: int = 0
        self.time: float = 0
        self.stages: list[Result] = [None] * stage_count
        self.best_stages: list[Result] = []

    def comparison_key(self) -> bool:
        return (len(self.best_stages), self.score, self.time)


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


headers = ["№", "Ім’я", "Клуб", "К-ть Е", "Час всього", "Бали", "Місце"]
for clname, competitors in class_results.items():
    print()
    print(f"== {clname} ==")
    competitors_ranged = sorted([item for item in competitors.items()],
                                key=lambda k: k[1].comparison_key(),
                                reverse=True)
    table = []
    prev_results = None
    place = 1
    for idx, (name, results) in enumerate(competitors_ranged):
        if prev_results and \
                prev_results.comparison_key() > results.comparison_key():
            place += 1
        prev_results = results
        table.append([idx + 1, name.full_name(), name.club,
                      len(results.best_stages),
                      format_time(results),
                      results.score,
                      place])
    print(tabulate(table, headers=headers))
