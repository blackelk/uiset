import datetime
import sys
import pytest

from uiset import Endpoint, Interval

_ver = sys.version_info
is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)


def test_interval_repr():

    i1 = Interval('[1, 2]')
    i2 = Interval('[1, 2)')
    i3 = Interval('(1, 2]')
    i4 = Interval('(1, 2)')
    i5 = Interval('(-inf, 2)')
    i6 = Interval('(1, inf)')
    a = Endpoint(None, 'A', False, True)
    b = Endpoint(None, 'Z', False, False)
    i7 = Interval(None, a=a, b=b)

    assert repr(i1) == "Interval('[1, 2]')"
    assert repr(i2) == "Interval('[1, 2)')"
    assert repr(i3) == "Interval('(1, 2]')"
    assert repr(i4) == "Interval('(1, 2)')"
    assert repr(i5) == "Interval('(-inf, 2)')"
    assert repr(i6) == "Interval('(1, inf)')"
    assert repr(i7) == "Interval(None, Endpoint(None, 'A', False, True), Endpoint(None, 'Z', False, False))"

    assert eval(repr(i1)) == i1
    assert eval(repr(i2)) == i2
    assert eval(repr(i3)) == i3
    assert eval(repr(i4)) == i4
    assert eval(repr(i5)) == i5
    assert eval(repr(i6)) == i6
    assert eval(repr(i7)) == i7


def test_interval_init_raises():

    with pytest.raises(ValueError):
        Interval('[6]')
    with pytest.raises(TypeError):
        Interval(a=1, b='')
    with pytest.raises(TypeError):
        Interval('[1, 2]', Endpoint('[1'))
    with pytest.raises(TypeError):
        Interval('[1, 2]', Endpoint('[1'), Endpoint('2]'))
    with pytest.raises(ValueError):
        Interval(a=Endpoint('[1'), b=Endpoint('[2'))
    with pytest.raises(ValueError):
        Interval(a=Endpoint('[1'), b=Endpoint('[0'))


def test_interval_eq():

    assert Interval('[1, 2]') == Interval('[1, 2]')
    assert Interval('[1, 2)') == Interval('[1, 2)')
    assert Interval('(1, 2]') == Interval('(1, 2]')
    assert Interval('(1, 2)') == Interval('(1, 2)')
    assert Interval('[1, 2]') != Interval('[1, 2)')
    assert Interval('[1, 2]') != Interval('(1, 2]')
    assert Interval('[1, 2]') != Interval('(1, 2)')
    assert Interval('[1, 2]') != Interval('[1, 3]')


def test_scalar_in_interval():

    assert 0 not in Interval('[1, 2]')
    assert 0 not in Interval('[1, 2)')
    assert 0 not in Interval('(1, 2]')
    assert 0 not in Interval('(1, 2)')
    assert 1 in Interval('[1, 2]')
    assert 1 in Interval('[1, 2)')
    assert 1 not in Interval('(1, 2]')
    assert 1 not in Interval('(1, 2)')
    assert 2 in Interval('[1, 2]')
    assert 2 not in Interval('[1, 2)')
    assert 2 in Interval('(1, 2]')
    assert 2 not in Interval('(1, 2)')
    assert 3 not in Interval('[1, 2]')
    assert 3 not in Interval('[1, 2)')
    assert 3 not in Interval('(1, 2]')
    assert 3 not in Interval('(1, 2)')
    

def test_endpoint_in_interval():

    assert Endpoint('[0') not in Interval('[1, 3]')
    assert Endpoint('(0') not in Interval('[1, 3]')
    assert Endpoint('0]') not in Interval('[1, 3]')
    assert Endpoint('0)') not in Interval('[1, 3]')
    assert Endpoint('[1') in Interval('[1, 3]')
    assert Endpoint('(1') in Interval('[1, 3]')
    assert Endpoint('1]') in Interval('[1, 3]')
    assert Endpoint('1)') not in Interval('[1, 3]')
    assert Endpoint('[2') in Interval('[1, 3]')
    assert Endpoint('(2') in Interval('[1, 3]')
    assert Endpoint('2]') in Interval('[1, 3]')
    assert Endpoint('2)') in Interval('[1, 3]')
    assert Endpoint('[3') in Interval('[1, 3]')
    assert Endpoint('(3') not in Interval('[1, 3]')
    assert Endpoint('3]') in Interval('[1, 3]')
    assert Endpoint('3)') in Interval('[1, 3]')
    assert Endpoint('[4') not in Interval('[1, 3]')
    assert Endpoint('(4') not in Interval('[1, 3]')
    assert Endpoint('4]') not in Interval('[1, 3]')
    assert Endpoint('4)') not in Interval('[1, 3]')


def test_interval_in_interval():

    assert Interval('[1, 2]') in Interval('[1, 2]')
    assert Interval('[1, 2]') not in Interval('[1, 2)')
    assert Interval('[1, 2]') not in Interval('(1, 2]')
    assert Interval('[1, 2]') not in Interval('(1, 2)')
    assert Interval('[1, 2)') in Interval('[1, 2]')
    assert Interval('[1, 2)') in Interval('[1, 2)')
    assert Interval('[1, 2)') not in Interval('(1, 2)')
    assert Interval('[1, 2)') not in Interval('(1, 2)')
    assert Interval('(1, 2]') in Interval('[1, 2]')
    assert Interval('(1, 2]') not in Interval('[1, 2)')
    assert Interval('(1, 2]') in Interval('(1, 2]')
    assert Interval('(1, 2]') not in Interval('(1, 2)')
    assert Interval('(1, 2)') in Interval('[1, 2]')
    assert Interval('(1, 2)') in Interval('[1, 2)')
    assert Interval('(1, 2)') in Interval('(1, 2]')
    assert Interval('(1, 2)') in Interval('(1, 2)')


def test_interval_copy():

    a = Endpoint('[1')
    b = Endpoint('2]')
    i1 = Interval(None, a, b)
    i2 = i1.copy()
    assert i1 == i2
    assert i1 is not i2
    assert a == i2.a
    assert a is not i2.a
    assert b == i2.b
    assert b is not i2.b


def test_str_interval():

    a = Endpoint(value='p', excluded=False, open=True)
    b = Endpoint(value='q', excluded=True, open=False)
    p = Interval(a=a, b=b)
    assert p.notation == '[p, q)'
    assert 'o' not in p
    assert 'p' in p
    assert 'p' * 1000 in p
    assert 'pq' in p
    assert 'q' not in p
    assert a in p
    assert b in p
    if is_py3:
        with pytest.raises(TypeError):
            1 in p
        with pytest.raises(TypeError):
            Endpoint('3]') in p


def test_date_interval():

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    inaweek = today + datetime.timedelta(days=7)
    ad1 = datetime.date(1, 1, 1)
    a = Endpoint(value=today, excluded=False, open=True)
    b = Endpoint(value=inaweek, excluded=True, open=False)
    week = Interval(a=a, b=b)
    assert today in week
    assert tomorrow in week
    assert ad1 not in week
    assert week in week

