from unittest.mock import patch

from pylsp.lsp import MessageType

from pylsp_rope import commands, plugin
from pylsp_rope.plugin import pylsp_commands, pylsp_execute_command
from pylsp_rope.text import Position
from test.conftest import create_document
from test.helpers import assert_text_edits, assert_single_document_edit, assert_is_apply_edit_request


def test_command_registration(config, workspace):
    commands = pylsp_commands(config, workspace)

    assert isinstance(commands, list)
    assert all(isinstance(cmd, str) for cmd in commands)
    assert all(cmd.startswith("pylsp_rope.") for cmd in commands)


def test_command_error_handling(caplog, config, workspace, document):
    """
    pylsp_execute_command should never raise an error when executeCommand().

    Instead, we'll show an error message to the user.
    """

    arguments = [
        {
            "document_uri": document.uri,
            "position": Position(1),
        },
    ]

    with patch(
        "pylsp_rope.plugin.CommandRefactorInline.__call__",
        side_effect=Exception("some unexpected exception"),
    ):
        pylsp_execute_command(
            config,
            workspace,
            command=commands.COMMAND_REFACTOR_INLINE,
            arguments=arguments,
        )

    workspace._endpoint.notify.assert_called_once_with(
        "window/showMessage",
        params={
            "type": MessageType.Error,
            "message": f"pylsp-rope: some unexpected exception",
        },
    )
    assert "Traceback (most recent call last):" in caplog.text


def test_command_nothing_to_modify(config, workspace, document, code_action_context):
    document = create_document(workspace, "simple.py")

    command = commands.COMMAND_SOURCE_ORGANIZE_IMPORT
    arguments = [{"document_uri": document.uri}]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    workspace._endpoint.request.assert_not_called()
