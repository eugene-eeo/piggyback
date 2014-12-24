from pytest import fixture
from piggyback import loader as _loader
from piggyback.finder import ModuleFinder



@ModuleFinder.file_filters.append
def ignore_test_files(p):
    return not p.startswith('test_')


@fixture
def loader():
    return _loader('tests/')
