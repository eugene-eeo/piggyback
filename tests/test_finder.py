from os.path import abspath, split, sep
from piggyback.finder import FileFinder, ModuleFinder


def test_find_single():
    path = abspath('tests/example.py')
    finder = FileFinder(path)

    assert list(finder.modules) == ['example']
    assert finder.path == split(path)[0]


def test_find_module():
    path = abspath('tests/')
    finder = ModuleFinder(path)

    assert set(finder.modules) == set(['tests.example', 'tests.conftest'])
    assert finder.path == split(path)[0]
