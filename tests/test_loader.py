from pytest import raises


def test_search(loader):
    for item in loader.search():
        assert item in ['tests.conftest', 'tests.example']


def test_import_all(loader):
    prev = loader.get('tests.example')
    curr = loader.import_all()

    assert 'tests.conftest' in curr
    assert 'tests.example' in curr

    example = curr['tests.example']

    assert example.const == 5
    assert example.delta is prev.delta


def test_get(loader):
    example = loader.get('tests.example')
    assert example.const == 5
