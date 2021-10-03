import ast
import logging

import rope.base.exceptions
from pylsp import hookimpl
from rope.refactor import extract, inline

from pylsp_rope import commands
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
def pylsp_commands(config, workspace):
    return [getattr(commands, cmd) for cmd in dir(commands) if not cmd.startswith('_')]


@hookimpl
def pylsp_code_actions(config, workspace, document, range, context):
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)

    current_document, resource = get_resource(workspace, document.uri)
    range_selection = range["start"] != range["end"]
    position = range["start"]
    start_offset = current_document.offset_at_position(range["start"])
    end_offset = current_document.offset_at_position(range["end"])
    selected_text = document.source[start_offset:end_offset]

    code_actions = []

    # FIXME: requires rope.refactor.extract._ExceptionalConditionChecker for proper checking
    code_actions.append(
        {
            "title": "Extract method",
            "kind": "refactor.extract",
            "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": {
                "document_uri": document.uri,
                "range": range,
            },
        }
    )

    # FIXME: requires rope.refactor.extract._ExceptionalConditionChecker for proper checking
    try:
        ast.parse(selected_text, mode="eval")
    except SyntaxError:
        pass
    else:
        code_actions.append(
            {
                "title": "Extract variable",
                "kind": "refactor.extract",
                "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
                "arguments": {
                    "document_uri": document.uri,
                    "range": range,
                },
            },
        )

    try:
        can_inline = inline.create_inline(
            project=get_project(workspace),
            resource=resource,
            offset=current_document.offset_at_position(position),
        )
    except rope.base.exceptions.RefactoringError as e:
        pass
    else:
        code_actions.append(
            {
                "title": "Inline method/variable",
                "kind": "refactor.inline",
                "command": commands.COMMAND_REFACTOR_INLINE,
                "arguments": {
                    "document_uri": document.uri,
                    "position": range["start"],
                },
            },
        )

    return code_actions


@hookimpl
def pylsp_execute_command(config, workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s", command, arguments)

    if command == commands.COMMAND_REFACTOR_EXTRACT_METHOD:
        refactor_extract_method(workspace, **arguments)

    elif command == commands.COMMAND_REFACTOR_EXTRACT_VARIABLE:
        refactor_extract_variable(workspace, **arguments)

    elif command == commands.COMMAND_REFACTOR_INLINE:
        refactor_inline(workspace, **arguments)


def refactor_extract_method(workspace, document_uri, range):
    current_document, resource = get_resource(workspace, document_uri)

    refactoring = extract.ExtractMethod(
        project=get_project(workspace),
        resource=resource,
        start_offset=current_document.offset_at_position(range["start"]),
        end_offset=current_document.offset_at_position(range["end"]),
    )
    rope_changeset = refactoring.get_changes(
        extracted_name="extracted_method",
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
        extracted_name="extracted_variable",
    )
    apply_rope_changeset(workspace, rope_changeset)


def refactor_inline(workspace, document_uri, position):
    current_document, resource = get_resource(workspace, document_uri)

    refactoring = inline.create_inline(
        project=get_project(workspace),
        resource=resource,
        offset=current_document.offset_at_position(position),
    )
    rope_changeset = refactoring.get_changes()
    apply_rope_changeset(workspace, rope_changeset)
