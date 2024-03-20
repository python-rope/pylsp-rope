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
input/output for something else, for example when using IPython or pudb, run
this from terminal:

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

This repository is setup to publish to PyPI using Github Actions when creating a Github Release.

1. Update version number in `setup.cfg`.

2. [Create a new Release](https://github.com/python-rope/pylsp-rope/releases/new)

3. Github Actions should publish to PyPI shortly. Verify the publishing are
   successful at https://pypi.org/project/pylsp-rope/#history.

4. Upload release assets to Github Release (fixme: find a way to automate this)
