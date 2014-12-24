from os import listdir, sep
from os.path import join, isdir, split
from re import compile


PY_IDENT = compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
PY_MODULE = compile(r'%s\.py[c]{,1}' % PY_IDENT.pattern)


def all_ok(functions, item):
    return all(f(item) for f in functions)


def ls(path, d_ok=(), f_ok=(), base=None):
    for item in listdir(path):
        if isdir(item) and all_ok(d_ok, item):
            for k in ls(item, ok, item):
                yield k
            continue
        if all_ok(f_ok, item):
            yield item if base is None else join(base, item)


def module_name(path):
    return path[:path.index('.py')].replace(sep, '.')


class FileFinder(object):
    def __init__(self, path):
        self.path, self.fname = split(self.filename)

    @property
    def modules(self):
        return [module_name(self.fname)]


class ModuleFinder(object):
    tree_filters = (
        lambda x: '__init__.py' in x,
        PY_IDENT.match,
    )
    file_filters = (
        lambda x: not x.startswith('.'),
        lambda x: not x.startswith('__'),
        lambda x: x.endswith('.py'),
        PY_MODULE.match,
    )

    def __init__(self, path):
        self.path = path

    @property
    def modules(self):
        iterable = ls(
            path=self.path,
            d_ok=self.tree_filters,
            f_ok=self.file_filters,
        )
        for item in iterable:
            yield module_name(item)
