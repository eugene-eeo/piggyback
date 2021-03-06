::

    Python  _                     _             _
       _ __(_)__ _ __ _ _  _ _  _| |__  __ _ __| |__
      | '_ \ / _` / _` | || | || | '_ \/ _` / _| / /
      | .__/_\__, \__, |\_, |\_, |_.__/\__,_\__|_\_\
      |_|    |___/|___/ |__/ |__/


**Supported Pythons:** 2.6+, 3.2+

Python package for finding modules recursively and then
importing them. Useful for scripts/libraries which expose
DSL-like stuff, like test suites and configuration.

Development goals include extensibility and stability. We
aim for a robust API that although doesn't do much does what
it does well. Currently we think that we've reached those
goals.

.. code-block:: python

    from piggyback import loader

    importer = loader('path')
    for module in importer:
        print(module)

    cache = importer.import_all()
    module = cache['path.module']

Let Piggyback manage all the hackery required for you and
go write some code. No more manual ``execfiles`` and namespace
management madness. Piggyback does importing and namespaces
right, namely:

- We isolate every module that we ``__import__``, and their
  namespaces are separate of one another, as well as the
  current module. No namespace clashes.

- The ``sys.path`` variable remains unchanged at the end of
  the importing- Piggyback will ensure that the `sys.path`
  is cleansed of all appended paths once we are finished with
  the importing.

To install the current version of the package, simply do a
``pip install piggyback``. For the documentation you can
simply visit the `docs`_ on Github pages.

.. _docs: https://eugene-eeo.github.io/piggyback

.. image:: https://travis-ci.org/eugene-eeo/piggyback.svg?branch=master
    :target: https://travis-ci.org/eugene-eeo/piggyback

.. image:: http://img.shields.io/pypi/v/Piggyback.svg
    :target: https://pypi.python.org/pypi/Piggyback
