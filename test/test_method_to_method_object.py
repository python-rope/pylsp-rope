from pylsp_rope import commands, plugin
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_changeset,
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

    expected = {
        "title": "To method object",
        "kind": "refactor",
        "command": {
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

    command = expected["command"]["command"]
    arguments = expected["command"]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_changeset = assert_single_document_edit(edit_request, document)
    new_text = assert_changeset(document_changeset, target="method_object.py")
    assert "class NewMethodObject(object)" in new_text
    assert "NewMethodObject(a, b)()" in new_text
