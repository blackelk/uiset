import pytest
from uiset import Endpoint, Interval, UISet, inf, unbounded


def test_uiset_init():

    s1 = UISet()
    s2 = UISet(s1)
    assert s1 == s2
    assert s1 is not s2

    s1 = UISet([Interval('[1, 2]')])
    s2 = UISet(s1)
    assert s1 == s2
    assert s1 is not s2

    s = UISet()
    assert s.intervals == []

    s = UISet([])
    assert s.intervals == []

    s = UISet([unbounded])
    assert s.intervals[0] == unbounded
    assert s.intervals[0] is not unbounded

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.intervals[0] is not i1
    assert s.intervals[1] is not i2

    i1 = Interval('[7, 9]')
    i2 = Interval('[1, 4]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.intervals[0] is not i1
    assert s.intervals[1] is not i2

    i1 = Interval('[1, 9]')
    i2 = Interval('[3, 5]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 9]')]

    i1 = Interval('[3, 5]')
    i2 = Interval('[1, 9]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 9]')]

    i1 = Interval('[1, 6]')
    i2 = Interval('[5, 8]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 8]')]

    i1 = Interval('[5, 8]')
    i2 = Interval('[1, 6]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 8]')]

    i1 = Interval('(0, 1)')
    i2 = Interval('(1, 2)')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('(0, 1)'), Interval('(1, 2)')]


def test_uiset_init_from_notation():

    s = UISet('[1, 2]')
    assert s.intervals == [Interval('[1, 2]')]

    s = UISet('[1, 2], (4, 5)')
    assert s.intervals == [Interval('[1, 2]'), Interval('(4, 5)')]

    s = UISet('[1, 2], [5, inf)')
    assert s.intervals == [Interval('[1, 2]'), Interval('[5, inf)')]


def test_uiset_init_from_notation_raises():

    with pytest.raises(ValueError):
        s = UISet('')
    with pytest.raises(ValueError):
        UISet('1')
    with pytest.raises(ValueError):
        UISet(',')
    with pytest.raises(ValueError):
        UISet('[1')
    with pytest.raises(ValueError):
        UISet('[1,')
    with pytest.raises(ValueError):
        UISet('[1, [2')
    with pytest.raises(ValueError):
        UISet('[1, 3], [2, 4]')
    with pytest.raises(ValueError):
        UISet('[1, 2], (2, 3)')
    with pytest.raises(ValueError):
        UISet('[1, 2), [2, 3)')


def test_uiset_repr():

    s = UISet()
    assert repr(s) == 'UISet([])'

    s = UISet([Interval('[1, 2.5)'), Interval('(2.5, 4]'), Interval('[7, 9]')])
    assert eval(repr(s)).intervals == s.intervals


def test_uiset_notation():

    s = UISet()
    assert s.notation == ''
    s.add(Interval('(-inf, 0)'))
    assert s.notation == '(-inf, 0)'
    s.add(Interval('[1, 2]'))
    assert s.notation == '(-inf, 0), [1, 2]'


