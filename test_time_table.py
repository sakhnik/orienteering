from time_table import TimeTable, ranking_table


def test_get_course_rules():
    tt = TimeTable()
    assert tt.get_course_rules(0) == []
    assert tt.get_course_rules(0.99) == []
    assert tt.get_course_rules(1) == ranking_table[1][1]
    assert tt.get_course_rules(1.1) == ranking_table[1][1]
    assert tt.get_course_rules(1.9) == ranking_table[1][1]
    assert tt.get_course_rules(2.0) == ranking_table[2][1]
    assert tt.get_course_rules(12) == ranking_table[8][1]
    assert ranking_table[8][0] == 10
    assert tt.get_course_rules(1150) == ranking_table[-2][1]
    assert tt.get_course_rules(1200) == ranking_table[-1][1]
    assert tt.get_course_rules(1201) == ranking_table[-1][1]
    assert tt.get_course_rules(1500) == ranking_table[-1][1]
