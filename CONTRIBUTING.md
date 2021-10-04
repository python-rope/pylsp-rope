## Developing

Install development dependencies with (you might want to create a virtualenv first):

``` bash
git clone https://github.com/python-rope/pylsp-rope.git pylsp-rope
cd pylsp-rope
pip install -e '.[dev]'
```

Run `pytest` to run plugin tests.

## Publishing

If this is your first time publishing to PyPI, follow the instruction at [Twine
docs](https://packaging.python.org/guides/distributing-packages-using-setuptools/#create-an-account)
to create an PyPI account and setup Twine.

1. Update version number in `setup.cfg`.

2. Build a package using setuptools:

``` bash
python setup.py sdist
twine check dist/*
```

3. Then upload using Twine:

```
twine upload -s dist/*
```

Alternatively, you may want to upload to Test PyPI first before going live:

```
twine upload -s --repository testpypi dist/*
```
