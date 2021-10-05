# pylsp-rope

Extended refactoring capabilities for Python LSP Server using
[Rope](https://github.com/python-rope/rope).

This is a plugin for [Python LSP
Server](https://github.com/python-lsp/python-lsp-server), so you also need to
have it installed.

python-lsp-server already has basic built-in support for using Rope, but it's
currently limited to just renaming and completion. Installing this plugin adds
more refactoring functionality to python-lsp-server.

## Installation

To use this plugin, you need to install this plugin in the same virtualenv as
python-lsp-server itself.

``` bash
pip install pylsp-rope
```

Then run `pylsp` as usual, the plugin will be auto-discovered by
python-lsp-server if you've installed it to the right environment. Refer to
your IDE/text editor's documentation on how to setup a language server in your
IDE/text editor.

## Configuration

There is no configuration yet.

## Features

This plugin adds the following features to python-lsp-server:

- extract method (codeAction)
- extract variable (codeAction)
- inline method/variable/parameter (codeAction)
- method to method object (codeAction)
- more to come...

Refer to [Rope documentation](https://github.com/python-rope/rope/blob/master/docs/overview.rst)
for more details on how these refactoring works.

## Usage

### Extract method

This refactoring works by triggering a CodeAction when selecting a block of code.

### Extract variable

This refactoring works by triggering a CodeAction when selecting a Python expression.

### Inline

This refactoring works by triggering a CodeAction when the cursor is on a resolvable Python identifier.

### Method to method object

This refactoring works when the cursor is on a function definition.

## Caveat

Support for working on unsaved document is currently incomplete.

Before you start refactoring you must save all unsaved changes in your text
editor. I highly recommended that you enable autosave on your text editor.

This plugin is in early development, so expect some bugs. Please report in
[Github issue tracker](https://github.com/python-lsp/python-lsp-server/issues)
if you had any issues with the plugin.

## Developing

See [CONTRIBUTING.md](https://github.com/python-rope/pylsp-rope/blob/main/CONTRIBUTING.md).

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) from
[lieryan/cookiecutter-pylsp-plugin](https://github.com/lieryan/cookiecutter-pylsp-plugin)
project template.
