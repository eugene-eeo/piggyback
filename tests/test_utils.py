from piggyback.finder import IDENT
from piggyback.utils import to_module, all_ok


def test_to_module():
    assert to_module('this/that.py') == 'this.that'
    assert to_module('this/that/those.py') == 'this.that.those'


def test_all_ok():
    valid = [lambda x: x == 1]

    assert all_ok(valid, 1)
    assert not all_ok(valid + [lambda x: x == 2], 1)


def test_ident():
    assert not IDENT.match('$mdb')
    assert not IDENT.match('0abc')
    assert not IDENT.match('ab#c')

    assert IDENT.match('ABC')
    assert IDENT.match('A12')
    assert IDENT.match('_a2')
