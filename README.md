piggyback
=========

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
