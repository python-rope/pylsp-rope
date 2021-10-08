from pylsp_rope import plugin, commands, typing
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_text_edits,
    assert_is_apply_edit_request,
    assert_modified_documents,
    assert_unmodified_document,
)


def test_use_function_globally(config, workspace, code_action_context):
    document = create_document(workspace, "function.py")
    document2 = create_document(workspace, "method_object.py")
    line = 0
    pos = document.lines[line].index("def add") + 4
    selection = Range((line, pos), (line, pos))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Use function",
        "kind": "refactor",
        "command": {
            "title": "Use function",
            "command": commands.COMMAND_REFACTOR_USE_FUNCTION,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "position": selection["start"],
                },
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

    workspace_edit = assert_is_apply_edit_request(edit_request)
    assert_modified_documents(workspace_edit, {document.uri, document2.uri})

    new_text = assert_text_edits(
        workspace_edit["changes"][document.uri], target="use_function.py"
    )
    assert "{add(a, b)}" in new_text

    new_text = assert_text_edits(
        workspace_edit["changes"][document2.uri], target="method_object_use_function.py"
    )
    assert "import function" in new_text
    assert "{function.add(a, b)}" in new_text


def test_use_function_in_current_file(config, workspace, code_action_context):
    document = create_document(workspace, "function.py")
    document2 = create_document(workspace, "method_object.py")

    line = 0
    pos = document.lines[line].index("def add") + 4
    selection = Range((line, pos), (line, pos))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Use function for current file only",
        "kind": "refactor",
        "command": {
            "title": "Use function for current file only",
            "command": commands.COMMAND_REFACTOR_USE_FUNCTION,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "position": selection["start"],
                    "documents": [document.uri],
                },
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

    workspace_edit = assert_is_apply_edit_request(edit_request)
    assert_modified_documents(workspace_edit, {document.uri})

    new_text = assert_text_edits(
        workspace_edit["changes"][document.uri], target="use_function.py"
    )
    assert "{add(a, b)}" in new_text

    assert_unmodified_document(workspace_edit, document2.uri)
