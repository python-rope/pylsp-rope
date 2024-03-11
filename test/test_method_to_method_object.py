from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_text_edits,
    assert_code_actions_do_not_offer,
    assert_single_document_edit,
)


def test_method_to_method_object(config, workspace, code_action_context):
    document = create_document(workspace, "function.py")
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
        "title": "To method object",
        "kind": "refactor.rewrite",
        "command": {
            "title": "To method object",
            "command": commands.COMMAND_REFACTOR_METHOD_TO_METHOD_OBJECT,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "position": selection["start"],
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
    new_text = assert_text_edits(document_edits, target="method_object.py")
    assert "class NewMethodObject(object)" in new_text
    assert "NewMethodObject(a, b)()" in new_text


def test_method_to_method_object_not_offered_when_selecting_unsuitable_range(
    config, workspace, code_action_context
):
    document = create_document(workspace, "function.py")
    line = 1
    pos = document.lines[line].index("return")
    selection = Range((line, pos), (line, pos))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    assert_code_actions_do_not_offer(
        response,
        command=commands.COMMAND_REFACTOR_INLINE,
    )
