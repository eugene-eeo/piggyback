from os.path import split
from piggyback.utils import module_name, PY_IDENT, PY_MODULE, ls


class FileFinder(object):
    def __init__(self, path):
        self.path, self.fname = split(path)

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
