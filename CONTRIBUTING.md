## Developing

Install development dependencies with (you might want to create a virtualenv first):

``` bash
git clone https://github.com/python-rope/pylsp-rope.git pylsp-rope
cd pylsp-rope
pip install -e '.[dev]'
```

### Enabling logging

Run pylsp in development mode, enable logs:

``` bash
pylsp -v --log-file /tmp/pylsp.log
```

Vim users should refer to [Rope in Vim or Neovim](https://github.com/python-rope/rope/wiki/Rope-in-Vim-or-Neovim)
for how to configure their LSP client to run `pylsp` in development mode.

### Enabling tcp mode

Optionally, run in tcp mode if you want to be able to use the standard
input/output, for example when using IPython or pudb, run this from terminal:

``` bash
pylsp -v --tcp --port 8772 --log-file /tmp/pylsp.log
```

#### Connecting to tcp mode pylsp from lsp-vim

``` vim
autocmd User lsp_setup call lsp#register_server({
    \ 'name': 'pylsp-debug',
    \ 'cmd': ["nc", "localhost", "8772"],
    \ 'allowlist': ['python'],
    \ })
```

TODO: document how to connect to pylsp via pylsp from LSP clients.

### Testing 

Run `pytest` to run plugin tests.

## Publishing

If this is your first time publishing to PyPI, follow the instruction at [Twine
docs](https://packaging.python.org/guides/distributing-packages-using-setuptools/#create-an-account)
to create an PyPI account and setup Twine.

1. Update version number in `setup.cfg`.

2. Build a package using setuptools:

``` bash
python -m build
twine check dist/*
```

3. Tag the release:

``` bash
git tag --sign 0.1.3
git push origin 0.1.3
git push origin main
```

4. Then upload using Twine:

``` bash
twine upload --sign dist/*
```

Alternatively, you may want to upload to Test PyPI first before going live:

``` bash
twine upload --sign --repository testpypi dist/*
```
