# pylsp-rope

Extended refactoring capabilities for Python LSP Server using Rope.

This is a plugin for the [Python LSP Server](https://github.com/python-lsp/python-lsp-server).

## Installation

Install into the same virtualenv as python-lsp-server itself.

``` bash
pip install pylsp-rope
```

## Configuration

... TODO ...

## Developing

Install development dependencies with (you might want to create a virtualenv first):

``` bash
git clone https://github.com/lieryan/pylsp-rope pylsp-rope
cd pylsp-rope
pip install -e '.[dev]'
```

Run `pytest` to run plugin tests.
## Publishing

If this is your first time publishing to PyPI, follow the instruction at [Twine
docs](https://packaging.python.org/guides/distributing-packages-using-setuptools/#create-an-account)
to create an PyPI account and setup Twine.

Build a package and upload using Twine:

``` bash
python setup.py sdist
twine check dist/*
twine upload dist/*
```

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[lieryan/cookiecutter-pylsp-plugin](https://github.com/lieryan/cookiecutter-pylsp-plugin)
project template.
