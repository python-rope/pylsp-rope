# pylsp-rope

Extended refactoring capabilities for Python LSP Server using
[Rope](https://github.com/python-rope/rope).

This is a plugin for [Python LSP
Server](https://github.com/python-lsp/python-lsp-server).

`python-lsp-server` already has basic built-in support for using Rope, but it's
currently limited to just renaming and completion. Installing this plugin adds
more refactoring functionality to `python-lsp-server`.

## Installation

To use this plugin, you need to install this plugin in the same virtualenv as
python-lsp-server itself.

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

## Usage

### Extract method

This refactoring works when selecting a block of code.

### Extract variable

This refactoring works when selecting a Python expression.

### Inline

This refactoring works when the cursor is on a resolvable Python identifier.

## Caveat

Support for working on unsaved document is currently incomplete.

Before you start refactoring you must save all unsaved changes in your text
editor. I highly recommended that you enable autosave on your text editor.

This plugin is in early development, so expect some bugs. Please report in
Github issue tracker if you had any issues.

## Developing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) from
[lieryan/cookiecutter-pylsp-plugin](https://github.com/lieryan/cookiecutter-pylsp-plugin)
project template.
