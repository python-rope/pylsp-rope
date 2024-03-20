# pylsp-rope

[![Tests](https://github.com/python-rope/pylsp-rope/actions/workflows/run-test.yml/badge.svg)](https://github.com/python-rope/pylsp-rope/actions/workflows/run-test.yml) 
[![codecov](https://codecov.io/gh/python-rope/pylsp-rope/graph/badge.svg?token=LMO7PW0AEK)](https://codecov.io/gh/python-rope/pylsp-rope)

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
python-lsp-server if you've installed it to the right environment. On Vim,
refer to [Rope in Vim or
Neovim](https://github.com/python-rope/rope/wiki/Rope-in-Vim-or-Neovim). For
other editors, refer to your IDE/text editor's documentation on how to setup a
language server. 

## Configuration

You can enable rename support using pylsp-rope with workspace config key
`pylsp.plugins.pylsp_rope.rename`. 

Note that this differs from the config key `pylsp.plugins.rope_rename.enabled`
that is used for the rope rename implementation using the python-lsp-rope's
builtin `rope_rename` plugin. To avoid confusion, avoid enabling more than one
python-lsp-server rename plugin.

## Features

This plugin adds the following features to python-lsp-server:

Rename: 

- rename everything: classes, functions, modules, packages (disabled by default)

Code Action:

- extract method
- extract variable 
- inline method/variable/parameter 
- use function 
- method to method object 
- convert local variable to field 
- organize imports 
- introduce parameter 
- generate variable/function/class from undefined variable 

Refer to [Rope documentation](https://github.com/python-rope/rope/blob/master/docs/overview.rst)
for more details on how these refactoring works.

## Usage

### Rename

When Rename is triggered, rename the symbol under the cursor. If the symbol
under the cursor points to a module/package, it will move that module/package
files.

### Extract method

Variants: 

- Extract method
- Extract global method
- Extract method including similar statements
- Extract global method including similar statements

When CodeAction is triggered and the cursor is on any block of code, extract
that expression into a method. Optionally, similar statements can also be
extracted.

### Extract variable

Variants: 

- Extract variable
- Extract global variable
- Extract variable including similar statements
- Extract global variable including similar statements

When CodeAction is triggered and the cursor is on a expression, extract that
expression into a variable. Optionally, similar statements can also be
extracted.

### Inline

When CodeAction is triggered and the cursor is on a resolvable Python variable,
replace all calls to that method with the method body.

### Use function

When CodeAction is triggered and the cursor is on the function name of a `def`
statement, try to replace code whose AST matches the selected function with a
call to the function.

### Method to method object

When CodeAction is triggered and the cursor is on the function name of a `def`
statement, create a callable class to replace that method. You may want to
inline the method afterwards to remove the indirection.

### Convert local variable to field

When CodeAction is triggered wand the cursor is on a local variable inside a
method, convert that local variable to an attribute.

### Organize import

Trigger CodeAction anywhere in a Python file to organize imports.

### Introduce parameter

When CodeAction is triggered and the cursor is selecting a Python variable or
attribute, make that variable/attribute a parameter.

### Generate code

Variants:

- [x] Generate variable
- [x] Generate function
- [x] Generate class
- [ ] Generate module
- [ ] Generate package

When CodeAction is triggered and the cursor is on an undefined Python
variable, generate an empty variable/function/class/module/package for that
name.

## Caveat

Support for working on unsaved document is currently experimental.

This plugin is in early development, so expect some bugs. Please report in
[Github issue tracker](https://github.com/python-lsp/python-lsp-server/issues)
if you had any issues with the plugin.

## Developing

See [CONTRIBUTING.md](https://github.com/python-rope/pylsp-rope/blob/main/CONTRIBUTING.md).

## Packaging status

[![Packaging status](https://repology.org/badge/vertical-allrepos/python:pylsp-rope.svg)](https://repology.org/project/python:pylsp-rope/versions)

[![Packaging status](https://repology.org/badge/vertical-allrepos/python:lsp-rope.svg)](https://repology.org/project/python:lsp-rope/versions)

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) from
[python-lsp/cookiecutter-pylsp-plugin](https://github.com/python-lsp/cookiecutter-pylsp-plugin)
project template.
