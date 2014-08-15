```
      _                     _             _
 _ __(_)__ _ __ _ _  _ _  _| |__  __ _ __| |__
| '_ \ / _` / _` | || | || | '_ \/ _` / _| / /
| .__/_\__, \__, |\_, |\_, |_.__/\__,_\__|_\_\
|_|    |___/|___/ |__/ |__/
```

Python package for finding modules recursively and then
importing them. Useful for scripts/libraries which expose
DSL-like stuff, like test suites and configuration.

```python
from piggyback.finder import Finder
from piggyback.lookup import Loader

importer = Loader(Finder)
for module in importer.look('.'):
    print(module)

cache = importer.import_all('.')
module = cache['module.name']
```

Let Piggyback manage all the hackery required for you and
go write some code. No more manual `execfiles` and namespace
management madness.
