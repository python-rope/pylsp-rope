import logging

from pylsp import hookimpl, uris
from rope.refactor import extract

from pylsp_rope.commands import COMMAND_REFACTOR_EXTRACT_METHOD
from pylsp_rope.project import get_project, get_resource


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
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)
    return [
        {
            "title": "Extract method",
            "kind": "refactor.extract",
            "command": COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": [document.uri, range],
        }
    ]


@hookimpl
def pylsp_execute_command(config, workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s", command, arguments)
    if command == COMMAND_REFACTOR_EXTRACT_METHOD:
        current_document_uri, range = arguments

        project = get_project(workspace)
        current_document, resource = get_resource(workspace, current_document_uri)
        refactoring = extract.ExtractMethod(
            project=project,
            resource=resource,
            start_offset=current_document.offset_at_position(range["start"]),
            end_offset=current_document.offset_at_position(range["end"]),
        )
        rope_changeset = refactoring.get_changes(extracted_name="new_extracted")

        workspace_changes = {}
        for change in rope_changeset.changes:
            doc = workspace.get_document(uris.from_fs_path(change.resource.real_path))
            document_changes = workspace_changes.setdefault(doc.uri, [])
            document_changes.append({
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": len(doc.lines), "character": 0},
                },
                "newText": change.new_contents,
            })

        workspace_edit = {
            "changes": workspace_changes,
        }

        logger.info("applying workspace edit: %s %s", command, workspace_edit)
        workspace.apply_edit(workspace_edit)


