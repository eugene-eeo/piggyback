import unittest
from piggyback.finder import Finder


class FinderTest(unittest.TestCase):
    def test_find_file(self):
        finder = Finder('tests/example.py')
        assert not finder.is_package
        assert list(finder.find_modules()) == ['example.py']

    def test_find_flat(self):
        finder = Finder('tests/examples/nested')
        assert finder.is_package
        assert list(finder.find_modules()) == ['module.py']

    def test_find_nested(self):
        finder = Finder('tests/examples')
        assert finder.is_package
        assert list(finder.find_modules()) == ['module.py', 'nested/module.py']

    def test_find_custom(self):
        finder = Finder('tests/examples')
        finder.ignored.append(lambda x: x == 'module.py')
        assert not list(finder.find_modules())

        finder.hints.append(lambda x: False)
        assert not list(finder.find_modules())
