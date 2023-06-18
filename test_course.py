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
