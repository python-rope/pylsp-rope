from unittest.mock import ANY, call

from pylsp_rope import plugin
from pylsp_rope.commands import (
    COMMAND_REFACTOR_EXTRACT_METHOD,
    COMMAND_REFACTOR_EXTRACT_VARIABLE,
)
from pylsp_rope.text import Range


def test_extract_method(config, workspace, document, code_action_context):
    selection = Range(3)

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected = {
        "title": "Extract method",
        "kind": "refactor.extract",
        "command": COMMAND_REFACTOR_EXTRACT_METHOD,
        "arguments": [document.uri, selection],
    }

    assert expected in response

    command = expected["command"]
    arguments = expected["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_changeset = assert_single_document_edit(edit_request, document)

    assert document.uri in edit_request[0][1]["edit"]["changes"]
    assert "def new_method(" in list(edit_request[0][1]["edit"]["changes"].values())[0][0]["newText"]


def test_extract_variable(config, workspace, document, code_action_context):
    selection = Range(3)

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected = {
        "title": "Extract variable",
        "kind": "refactor.extract",
        "command": COMMAND_REFACTOR_EXTRACT_VARIABLE,
        "arguments": [document.uri, selection],
    }

    assert expected in response

    command = expected["command"]
    arguments = expected["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_changeset = assert_single_document_edit(edit_request, document)

    assert document.uri in edit_request[0][1]["edit"]["changes"]
    assert "new_variable = " in list(edit_request[0][1]["edit"]["changes"].values())[0][0]["newText"]


def assert_single_document_edit(edit_request, document):
    assert edit_request == call(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": {
                    document.uri: ANY,
                },
            },
        },
    )

    document_changeset, = edit_request[0][1]["edit"]["changes"].values()
    for change in document_changeset:
        assert change == {
            "range": {
                "start": {"line": ANY, "character": ANY},
                "end": {"line": ANY, "character": ANY},
            },
            "newText": ANY,
        }

    return document_changeset
