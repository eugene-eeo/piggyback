import unittest
from piggyback.finder import Finder
from piggyback.loader import Loader


class LoaderTest(unittest.TestCase):
    def setUp(self):
        self.loader = Loader(Finder('tests/examples'))

    def test_look(self):
        found = set(self.loader.search())
        assert found == set(('examples.module', 'examples.nested.module'))

    def test_import_all(self):
        cache = self.loader.import_all()
        for item in ('examples.module', 'examples.nested.module'):
            assert item in cache

        assert len(cache) == 2
        assert cache['examples.module'].__name__ == 'examples.module'

    def test_load(self):
        assert self.loader.load('examples.module').this
        assert self.loader.load('examples.nested.module')
