# Installation Guide

This guide covers how to install and set up pylsp-rope.

## Prerequisites

- Python 3.8 or higher
- [Python LSP Server](https://github.com/python-lsp/python-lsp-server) installed
- An LSP-capable editor/IDE

## Installation

### Standard Installation

Install pylsp-rope in the same virtual environment as python-lsp-server:

```bash
pip install pylsp-rope
```

### Development Installation

For development or testing:

```bash
git clone https://github.com/python-rope/pylsp-rope.git
cd pylsp-rope
pip install -e .
```

### Verification

To verify installation:

1. Check that pylsp can load the plugin:
   ```bash
   pylsp --help
   ```

2. Start your LSP client and check logs for:
   ```
   Initializing pylsp_rope
   ```

## Editor Setup

### Vim/Neovim

Using [vim-lsp](https://github.com/prabirshrestha/vim-lsp) or [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig):

```vim
" For vim-lsp
if executable('pylsp')
    au User lsp_setup call lsp#register_server({
        \ 'name': 'pylsp',
        \ 'cmd': {server_info->['pylsp']},
        \ 'allowlist': ['python'],
        \ })
endif

" For nvim-lspconfig
require'lspconfig'.pylsp.setup{
  settings = {
    pylsp = {
      plugins = {
        pylsp_rope = {
          enabled = true
        }
      }
    }
  }
}
```

### Visual Studio Code

Install the official Python extension and configure:

```json
{
  "pylsp.configurationSources": ["pycodestyle"],
  "pylsp.plugins.pylsp_rope.enabled": true
}
```

### Emacs

Using [lsp-mode](https://github.com/emacs-lsp/lsp-mode):

```elisp
(use-package lsp-pylsp
  :config
  (setq lsp-pylsp-plugins-pylsp_rope-enabled t))
```

### Sublime Text

Using [LSP-pylsp](https://packagecontrol.io/packages/LSP-pylsp):

```json
{
  "LSP-pylsp": {
    "settings": {
      "pylsp": {
        "plugins": {
          "pylsp_rope": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

### Other Editors

Any editor that supports the Language Server Protocol can use pylsp-rope. Configure the server to use `pylsp` and ensure the plugin settings are properly configured.

## Troubleshooting

### Plugin Not Found

If pylsp-rope is not recognized:

1. **Check Installation**: Ensure it's installed in the same environment as pylsp
   ```bash
   pip list | grep pylsp-rope
   ```

2. **Verify Path**: Check that your editor is using the correct Python interpreter

3. **Restart LSP**: Restart the language server in your editor

### Virtual Environment Issues

If using virtual environments:

1. Activate the environment before installing
2. Install both `python-lsp-server` and `pylsp-rope` in the same environment
3. Configure your editor to use the virtual environment's Python interpreter

Example with pipenv:
```bash
pipenv install python-lsp-server pylsp-rope
pipenv shell
```

Example with poetry:
```bash
poetry add python-lsp-server pylsp-rope
poetry shell
```

### Performance Considerations

For large codebases:

1. Increase Rope's memory limits in your LSP configuration
2. Consider disabling unused features
3. Ensure sufficient disk space for Rope's project cache

## Next Steps

- See [Configuration Guide](configuration.md) for detailed configuration options
- Check [Features Overview](features.md) to understand available refactorings
- Refer to [Usage Examples](usage.md) for practical examples