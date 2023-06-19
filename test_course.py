from course import Course


def test_is_junior():
    assert Course('ЧН').is_junior
    assert Course('ЖН').is_junior
    assert not Course('ЧСт').is_junior
    assert not Course('ЖСт').is_junior
    assert Course("Ч14").is_junior
    assert Course("Ж14").is_junior
    assert not Course("Ч16").is_junior
    assert not Course("Ж16").is_junior
    assert not Course("Ч21").is_junior
    assert not Course("Ж21").is_junior


def test_get_rank_value():
    assert 150.0 == Course("Ч21").get_rank_value("МСМК")
    assert 150.0 == Course("Ж21").get_rank_value("МСМК")
    assert 100.0 == Course("Ч21").get_rank_value("МСУ")
    assert 100.0 == Course("Ж21").get_rank_value("МСУ")
    assert 30.0 == Course("Ч21").get_rank_value("КМСУ")
    assert 30.0 == Course("Ж21").get_rank_value("КМСУ")
    assert 10.0 == Course("Ч21").get_rank_value("І")
    assert 10.0 == Course("Ж21").get_rank_value("І")
    assert 3.0 == Course("Ч18").get_rank_value("ІІ")
    assert 3.0 == Course("Ж18").get_rank_value("ІІ")
    assert 1.0 == Course("Ч16").get_rank_value("ІІІ")
    assert 1.0 == Course("Ж16").get_rank_value("ІІІ")
    assert 1.0 == Course("Ч14").get_rank_value("ІІ-ю")
    assert 1.0 == Course("Ж14").get_rank_value("ІІ-ю")
    assert 0.3 == Course("Ч16").get_rank_value("")
    assert 0.3 == Course("Ж16").get_rank_value("")
    assert 0.1 == Course("Ч14").get_rank_value("")
    assert 0.1 == Course("Ж14").get_rank_value("")
