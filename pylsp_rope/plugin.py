import logging

from pylsp import hookimpl
from rope.refactor import extract

from pylsp_rope.commands import (
    COMMAND_REFACTOR_EXTRACT_METHOD,
    COMMAND_REFACTOR_EXTRACT_VARIABLE,
)
from pylsp_rope.project import (
    get_project,
    get_resource,
    apply_rope_changeset,
)


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
        },
        {
            "title": "Extract variable",
            "kind": "refactor.extract",
            "command": COMMAND_REFACTOR_EXTRACT_VARIABLE,
            "arguments": [document.uri, range],
        },
    ]


@hookimpl
def pylsp_execute_command(config, workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s", command, arguments)
    if command == COMMAND_REFACTOR_EXTRACT_METHOD:
        document_uri, range = arguments
        refactor_extract_method(workspace, document_uri, range)
    elif command == COMMAND_REFACTOR_EXTRACT_VARIABLE:
        document_uri, range = arguments
        refactor_extract_variable(workspace, document_uri, range)


def refactor_extract_method(workspace, document_uri, range):
    current_document, resource = get_resource(workspace, document_uri)

    refactoring = extract.ExtractMethod(
        project=get_project(workspace),
        resource=resource,
        start_offset=current_document.offset_at_position(range["start"]),
        end_offset=current_document.offset_at_position(range["end"]),
    )
    rope_changeset = refactoring.get_changes(
        extracted_name="new_method",
    )
    apply_rope_changeset(workspace, rope_changeset)


def refactor_extract_variable(workspace, document_uri, range):
    current_document, resource = get_resource(workspace, document_uri)

    refactoring = extract.ExtractVariable(
        project=get_project(workspace),
        resource=resource,
        start_offset=current_document.offset_at_position(range["start"]),
        end_offset=current_document.offset_at_position(range["end"]),
    )
    rope_changeset = refactoring.get_changes(
        extracted_name="new_variable",
    )
    apply_rope_changeset(workspace, rope_changeset)
