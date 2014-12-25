from piggyback.utils import to_module, all_ok


def test_to_module():
    assert to_module('this/that.py') == 'this.that'
    assert to_module('this/that/those.py') == 'this.that.those'


def test_all_ok():
    valid = [lambda x: x == 1]

    assert all_ok(valid, 1)
    assert not all_ok(valid + [lambda x: x == 2], 1)
