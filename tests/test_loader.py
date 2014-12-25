from pytest import raises
from piggyback.loader import Loader
from piggyback.finder import FileFinder


def test_single_file():
    loader = Loader(FileFinder('tests/example.py'))

    assert 'example' in loader
    assert loader['example'].const == 5


def test_search(loader):
    modules = list(loader)
    assert modules

    for item in modules:
        assert item in ['tests.conftest', 'tests.example']


def test_import_all(loader):
    prev = loader['tests.example']
    curr = loader.import_all()

    assert 'tests.conftest' in curr
    assert 'tests.example' in curr

    example = curr['tests.example']

    assert example.const == 5
    assert example.delta is prev.delta


def test_getitem(loader):
    example = loader['tests.example']
    assert example.const == 5

    with raises(ImportError):
        loader['tests.test_this']
