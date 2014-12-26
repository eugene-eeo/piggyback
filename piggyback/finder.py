from os.path import split, sep
from re import compile
from piggyback.utils import to_module, ls


IDENT = compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


class Finder(object):
    pass


class FileFinder(Finder):
    def __init__(self, path):
        self.path, self.root = split(path)

    @property
    def modules(self):
        yield to_module(self.root)


class ModuleFinder(Finder):
    tree_filters = [
        lambda x: '__init__.py' in x,
        IDENT.match,
    ]
    file_filters = [
        lambda x: not x.startswith('.'),
        lambda x: not x.startswith('__'),
        lambda x: x.endswith('.py'),
    ]

    def __init__(self, path):
        self.base = path
        self.path, self.root = split(path.rstrip(sep))

    def find(self):
        return ls(
            path=self.base,
            d_ok=self.tree_filters,
            f_ok=self.file_filters,
        )

    @property
    def modules(self):
        for item in self.find():
            module = to_module(item)
            if not IDENT.match(module):
                continue
            yield '%s.%s' % (self.root, module)
