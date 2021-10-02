# pylsp-rope

Extended refactoring capabilities for Python LSP Server using [Rope](https://github.com/python-rope/rope).

This is a plugin for [Python LSP Server](https://github.com/python-lsp/python-lsp-server).

## Installation

Install into the same virtualenv as python-lsp-server itself.

``` bash
pip install pylsp-rope
```

## Configuration

There is no configuration yet.

## Features

This plugin adds the following features to `pylsp`:

- extract method (codeAction)
- extract variable (codeAction)
- inline method/variable/parameter (codeAction)

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

Build a package using setuptools:

``` bash
python setup.py sdist
twine check dist/*
```

Then upload using Twine:

```
twine upload dist/*
```

Alternatively, you may want to upload to test PyPI first before going live:

```
twine upload --repository testpypi dist/*
```

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) from
[lieryan/cookiecutter-pylsp-plugin](https://github.com/lieryan/cookiecutter-pylsp-plugin)
project template.
