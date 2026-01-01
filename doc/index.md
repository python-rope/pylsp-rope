# pylsp-rope Documentation

Welcome to the comprehensive documentation for pylsp-rope, a plugin that extends Python LSP Server with advanced refactoring capabilities using Rope.

## Features

This plugin adds the following features to python-lsp-server:

### Rename Functionality
- **Implemented**: Variables, classes, functions (disabled by default, requires explicit configuration)
- **Planned**: Modules, packages (coming soon)

### Code Actions
- Extract method
- Extract variable
- Inline method/variable/parameter
- Use function
- Method to method object
- Convert local variable to field
- Organize imports
- Introduce parameter
- Generate variable/function/class from undefined variable

## Documentation

```{toctree}
---
maxdepth: 2
caption: Contents:
---
configuration
features
installation
usage
troubleshooting
```

## Quick Start

1. Install pylsp-rope:
   ```bash
   pip install pylsp-rope
   ```

2. Configure in your LSP client:
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

3. For rename functionality, enable it explicitly:
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

## Contributing

Found a bug or want to contribute? Please check the Contributing Guidelines in the main repository at `../CONTRIBUTING.md`.

## Support

For issues and questions:
- [GitHub Issues](https://github.com/python-rope/pylsp-rope/issues)
- [Rope Documentation](https://github.com/python-rope/rope/blob/master/docs/overview.rst)
