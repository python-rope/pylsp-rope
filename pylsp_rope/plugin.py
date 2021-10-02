import logging

from pylsp import hookimpl, uris


logger = logging.getLogger(__name__)


@hookimpl
def pylsp_settings():
    logger.info("Initializing pylsp_rope")

    # Disable default plugins that conflicts with our plugin
    return {
        "plugins": {
            # "autopep8_format": {"enabled": False},
            # "definition": {"enabled": False},
            # "flake8_lint": {"enabled": False},
            # "folding": {"enabled": False},
            # "highlight": {"enabled": False},
            # "hover": {"enabled": False},
            # "jedi_completion": {"enabled": False},
            # "jedi_rename": {"enabled": False},
            # "mccabe_lint": {"enabled": False},
            # "preload_imports": {"enabled": False},
            # "pycodestyle_lint": {"enabled": False},
            # "pydocstyle_lint": {"enabled": False},
            # "pyflakes_lint": {"enabled": False},
            # "pylint_lint": {"enabled": False},
            # "references": {"enabled": False},
            # "rope_completion": {"enabled": False},
            # "rope_rename": {"enabled": False},
            # "signature": {"enabled": False},
            # "symbols": {"enabled": False},
            # "yapf_format": {"enabled": False},
        },
    }


@hookimpl
def pylsp_code_actions(config, workspace, document, range, context):
    logger.info("Retrieving code actions: %s %s %s %s %s", config, workspace, document, range, context)
    return [
        {
            "title": "Extract method",
            "kind": "refactor.extract",
            "command": "lsp_rope.refactor.extract",
            "arguments": [document.uri, range],
        }
    ]


@hookimpl
def pylsp_execute_command(config, workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s %s %s", config, workspace, command, arguments)
    if command == "lsp_rope.refactor.extract":
        current_document, range = arguments

        workspace_edit = {
            "changes": {
                current_document: [
                    {
                        "range": range,
                        "newText": "replacement text",
                    },
                ]
            }
        }

        logger.info("applying workspace edit: %s %s", command, workspace_edit)
        workspace.apply_edit(workspace_edit)


