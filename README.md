# pylsp-rope

[![Tests](https://github.com/python-rope/pylsp-rope/actions/workflows/run-test.yml/badge.svg)](https://github.com/python-rope/pylsp-rope/actions/workflows/run-test.yml) 
[![codecov](https://codecov.io/gh/python-rope/pylsp-rope/graph/badge.svg?token=LMO7PW0AEK)](https://codecov.io/gh/python-rope/pylsp-rope)
[![Documentation](https://readthedocs.org/projects/pylsp-rope/badge/?version=latest)](https://pylsp-rope.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pylsp-rope.svg)](https://badge.fury.io/py/pylsp-rope)

Extended refactoring capabilities for Python LSP Server using [Rope](https://github.com/python-rope/rope).

This is a plugin for [Python LSP Server](https://github.com/python-lsp/python-lsp-server), so you also need to have it installed.

python-lsp-server already has basic built-in support for using Rope, but it's currently limited to just renaming and completion. Installing this plugin adds more refactoring functionality to python-lsp-server.

## Features

- **Enhanced Rename**: Advanced cross-file renaming with Rope's refactoring engine
- **Code Actions**: 12+ refactoring operations including extract method, inline, use function, and more
- **Code Generation**: Create variables, functions, and classes from undefined symbols
- **Import Organization**: Automatic cleanup and sorting of imports
- **Local to Field**: Convert local variables to class attributes

## Quick Start

### Installation

Install pylsp-rope in the same virtualenv as python-lsp-server:

```bash
pip install pylsp-rope
```

### Basic Configuration

Add to your LSP configuration:

```json
{
  "pylsp": {
    "plugins": {
      "pylsp_rope": {
        "enabled": true
      }
    }
  }
}
```

### Enable Rename Support

For advanced rename functionality, enable it explicitly:

```json
{
  "pylsp": {
    "plugins": {
      "pylsp_rope": {
        "enabled": true,
        "rename": true
      }
    }
  }
}
```

## Documentation

Complete documentation is available at **[pylsp-rope.readthedocs.io](https://pylsp-rope.readthedocs.io/)**

- **[Installation Guide](https://pylsp-rope.readthedocs.io/en/latest/installation.html)** - Setup for various editors
- **[Configuration Guide](https://pylsp-rope.readthedocs.io/en/latest/configuration.html)** - Complete configuration options
- **[Features Overview](https://pylsp-rope.readthedocs.io/en/latest/features.html)** - Detailed feature descriptions
- **[Usage Examples](https://pylsp-rope.readthedocs.io/en/latest/usage.html)** - Practical examples
- **[Troubleshooting](https://pylsp-rope.readthedocs.io/en/latest/troubleshooting.html)** - Common issues and solutions

## Available Refactorings

| Category | Operations |
|----------|------------|
| **Extract** | Method, Variable (with similar statement support) |
| **Inline** | Method, Variable, Parameter |
| **Restructure** | Use Function, Method to Method Object, Local to Field |
| **Generate** | Variable, Function, Class |
| **Utilities** | Organize Imports, Introduce Parameter |
| **Rename** | Enhanced cross-file renaming (Rope-based) |

## Caveat

Support for working on unsaved documents is currently experimental, but it should work.

This plugin is in early development, so expect some bugs. Please report in the [GitHub issue tracker](https://github.com/python-lsp/python-lsp-server/issues) if you have any issues with the plugin.

## Contributing

See [CONTRIBUTING.md](https://github.com/python-rope/pylsp-rope/blob/main/CONTRIBUTING.md).

## Packaging status

[![Packaging status](https://repology.org/badge/vertical-allrepos/python:pylsp-rope.svg)](https://repology.org/project/python:pylsp-rope/versions)

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) from [python-lsp/cookiecutter-pylsp-plugin](https://github.com/python-lsp/cookiecutter-pylsp-plugin) project template.