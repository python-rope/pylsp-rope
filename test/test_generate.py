from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import assert_single_document_edit, assert_text_edits


def test_generate_variable(config, workspace, code_action_context):
    document = create_document(workspace, "undefined_variable.py")
    line = 1
    start_col = end_col = document.lines[line].index("undef_var")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Generate variable",
        "kind": "quickfix",
        "command": {
            "title": "Generate variable",
            "command": commands.COMMAND_GENERATE_CODE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "position": selection["start"],
                    "generate_kind": "variable",
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
    new_text = assert_text_edits(document_edits, target="generate_variable.py")
    assert "undef_var = None" in new_text


def test_generate_function(config, workspace, code_action_context):
    document = create_document(workspace, "undefined_variable.py")
    line = 1
    start_col = end_col = document.lines[line].index("undef_var")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Generate function",
        "kind": "quickfix",
        "command": {
            "title": "Generate function",
            "command": commands.COMMAND_GENERATE_CODE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "position": selection["start"],
                    "generate_kind": "function",
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
    new_text = assert_text_edits(document_edits, target="generate_function.py")
    assert "def undef_var():" in new_text


def test_generate_class(config, workspace, code_action_context):
    document = create_document(workspace, "undefined_variable.py")
    line = 1
    start_col = end_col = document.lines[line].index("undef_var")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Generate class",
        "kind": "quickfix",
        "command": {
            "title": "Generate class",
            "command": commands.COMMAND_GENERATE_CODE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "position": selection["start"],
                    "generate_kind": "class",
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
    new_text = assert_text_edits(document_edits, target="generate_class.py")
    assert "class undef_var(object):" in new_text
