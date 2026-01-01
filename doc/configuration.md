# Configuration

This document provides comprehensive configuration information for pylsp-rope.

## Plugin Configuration

pylsp-rope is configured through the standard `pylsp_settings` in your LSP client configuration. The plugin settings are located under `plugins.pylsp_rope`.

### Available Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable the pylsp-rope plugin |
| `rename` | boolean | `false` | Enable pylsp-rope's rename functionality |

### Basic Configuration

To enable pylsp-rope with default settings:

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

## Rename Configuration

### Enabling Rename Support

To enable pylsp-rope's rename functionality, add the following to your LSP configuration:

```json
{
  "pylsp": {
    "plugins": {
      "pylsp_rope": {
        "enabled": true,
        "rename": true
      },
      "jedi_rename": {
        "enabled": false
      }
    }
  }
}
```

**Important:** Only enable one rename plugin at a time to avoid conflicts.

### Rename Plugin Comparison

| Plugin | Identifier | Description | When to Use |
|--------|------------|-------------|-------------|
| **pylsp-rope** | `pylsp_rope` | This plugin's rename using Rope's refactoring engine | Complex cross-file refactoring, future module/package support |
| **Built-in Jedi** | `jedi_rename` | Built-in python-lsp-server Jedi rename | Simple renaming scenarios |

### Verification

To verify that pylsp-rope is handling rename requests:

1. Check your LSP logs - pylsp-rope logs `"textDocument/rename: ..."` when handling rename requests
2. The rename behavior uses Rope's refactoring engine, which may handle complex scenarios differently than Jedi
3. Ensure other rename plugins are disabled as shown above

### Current Limitations and Future Support

Currently, pylsp-rope's rename supports:
- ✅ Variables, classes, and functions
- ❌ Modules and packages (planned for a future release)

### Benefits of pylsp-rope Rename

- More mature refactoring engine (Rope)
- Improved handling of complex cross-file refactoring scenarios
- Foundation for future module/package renaming capabilities

If you only need basic variable, class, or function renaming, the built-in rename plugin is sufficient. Use pylsp-rope if you require Rope's advanced refactoring capabilities or plan to use future module/package support.

## Code Actions Configuration

All code actions provided by pylsp-rope are automatically available when the plugin is enabled with `"pylsp.plugins.pylsp_rope.enabled": true`. No additional configuration is required.

### Available Code Actions

- **Extract Method** - Extract code blocks into methods
- **Extract Variable** - Extract expressions into variables
- **Inline** - Inline methods/variables/parameters
- **Use Function** - Replace matching code with function calls
- **Method to Method Object** - Convert methods to callable classes
- **Convert Local Variable to Field** - Convert locals to class attributes
- **Organize Imports** - Clean up import statements
- **Introduce Parameter** - Convert variables to method parameters
- **Generate Code** - Create undefined variables/functions/classes

## Editor-Specific Configuration

### Vim/Neovim

For Vim or Neovim, add the configuration to your `vimrc` or init file:

```vim
lua << EOF
require'lspconfig'.pylsp.setup{
  settings = {
    pylsp = {
      plugins = {
        pylsp_rope = {
          enabled = true,
          rename = true
        },
        jedi_rename = {
          enabled = false
        }
      }
    }
  }
}
EOF
```

### VS Code

For VS Code with the Python LSP plugin, add to your `settings.json`:

```json
{
  "pylsp.configurationSources": ["pycodestyle"],
  "pylsp.plugins.pylsp_rope.enabled": true,
  "pylsp.plugins.pylsp_rope.rename": true,
  "pylsp.plugins.jedi_rename.enabled": false
}
```

### Emacs

For Emacs with lsp-mode, add to your configuration:

```elisp
(setq lsp-pylsp-plugins-pylsp-rope-enabled t
      lsp-pylsp-plugins-pylsp-rope-rename t
      lsp-pylsp-plugins-rope-rename-enabled nil
      lsp-pylsp-plugins-jedi-rename-enabled nil)
```

## Troubleshooting

### Plugin Not Loading

1. Verify pylsp-rope is installed in the same virtualenv as python-lsp-server
2. Check LSP logs for initialization messages
3. Ensure `pylsp_rope` appears in the plugin list

### Rename Not Working

1. Verify `rename: true` is set in pylsp_rope configuration
2. Ensure other rename plugins are disabled
3. Check logs for `"textDocument/rename"` messages
4. Try restarting the language server

### Code Actions Not Available

1. Ensure the plugin is enabled: `"enabled": true`
2. Check that the cursor is in the correct position for the action
3. Verify the code structure supports the requested refactoring
4. Restart the language server if needed
