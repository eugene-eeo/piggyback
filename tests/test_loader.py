import unittest
from piggyback.finder import Finder
from piggyback.loader import Loader


class LoaderTest(unittest.TestCase):
    def setUp(self):
        self.path = 'tests/examples'
        self.loader = Loader(Finder)

    def test_look(self):
        found = list(self.loader.look(self.path))
        assert found == ['module', 'nested.module']

    def test_import_all(self):
        cache = self.loader.import_all(self.path)
        for item in ('module', 'nested.module'):
            assert item in cache

        assert len(cache) == 2
        assert cache['module'].this

    def test_load(self):
        assert self.loader.load(self.path, 'module').this
        assert self.loader.load(self.path, 'nested.module')
