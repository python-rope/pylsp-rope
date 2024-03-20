import logging
from typing import List, Optional

from pylsp import hookimpl, uris
from rope.base import libutils
from pylsp.lsp import MessageType
from rope.refactor.rename import Rename

from pylsp_rope import refactoring, typing, commands
from pylsp_rope.project import (
    get_project,
    get_resource,
    get_resources,
    rope_changeset_to_workspace_edit,
    new_project,
)


logger = logging.getLogger(__name__)


@hookimpl
def pylsp_settings():
    logger.info("Initializing pylsp_rope")

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
            "pylsp_rope": {
                "enabled": True,
                "rename": False,
            },
            # "signature": {"enabled": False},
            # "symbols": {"enabled": False},
            # "yapf_format": {"enabled": False},
        },
    }


@hookimpl
def pylsp_commands(config, workspace) -> List[str]:
    return [getattr(commands, cmd) for cmd in dir(commands) if not cmd.startswith("_")]


@hookimpl
def pylsp_code_actions(
    config,
    workspace,
    document,
    range,
    context,
) -> List[typing.CodeAction]:
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)

    class info:
        current_document, resource = get_resource(workspace, document.uri)
        position = range["start"]
        start_offset = current_document.offset_at_position(range["start"])
        end_offset = current_document.offset_at_position(range["end"])
        selected_text = document.source[start_offset:end_offset]

    project = get_project(workspace)
    for resource in get_resources(workspace, workspace.documents.keys()):
        project.pycore._invalidate_resource_cache(resource)

    commands = {}
    commands.update(
        refactoring.CommandRefactorExtractMethod.get_code_actions(
            workspace,
            document=document,
            range=range,
        ),
    )
    commands.update(
        refactoring.CommandRefactorExtractVariable.get_code_actions(
            workspace,
            document=document,
            range=range,
        ),
    )
    commands.update(
        {
            "Inline method/variable/parameter": refactoring.CommandRefactorInline(
                workspace,
                document_uri=document.uri,
                position=info.position,
            ),
            "Use function": refactoring.CommandRefactorUseFunction(
                workspace,
                document_uri=document.uri,
                position=info.position,
            ),
            "Use function for current file only": refactoring.CommandRefactorUseFunction(
                workspace,
                document_uri=document.uri,
                position=info.position,
                documents=[document.uri],
            ),
            "To method object": refactoring.CommandRefactorMethodToMethodObject(
                workspace,
                document_uri=document.uri,
                position=info.position,
            ),
            "Convert local variable to field": refactoring.CommandRefactorLocalToField(
                workspace,
                document_uri=document.uri,
                position=info.position,
            ),
            "Organize import": refactoring.CommandSourceOrganizeImport(
                workspace,
                document_uri=document.uri,
            ),
            "Introduce parameter": refactoring.CommandIntroduceParameter(
                workspace,
                document_uri=document.uri,
                position=info.position,
            ),
        }
    )
    commands.update(
        refactoring.GenerateCode.get_code_actions(
            workspace,
            document=document,
            position=info.position,
        ),
    )

    return [
        cmd.get_code_action(title=title)
        for title, cmd in commands.items()
        if cmd.is_valid(info)
    ]


@hookimpl
def pylsp_execute_command(config, workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s", command, arguments)

    commands = {cmd.name: cmd for cmd in refactoring.Command.__subclasses__()}

    try:
        return commands[command](workspace, **arguments[0])(
            # FIXME: Hardcode executeCommand to use WorkspaceEditWithChanges
            #        We need to upgrade this at some point.
            workspace_edit_format=["changes"],
        )
    except Exception as exc:
        logger.exception(
            "Exception when doing workspace/executeCommand: %s",
            str(exc),
            exc_info=exc,
        )
        workspace.show_message(
            f"pylsp-rope: {exc}",
            msg_type=MessageType.Error,
        )


@hookimpl
def pylsp_rename(
    config,
    workspace,
    document,
    position,
    new_name,
) -> Optional[typing.WorkspaceEdit]:
    cfg = config.plugin_settings("pylsp_rope", document_path=document.uri)
    if not cfg.get("rename", False):
        return None

    logger.info("textDocument/rename: %s %s %s", document, position, new_name)
    project = new_project(workspace)  # FIXME: we shouldn't have to always keep creating new projects here
    document, resource = get_resource(workspace, document.uri, project=project)

    rename = Rename(
        project=project,
        resource=resource,
        offset=document.offset_at_position(position),
    )

    logger.debug(
        "Executing rename of %s to %s",
        document.word_at_position(position),
        new_name,
    )

    rope_changeset = rename.get_changes(new_name, in_hierarchy=True, docs=True)

    logger.debug("Finished rename: %s", rope_changeset.changes)
    workspace_edit = rope_changeset_to_workspace_edit(
        workspace,
        rope_changeset,
    )
    return workspace_edit
