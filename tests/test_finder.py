import unittest
from piggyback.finder import Finder, traverse, normalize_paths,\
    filter_files


class FinderTest(unittest.TestCase):
    def test_find_file(self):
        finder = Finder('tests/example.py')
        assert not finder.is_package
        assert set(finder.find_modules()) == set(('example.py',))

    def test_find_flat(self):
        finder = Finder('tests/examples/nested')
        assert finder.is_package
        assert set(finder.find_modules()) == set(('module.py',))

    def test_find_nested(self):
        finder = Finder('tests/examples')
        expected = ('module.py', 'nested/module.py')

        assert finder.is_package
        assert set(finder.find_modules()) == set(expected)

    def test_find_custom(self):
        finder = Finder('tests/examples')
        finder.ignored.append(lambda x: x == 'module.py')
        assert not list(finder.find_modules())

        finder.hints.append(lambda x: False)
        assert not list(finder.find_modules())


class FinderFuncTest(unittest.TestCase):
    def test_traverse(self):
        def hinter(files):
            return '__init__.py' in files

        given = traverse('tests/examples', hinter)
        expected = [
            'tests/examples/__init__.py',
            'tests/examples/module.py',
            'tests/examples/nested/__init__.py',
            'tests/examples/nested/module.py'
        ]
        assert set(given) == set(expected)

    def test_normalize_paths(self):
        given = [
            'tests/this/path.py',
            'tests/this/normal/this.py',
        ]
        iterable = normalize_paths(given, 'tests/this')
        expected = ['path.py', 'normal/this.py']
        assert list(iterable) == expected

    def test_filter_files(self):
        given = [
            'tests/this/this/path.py',
            'tests/this/this/this/mpath.py',
            'tests/zpath.py',
        ]
        iterable = filter_files(given, 'm', '.py')
        expected = ['tests/this/this/this/mpath.py']
        assert list(iterable) == expected
