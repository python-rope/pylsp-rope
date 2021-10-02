from unittest.mock import ANY, call

from pylsp_rope import plugin, commands
from pylsp_rope.text import Range
from test.conftest import fixtures_dir


def test_extract_method(config, workspace, document, code_action_context):
    selection = Range(4)

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
        "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
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
    new_text = assert_wholefile_changeset(
        document_changeset, target=fixtures_dir / "simple_extract_method.py"
    )
    assert "def extracted_method(" in new_text


def test_extract_variable(config, workspace, document, code_action_context):
    line = 4
    start_col = document.lines[line].index("sys")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

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
        "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
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
    new_text = assert_wholefile_changeset(
        document_changeset, target=fixtures_dir / "simple_extract_variable.py"
    )
    assert "extracted_variable = " in new_text


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

    (document_changeset,) = edit_request[0][1]["edit"]["changes"].values()
    for change in document_changeset:
        assert change == {
            "range": {
                "start": {"line": ANY, "character": ANY},
                "end": {"line": ANY, "character": ANY},
            },
            "newText": ANY,
        }

    return document_changeset


def assert_wholefile_changeset(document_changeset, target):
    assert len(document_changeset) == 1
    (change,) = document_changeset
    new_text = open(target, "r").read()
    assert change["newText"] == new_text
    return new_text
