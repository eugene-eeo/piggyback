from os import listdir, sep
from os.path import isdir, join
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
            if base is not None:
                item = join(base, item)
            yield item


def to_module(path):
    return path[:path.index('.py')].replace(sep, '.')
