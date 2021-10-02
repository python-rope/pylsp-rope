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
- more to come...

## Developing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) from
[lieryan/cookiecutter-pylsp-plugin](https://github.com/lieryan/cookiecutter-pylsp-plugin)
project template.
