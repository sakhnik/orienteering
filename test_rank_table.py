from rank_table import RankTable, time_table, point_table


def test_get_course_rules_time():
    tt = RankTable()
    assert tt.get_course_rules(0) == []
    assert tt.get_course_rules(0.99) == []
    assert tt.get_course_rules(1) == time_table[1][1]
    assert tt.get_course_rules(1.1) == time_table[1][1]
    assert tt.get_course_rules(1.9) == time_table[1][1]
    assert tt.get_course_rules(2.0) == time_table[2][1]
    assert tt.get_course_rules(12) == time_table[8][1]
    assert time_table[8][0] == 10
    assert tt.get_course_rules(1150) == time_table[-2][1]
    assert tt.get_course_rules(1200) == time_table[-1][1]
    assert tt.get_course_rules(1201) == time_table[-1][1]
    assert tt.get_course_rules(1500) == time_table[-1][1]


def test_get_course_rules_points():
    tt = RankTable(False)
    assert tt.get_course_rules(0) == []
    assert tt.get_course_rules(0.99) == []
    assert tt.get_course_rules(1) == point_table[1][1]
    assert tt.get_course_rules(1.1) == point_table[1][1]
    assert tt.get_course_rules(1.9) == point_table[1][1]
    assert tt.get_course_rules(2.0) == point_table[2][1]
    assert tt.get_course_rules(12) == point_table[8][1]
    assert point_table[8][0] == 10
    assert tt.get_course_rules(1150) == point_table[-2][1]
    assert tt.get_course_rules(1200) == point_table[-1][1]
    assert tt.get_course_rules(1201) == point_table[-1][1]
    assert tt.get_course_rules(1500) == point_table[-1][1]
