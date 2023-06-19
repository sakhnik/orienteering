from result_parser import Competitors
import re


class Course:
    def __init__(self, clname: str):
        self.is_junior = self.is_class_junior(clname)

    def is_class_junior(self, clname: str) -> bool:
        if clname == 'ЧН' or clname == "ЖН":
            return True
        m = re.match(r"[^0-9]*(\d+)", clname)
        if not m:
            return False   # студенти
        return int(m.group(1)) < 16

    def get_rank_value(self, rank: str) -> float:
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
        return 0.1 if self.is_junior else 0.3

    def calc_value(self, competitors: Competitors, storage) -> float:
        valuable = [res for res in competitors if res.position]
        if len(valuable) < 3:
            return 0
        valuable = valuable[:12]
        total_value = 0
        for res in valuable:
            rank = storage.get_ranking(res.name.id)
            val = self.get_rank_value(rank)
            total_value += val
        return total_value
