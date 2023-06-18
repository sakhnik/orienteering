from bisect import bisect

ranking_table = [
    (0,    []),
    (1,    [0.00, 0.00, 0.00, 0.00, 1.14]),
    (2,    [0.00, 0.00, 0.00, 0.00, 1.23]),
    (3,    [0.00, 0.00, 0.00, 1.05, 1.29]),
    (4,    [0.00, 0.00, 0.00, 1.08, 1.32]),
    (5,    [0.00, 0.00, 0.00, 1.11, 1.35]),
    (6,    [0.00, 0.00, 0.00, 1.14, 1.38]),
    (8,    [0.00, 0.00, 0.00, 1.17, 1.42]),
    (10,   [0.00, 0.00, 1.00, 1.20, 1.46]),
    (13,   [0.00, 0.00, 1.02, 1.23, 1.50]),
    (16,   [0.00, 0.00, 1.05, 1.26, 1.54]),
    (20,   [0.00, 0.00, 1.08, 1.29, 1.58]),
    (25,   [0.00, 0.00, 1.11, 1.32, 1.62]),
    (32,   [0.00, 0.00, 1.14, 1.35, 1.66]),
    (36,   [0.00, 1.00, 1.17, 1.38, 1.70]),
    (50,   [0.00, 1.02, 1.20, 1.42, 1.74]),
    (63,   [0.00, 1.05, 1.23, 1.46, 1.79]),
    (80,   [0.00, 1.08, 1.26, 1.50, 1.84]),
    (100,  [0.00, 1.11, 1.29, 1.54, 1.89]),
    (120,  [1.00, 1.14, 1.32, 1.58, 1.94]),
    (160,  [1.02, 1.17, 1.35, 1.62, 1.99]),
    (200,  [1.05, 1.20, 1.38, 1.66, 2.04]),
    (250,  [1.08, 1.23, 1.42, 1.70, 1.09]),
    (320,  [1.11, 1.26, 1.46, 1.74, 2.14]),
    (400,  [1.14, 1.29, 1.50, 1.79, 2.19]),
    (500,  [1.17, 1.32, 1.54, 1.84, 2.24]),
    (630,  [1.20, 1.35, 1.58, 1.89, 9999]),
    (800,  [1.23, 1.38, 1.62, 1.94, 9999]),
    (1000, [1.26, 1.41, 1.66, 1.99, 9999]),
    (1100, [1.29, 1.44, 1.70, 2.04, 9999]),
    (1200, [1.31, 1.47, 1.74, 2.09, 9999]),
]


class TimeTable:
    def __init__(self):
        pass

    def get_course_rules(self, course_value: float) -> [float]:
        idx = bisect(ranking_table, course_value, key=lambda v: v[0])
        if idx >= len(ranking_table):
            return ranking_table[-1][1]
        if idx <= 0:
            idx = 1
        return ranking_table[idx - 1][1]

    def estimate_rank(self, time: int, leader_time: int, is_junior: bool,
                      course_rules: [float]) -> str:
        if not course_rules:
            return ""
        ratio = float(time) / leader_time
        if ratio <= course_rules[0]:
            return "КМСУ"
        if ratio <= course_rules[1]:
            return "І"
        if not is_junior:
            if ratio <= course_rules[2]:
                return "ІІ"
            if ratio <= course_rules[3]:
                return "ІІІ"
        else:
            if ratio <= course_rules[2]:
                return "І-ю"
            if ratio <= course_rules[3]:
                return "ІІ-ю"
            if ratio <= course_rules[4]:
                return "ІІІ-ю"
        return ""
