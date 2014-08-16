import unittest
from piggyback.finder import Finder
from piggyback.loader import Loader

dirloader = Loader(Finder('tests/examples'))
fileloader = Loader(Finder('tests/example.py'))


class DirectoryLoaderTest(unittest.TestCase):
    def test_look(self):
        found = set(dirloader.search())
        assert found == set(('examples.module', 'examples.nested.module'))

    def test_import_all(self):
        cache = dirloader.import_all()
        for item in ('examples.module', 'examples.nested.module'):
            assert item in cache

        assert len(cache) == 2
        assert cache['examples.module'].__name__ == 'examples.module'

    def test_load(self):
        assert dirloader.load('examples.module').this
        assert dirloader.load('examples.nested.module')


class FileLoaderTest(unittest.TestCase):
    def test_look(self):
        found = set(fileloader.search())
        assert found == set(('example',))

    def test_import_all(self):
        cache = fileloader.import_all()
        assert len(cache) == 1
        assert cache['example'].__name__ == 'example'
