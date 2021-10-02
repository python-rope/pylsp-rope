from unittest.mock import ANY, call

from pylsp_rope import plugin
from pylsp_rope.text import Position, Range


def test_extract_method(config, workspace, document, code_action_context):
    selection = Range(3)

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected = [
        {
            "title": "Extract method",
            "kind": "refactor.extract",
            "command": "lsp_rope.refactor.extract",
            "arguments": [document.uri, selection],
        }
    ]

    assert response == expected

    command = response[0]["command"]
    arguments = response[0]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    assert edit_request == call(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": {
                    document.uri: [
                        {
                            "range": {
                                "start": {"line": ANY, "character": ANY},
                                "end": {"line": ANY, "character": ANY},
                            },
                            "newText": ANY,
                        },
                    ],
                },
            },
        },
    )

    assert document.uri in edit_request[0][1]["edit"]["changes"]
