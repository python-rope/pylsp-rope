from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.helpers import (
    assert_text_edits,
    assert_code_actions_do_not_offer,
    assert_single_document_edit,
)


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

    expected: typing.CodeAction = {
        "title": "Extract variable",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract variable",
            "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                }
            ],
        },
    }

    assert expected in response

    assert expected["command"] is not None
    command = expected["command"]["command"]
    arguments = expected["command"]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_edits = assert_single_document_edit(edit_request, document)
    new_text = assert_text_edits(document_edits, target="simple_extract_variable.py")
    assert "extracted_variable = " in new_text


def test_extract_variable_not_offered_when_selecting_non_expression(
    config, workspace, document, code_action_context
):
    line = 4
    start_col = document.lines[line].index("print")
    end_col = document.lines[line].index(".read())\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    assert_code_actions_do_not_offer(
        response,
        command=commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
    )


def test_extract_method(config, workspace, document, code_action_context):
    selection = Range(4)

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract method",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract method",
            "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                }
            ],
        },
    }

    assert expected in response

    assert expected["command"] is not None
    command = expected["command"]["command"]
    arguments = expected["command"]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_edits = assert_single_document_edit(edit_request, document)
    new_text = assert_text_edits(document_edits, target="simple_extract_method.py")
    assert "def extracted_method(" in new_text
