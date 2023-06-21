from rank_table import RankTable, time_table


def test_get_course_rules():
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
