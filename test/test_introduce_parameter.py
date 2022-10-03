from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_code_actions_do_not_offer,
    assert_single_document_edit,
    assert_text_edits,
)


def test_introduce_parameter(config, workspace, code_action_context):
    document = create_document(workspace, "simple.py")
    line = 4
    pos = document.lines[line].index("stdin.read()")
    selection = Range((line, pos), (line, pos))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Introduce parameter",
        "kind": "refactor",
        "command": {
            "title": "Introduce parameter",
            "command": commands.COMMAND_INTRODUCE_PARAMETER,
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
    new_text = assert_text_edits(document_edits, target="introduce_parameter.py")
    assert "new_parameter=sys.stdin" in new_text
    assert "new_parameter.read()" in new_text