def test_uiset_add():

    s = UISet()
    i1 = Interval('(-inf, 0)')
    s.add(i1)
    assert s.intervals == [i1]
    
    i2 = Interval('(-inf, 0)')
    s.add(i2)
    assert s.intervals == [i1]
    
    i3 = Interval('[-1, 0]')
    s.add(i3)
    assert s.intervals == [Interval('(-inf, 0]')]
    
    i4 = Interval('(0, 1)')
    s.add(i4)
    assert s.intervals == [Interval('(-inf, 1)')]
    
    i5 = Interval('(1, 2)')
    s.add(i5)
    assert s.intervals == [Interval('(-inf, 1)'), Interval('(1, 2)')]

    s = UISet([i4])
    s.add(i3)
    assert s.intervals == [Interval('[-1, 1)')]

    i6 = Interval('[0, 1)')
    i7 = Interval('[-1, 0)')
    s = UISet([i6])
    s.add(i7)
    assert s.intervals == [Interval('[-1, 1)')]

    i8 = Interval('(0, 1)')
    i9 = Interval('(-1, 0)')
    s = UISet([i8])
    s.add(i9)
    assert s.intervals == [Interval('(-1, 0)'), Interval('(0, 1)')]

    # Make sure original intervals has not changed.
    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(-inf, 0)')
    assert i3 == Interval('[-1, 0]')
    assert i4 == Interval('(0, 1)')
    assert i5 == Interval('(1, 2)')
    assert i6 == Interval('[0, 1)')
    assert i7 == Interval('[-1, 0)')
    assert i8 == Interval('(0, 1)')
    assert i9 == Interval('(-1, 0)')

    # Bulk test 1
    s0 = UISet('(4, 7)')
    tests = [
        ('(1, 2)', '(1, 2), (4, 7)'),
        ('(1, 4)', '(1, 4), (4, 7)'),
        ('(1, 4]', '(1, 7)'),
        ('(1, 5]', '(1, 7)'),
        ('(1, 7)', '(1, 7)'),
        ('(1, 7]', '(1, 7]'),
        ('(1, 8]', '(1, 8]'),
        ('(5, 6]', '(4, 7)'),
        ('(5, 7)', '(4, 7)'),
        ('(5, 7]', '(4, 7]'),
        ('(5, 8]', '(4, 8]'),
        ('(7, 9)', '(4, 7), (7, 9)'),
        ('[7, 9]', '(4, 9]'),
        ('[8, 9]', '(4, 7), [8, 9]'),
    ]
    for i_notation, res_notation in tests:
        s = s0.copy()
        interval = Interval(i_notation)
        s.add(interval)
        assert s.notation == res_notation

    # Bulk test 2
    s0 = UISet('(0, 4), (6, 8), (9, 10), (12, 15)')
    tests = [
        ('(-inf, -1]', '(-inf, -1], (0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 0)', '(-inf, 0), (0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 0]', '(-inf, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 1)', '(-inf, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 4)', '(-inf, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 4]', '(-inf, 4], (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 5]', '(-inf, 5], (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 6)', '(-inf, 6), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 6]', '(-inf, 8), (9, 10), (12, 15)'),
        ('(-inf, 7]', '(-inf, 8), (9, 10), (12, 15)'),
        ('(-inf, 8)', '(-inf, 8), (9, 10), (12, 15)'),
        ('(-inf, 8]', '(-inf, 8], (9, 10), (12, 15)'),
        ('(-inf, 13]', '(-inf, 15)'),
        ('(-inf, inf)', '(-inf, inf)'),
        ('[0, 1)', '[0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(0, 1)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('[0, 4)', '[0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(0, 4)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('[0, 4]', '[0, 4], (6, 8), (9, 10), (12, 15)'),
        ('(0, 4]', '(0, 4], (6, 8), (9, 10), (12, 15)'),
        ('[0, 5]', '[0, 5], (6, 8), (9, 10), (12, 15)'),
        ('(0, 5]', '(0, 5], (6, 8), (9, 10), (12, 15)'),
        ('[0, 6)', '[0, 6), (6, 8), (9, 10), (12, 15)'),
        ('(0, 6)', '(0, 6), (6, 8), (9, 10), (12, 15)'),
        ('[0, 6]', '[0, 8), (9, 10), (12, 15)'),
        ('(0, 6]', '(0, 8), (9, 10), (12, 15)'),
        ('[0, 13]', '[0, 15)'),
        ('(0, 13]', '(0, 15)'),
        ('(1, 2)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(1, 4)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(1, 4]', '(0, 4], (6, 8), (9, 10), (12, 15)'),
        ('(1, 5]', '(0, 5], (6, 8), (9, 10), (12, 15)'),
        ('(1, 7)', '(0, 8), (9, 10), (12, 15)'),
        ('(4, 5)', '(0, 4), (4, 5), (6, 8), (9, 10), (12, 15)'),
        ('[4, 5)', '(0, 5), (6, 8), (9, 10), (12, 15)'),
        ('(4, 6)', '(0, 4), (4, 6), (6, 8), (9, 10), (12, 15)'),
        ('[4, 6]', '(0, 8), (9, 10), (12, 15)'),
        ('(15, 16)', '(0, 4), (6, 8), (9, 10), (12, 15), (15, 16)'),
        ('[15, 16)', '(0, 4), (6, 8), (9, 10), (12, 16)'),
    ]
    for i_notation, res_notation in tests:
        s = s0.copy()
        interval = Interval(i_notation)
        s.add(interval)
        assert s.notation == res_notation


def test_uiset_bool():

    s = UISet()
    assert bool(s) is False

    s.add(Interval('[1, 2]'))
    assert bool(s) is True


def test_uiset_inverse():

    i0 = Interval('(-inf, inf)')
    s = UISet([i0])
    assert (~s).intervals == []
    assert (~~s).intervals == s.intervals

    s = UISet()
    assert (~s).intervals == [i0]
    assert (~~s).intervals == s.intervals

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    expected = [Interval('(-inf, 1)'), Interval('(4, 7)'), Interval('(9, inf)')]
    assert (~s).intervals == expected
    assert (~~s).intervals == s.intervals

    i3 = Interval('[5, 8]')
    i4 = Interval('[1, 6]')
    s = UISet([i3, i4])
    assert (~s).intervals == [Interval('(-inf, 1)'), Interval('(8, inf)')]
    assert (~~s).intervals == s.intervals

    i5 = Interval('(0, 1)')
    i6 = Interval('(1, 2)')
    s = UISet([i5, i6])
    expected = [Interval('(-inf, 0]'), Interval('[1, 1]'), Interval('[2, inf)')]
    assert (~s).intervals == expected
    assert (~~s).intervals == s.intervals

    i7 = Interval('(-inf, 0)')
    s = UISet([i7])
    assert (~s).intervals == [Interval('[0, inf)')]
    assert (~~s).intervals == s.intervals

    i8 = Interval('[0, inf)')
    s = UISet([i8])
    assert (~s).intervals == [i7]
    assert (~~s).intervals == s.intervals

    assert i0 == Interval('(-inf, inf)')
    assert i1 == Interval('[1, 4]')
    assert i2 == Interval('[7, 9]')
    assert i3 == Interval('[5, 8]')
    assert i4 == Interval('[1, 6]')
    assert i5 == Interval('(0, 1)')
    assert i6 == Interval('(1, 2)')
    assert i7 == Interval('(-inf, 0)')
    assert i8 == Interval('[0, inf)')


def test_uiset_search():

    s = UISet()
    assert s.search(1) is None
    
    s = UISet([unbounded])
    assert s.search(1) == unbounded

    i1 = Interval('[0, 1]')
    i2 = Interval('(2, 3)')
    s = UISet([i1, i2])
    assert s.search(1) == i1
    assert s.search(2) is None
    assert s.search(2.5) == i2
    assert s.search(2.5, enumerated=True) == (1, i2)
    assert s.search(1, lo=1) is None
    assert s.search(2.5, hi=1) is None
    assert s.search(2.5, lo=1)


def test_uiset_contains_scalar():

    s = UISet()
    assert 1 not in s

    s = UISet([unbounded])
    assert 1 in s

    i1 = Interval('[1, 3]')
    s = UISet([i1])
    assert 0 not in s
    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s

    i2 = Interval('(5, 7)')
    s.add(i2)
    assert 0 not in s
    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s
    assert 5 not in s
    assert 6 in s
    assert 7 not in s

    i3 = Interval('(7, inf)')
    s.add(i3)
    assert 0 not in s
    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s
    assert 5 not in s
    assert 6 in s
    assert 7 not in s
    assert 100 in s
    assert inf not in s

    s = ~s
    assert 0 in s
    assert 1 not in s
    assert 2 not in s
    assert 3 not in s
    assert 4 in s
    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 100 not in s
    assert inf not in s


def test_uiset_contains_interval():

    s = UISet()
    assert Interval('(1, 2)') not in s

    s = UISet('(1, 4)')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') not in s
    assert Interval('(1, 4]') not in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s
    assert Interval('(0, 1)') not in s

    s = UISet('[1, 4)')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') in s
    assert Interval('(1, 4]') not in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s

    s = UISet('(1, 4]')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') not in s
    assert Interval('(1, 4]') in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s

    s = UISet('[1, 4]')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') in s
    assert Interval('(1, 4]') in s
    assert Interval('[1, 4]') in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s


def test_uiset_eq_and_ne():

    s1 = UISet()
    s2 = UISet()
    assert s1 == s2
    s1.add(Interval('[1, 2]'))
    assert s1 != s2

    s2 = UISet([Interval('[1, 2]')])
    assert s1 == s2

    s2.discard(2)
    assert s1 != s2

    assert not s1 == 0
    assert s1 != 0


def test_uiset_discard():

    i1 = Interval('[0, 2]')
    s = UISet([i1])
    s.discard(0)
    assert s.intervals == [Interval('(0, 2]')]
    s.discard(2)
    assert s.intervals == [Interval('(0, 2)')]
    s.discard(1)
    s.discard(-1)
    assert s.intervals == [Interval('(0, 1)'), Interval('(1, 2)')]
    i2 = Interval('[2, inf)')
    s.add(i2)
    s.discard(inf)
    assert s.intervals == [Interval('(0, 1)'), Interval('(1, inf)')]

    assert i1 == Interval('[0, 2]')
    assert i2 == Interval('[2, inf)')


def test_uiset_clear():

    i1 = Interval('[0, 1]')
    i2 = Interval('[2, 3]')
    s = UISet([i1, i2])
    s.clear()
    assert s.intervals == []


def test_uiset_copy():

    s1 = UISet()
    s2 = s1.copy()
    assert s1 == s2
    assert s1 is not s2

    i = Interval('[1, 2]')
    s1 = UISet([i])
    s2 = s1.copy()
    assert s1 == s2
    assert s2.intervals[0] is not i

    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    a = Endpoint(None, l1, True, True)
    b = Endpoint(None, l2, True, False)
    i = Interval(None, a, b)
    s1 = UISet([i])
    s2 = s1.copy()
    s2.intervals[0].a.value[2] = -1
    assert i.a.value[2] == -1


def test_uiset_ge():

    assert UISet() >= UISet()
    assert not UISet() >= UISet('[1, 2]')
    assert UISet('(1, 6)') >= UISet()
    assert UISet('(1, 6)') >= UISet('(2, 3)')
    assert UISet('(1, 6)') >= UISet('(2, 3), (4, 5)')
    assert UISet('(1, 6)') >= UISet('(1, 3), (4, 6)')
    assert UISet('(1, 6)') >= UISet('(1, 6)')
    assert not UISet('(1, 6)') >= UISet('(4, 6]')
    assert not UISet('(1, 6)') >= UISet('(1, 6]')
    assert not UISet('(1, 6)') >= UISet('[1, 6)')
    assert not UISet('(1, 6)') >= UISet('[1, 6]')
    assert not UISet('(1, 6)') >= UISet('[2, 7]')
    assert UISet('(2, 4), (4, 6)') >= UISet('(2, 4), (4, 6)')
    assert UISet('(2, 4), (4, 6)') >= UISet('(2, 3), (3, 4), (4, 6)')
    assert not UISet('(2, 4), (4, 6)') >= UISet('(1, 3)')
    assert not UISet('(2, 4), (4, 6)') >= UISet('(3, 5)')
    assert not UISet('(2, 4), (4, 6)') >= UISet('(5, 7)')
    assert UISet('[1, 2]') >= UISet('(1, 2)')
    assert UISet('[1, 2]') >= UISet('[1, 2]')
    assert UISet('[1, inf)') >= UISet('[1, 10]')
    assert not UISet('[1, inf)') >= UISet('(0, 10]')

    with pytest.raises(TypeError):
        UISet() >= 0
    with pytest.raises(TypeError):
        UISet() >= -inf
    inf >= UISet()


def test_uiset_le():

    assert UISet() <= UISet()
    assert UISet() <= UISet('[1, 2]')
    assert not UISet('(1, 6)') <= UISet()
    assert not UISet('(1, 6)') <= UISet('(2, 3)')
    assert not UISet('(1, 6)') <= UISet('(2, 3), (4, 5)')
    assert not UISet('(1, 6)') <= UISet('(1, 3), (4, 6)')
    assert UISet('(1, 6)') <= UISet('(1, 6)')
    assert not UISet('(1, 6)') <= UISet('(4, 6]')
    assert UISet('(1, 6)') <= UISet('(1, 6]')
    assert UISet('(1, 6)') <= UISet('[1, 6)')
    assert UISet('(1, 6)') <= UISet('[1, 6]')
    assert not UISet('(1, 6)') <= UISet('[2, 7]')
    assert UISet('(2, 4), (4, 6)') <= UISet('(2, 4), (4, 6)')
    assert not UISet('(2, 4), (4, 6)') <= UISet('(2, 3), (3, 4), (4, 6)')
    assert not UISet('(2, 4), (4, 6)') <= UISet('(1, 3)')
    assert not UISet('(2, 4), (4, 6)') <= UISet('(3, 5)')
    assert not UISet('(2, 4), (4, 6)') <= UISet('(5, 7)')
    assert not UISet('[1, 2]') <= UISet('(1, 2)')
    assert UISet('[1, 2]') <= UISet('[1, 2]')
    assert not UISet('[1, inf)') <= UISet('[1, 10]')
    assert not UISet('[1, inf)') <= UISet('(0, 10]')

    with pytest.raises(TypeError):
        0 <= UISet()


def test_uiset_issuperset():

    assert UISet('[1, 3]').issuperset(UISet('(1, 3)'))
    assert not UISet().issuperset(UISet('(1, 3)'))


def test_uiset_issubset():

    assert not UISet('[1, 3]').issubset(UISet('(1, 3)'))
    assert UISet().issubset(UISet('(1, 3)'))

