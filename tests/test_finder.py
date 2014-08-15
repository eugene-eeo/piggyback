import unittest
from piggyback.finder import Finder


class FinderTest(unittest.TestCase):
    def test_find_file(self):
        finder = Finder('tests/example.py')
        assert not finder.is_package
        assert list(finder.find_modules()) == ['example.py']

    def test_find_directory(self):
        finder = Finder('tests/examples')
        assert finder.is_package
        assert list(finder.find_modules()) == ['module.py', 'nested/module.py']
