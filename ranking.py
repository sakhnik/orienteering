#!/usr/bin/env python

import xml.etree.ElementTree as ET
import re
from collections import OrderedDict
from pg_storage import PgStorage
from time_table import TimeTable
from tabulate import tabulate

ns = {"": "http://www.orienteering.org/datastandard/3.0"}
storage = PgStorage()
rank_table = TimeTable()


class Name:
    def __init__(self, el: ET.Element):
        self.id: int = int(el.find("./Person/Id", ns).text)
        self.family: str = el.find("./Person/Name/Family", ns).text
        self.given: str = el.find("./Person/Name/Given", ns).text
        self.club: str = el.find("./Organisation/Name", ns).text
        if not self.club:
            self.club = ""

    def full_name(self):
        return f"{self.family} {self.given}"

    def __hash__(self):
        return hash((self.family, self.given))

    def __eq__(self, other):
        return (self.family, self.given) == (other.family, other.given)

    def __ne__(self, other):
        return not (self == other)


def get_status(st: str) -> str:
    if st == "OK":
        return "OK"
    if st == "MissingPunch":
        return "MP"
    if st == "NotCompeting":
        return "NC"
    raise Exception(f"Unknown status {st}")


class Result:
    def __init__(self, el: ET.Element):
        self.name = Name(el)
        self.stage: int = 0
        self.time: float = float(el.find("./Result/Time", ns).text)
        self.time_behind: float = \
            float(el.find("./Result/TimeBehind", ns).text)
        self.rank: str = None
        try:
            self.position: int = int(el.find("./Result/Position", ns).text)
        except AttributeError:
            self.position: int = None
        self.status: str = get_status(el.find("./Result/Status", ns).text)


Competitors = list[Result]
ClassResults = OrderedDict[str, Competitors]
class_results: ClassResults = OrderedDict()

tree = ET.parse("results-iof-3.0.xml")
root = tree.getroot()
for class_res in root.findall("./ClassResult", ns):
    clname = class_res.find("./Class/Name", ns).text
    competitors = class_results.setdefault(clname, [])
    for person_res in class_res.findall("./PersonResult", ns):
        competitors.append(Result(person_res))


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


def is_class_junior(clname: str) -> bool:
    if clname == 'ЧН' or clname == "ЖН":
        return True
    m = re.match(r"[^0-9]*(\d+)", clname)
    if not m:
        return False   # студенти
    return int(m.group(1)) < 16


def rank_value(rank: str, is_junior: bool) -> float:
    if rank == "МСМК":
        return 150.0
    if rank == "МСУ":
        return 100.0
    if rank == "КМСУ":
        return 30.0
    if rank == "І":
        return 10.0
    if rank == "ІІ" or rank == "І-ю":
        return 3.0
    if rank == "ІІІ" or rank == "ІІ-ю":
        return 1.0
    if rank == "б/р":
        return 0.3
    if rank == "б/р ю":
        return 0.1
    return 0.1 if is_junior else 0.3


def calc_course_value(competitors: Competitors, is_junior: bool) -> float:
    valuable = [res for res in competitors if res.position]
    if len(valuable) < 3:
        return 0
    valuable = valuable[:12]
    total_value = 0
    for res in valuable:
        rank = storage.get_ranking(res.name.id)
        val = rank_value(rank, is_junior)
        total_value += val
    return total_value


headers = ["№", "Ім’я", "Розряд", "Клуб", "Час", "Місце", "Виконано"]
for clname, competitors in class_results.items():
    print()
    course_value = calc_course_value(competitors, is_class_junior(clname))
    course_rules = rank_table.get_course_rules(course_value)
    print(f"== {clname} (ранг = {course_value:.1f}) ==")
    table = []
    for idx, result in enumerate(competitors):
        name = result.name
        is_junior = is_class_junior(clname)
        if result.position:
            rank = rank_table.estimate_rank(result.time, competitors[0].time,
                                            is_junior, course_rules)
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
