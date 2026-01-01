# Troubleshooting

This document provides solutions to common issues with pylsp-rope.

## General Issues

### Plugin Not Loading

**Symptoms:**
- pylsp-rope features don't appear in your editor
- LSP logs don't mention pylsp-rope initialization
- Code actions for refactoring are missing

**Solutions:**

1. **Check Installation:**
   ```bash
   pip list | grep pylsp-rope
   ```
   If not installed, install in the same environment as pylsp:
   ```bash
   pip install pylsp-rope
   ```

2. **Verify Environment:**
   Ensure pylsp-rope and python-lsp-server are in the same virtual environment:
   ```bash
   which pylsp
   pip list | grep pylsp
   ```

3. **Check Configuration:**
   Verify the plugin is enabled in your LSP settings:
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

4. **Restart LSP:**
   Restart the language server in your editor.

### Performance Issues

**Symptoms:**
- Slow response times for refactoring operations
- High memory usage
- Editor freezing during large refactorings

**Solutions:**

1. **Increase Memory:**
   Add memory limits to your configuration if available.

2. **Disable Unused Features:**
   Only enable features you actually use:
   ```json
   {
     "pylsp": {
       "plugins": {
         "pylsp_rope": {
           "enabled": true,
           "rename": false  // Disable if not used
         }
       }
     }
   }
   ```

3. **Clean Project Cache:**
   Delete Rope's cache directory:
   ```bash
   rm -rf .rope_project
   ```

## Rename-Specific Issues

### Rename Not Working

**Symptoms:**
- Rename operation doesn't trigger
- Old rename plugin still active
- No rename dialog appears

**Solutions:**

1. **Enable Rename Explicitly:**
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

2. **Check for Conflicting Plugins:**
   Ensure only one rename plugin is enabled:
   - `pylsp_rope` (this plugin)
   - `jedi_rename` (built-in jedi)

3. **Verify Active Plugin:**
   Check LSP logs for `"textDocument/rename"` messages from pylsp-rope.

### Rename Not Updating All Files

**Symptoms:**
- Rename only affects current file
- Cross-file references not updated
- Import statements not modified

**Solutions:**

1. **Save All Files:**
   Ensure all modified files are saved before renaming.

2. **Check Project Structure:**
   Verify your editor has recognized the entire project as a workspace.

3. **Restart LSP:**
   Restart the language server to refresh project context.

## Code Action Issues

### Code Actions Not Available

**Symptoms:**
- Refactoring options don't appear in code action menu
- "No code actions available" message
- Some refactorings work, others don't

**Solutions:**

1. **Check Cursor Position:**
   Ensure cursor is positioned correctly for the intended refactoring:
   - For extract: on the code block/expression
   - For inline: on the variable/method name
   - For use function: on the function definition

2. **Verify Code Structure:**
   Some refactorings require specific code structures:
   - Extract method needs valid Python statements
   - Inline needs resolvable references
   - Generate code needs undefined symbols

3. **Check for Syntax Errors:**
   Fix any syntax errors in the file before refactoring.

### Refactoring Fails with Error

**Symptoms:**
- Error dialog appears
- Refactoring operation completes incorrectly
- Files become corrupted

**Solutions:**

1. **Check LSP Logs:**
   Look for detailed error messages in the language server logs.

2. **Save All Files:**
   Ensure all files are saved before refactoring.

3. **Try Manual Refactoring:**
   If automatic refactoring fails, consider doing it manually.

4. **Report Issue:**
   If it's a bug, file an issue with:
   - The error message
   - Code example that reproduces the issue
   - Steps to reproduce

## Editor-Specific Issues

### Vim/Neovim

#### No Code Actions

**Solution:**
```vim
" Check if LSP is working
:lua print(vim.inspect(vim.lsp.get_active_clients()))

" Manually trigger code actions
:lua vim.lsp.buf.code_action()
```

#### Conflicting Keybindings

**Solution:**
```vim
" Map code actions to available keybinding
nnoremap <silent> <C-.> <cmd>lua vim.lsp.buf.code_action()<cr>
```

### VS Code

#### Multiple Python Interpreters

**Symptoms:**
- pylsp-rope installed but not recognized
- Different Python interpreters being used

**Solution:**
1. Set the interpreter explicitly:
   ```json
   {
     "python.defaultInterpreterPath": "/path/to/your/venv/bin/python"
   }
   ```

2. Restart VS Code and reload the workspace.

#### Extensions Conflict

**Solution:**
Disable conflicting Python extensions:
- Pylance (may conflict with pylsp)
- Other Python LSP clients

### Emacs

#### lsp-mode Issues

**Solution:**
```elisp
;; Check LSP status
lsp-describe-session

;; Restart LSP
lsp-restart-workspace
```

## Rope-Specific Issues

### Rope Cache Corruption

**Symptoms:**
- Inconsistent refactoring behavior
- Errors mentioning Rope cache
- Slow performance

**Solution:**
```bash
# Remove Rope cache
rm -rf .rope_project
rm -rf ~/.rope
```

### Large Project Issues

**Symptoms:**
- Very slow refactoring on large projects
- Memory errors
- Timeouts

**Solutions:**

1. **Exclude Directories:**
   Configure pylsp to exclude large directories:
   ```json
   {
     "pylsp": {
       "configurationSources": ["pycodestyle"],
       "plugins": {
         "pylsp_rope": {
           "enabled": true
         }
       }
     }
   }
   ```

2. **Use Incremental Refactoring:**
   Break large refactorings into smaller steps.

3. **Consider Project Structure:**
   Split very large projects into smaller subprojects.

## Getting Help

### Log Files

**Vim/Neovim:**
```vim
:lua print(vim.lsp.get_log_path())
```

**VS Code:**
- Help → Toggle Developer Tools → Console
- Extensions → Python → Show Log

**Emacs:**
```elisp
*Messages* buffer
*LSP* buffer
```

### Reporting Issues

When reporting issues, include:

1. **Environment Information:**
   - Python version
   - pylsp and pylsp-rope versions
   - Editor and version
   - Operating system

2. **Configuration:**
   - Your LSP configuration
   - Project structure (if relevant)

3. **Steps to Reproduce:**
   - Detailed steps
   - Code example
   - Expected vs actual behavior

4. **Logs:**
   - LSP logs showing the error

### Community Support

- [GitHub Issues](https://github.com/python-rope/pylsp-rope/issues)
- [Rope Documentation](https://github.com/python-rope/rope)
- [Python LSP Server](https://github.com/python-lsp/python-lsp-server)
