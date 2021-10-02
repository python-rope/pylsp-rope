from unittest.mock import ANY

from pylsp_rope import plugin
from pylsp_rope.text import Position, Range


def test_code_action(config, workspace, document, code_action_context):
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

    workspace._endpoint.request.assert_called_once_with(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": {
                    document.uri: [
                        {
                            "range": {
                                "start": {"line": 3, "character": 0},
                                "end": {"line": 4, "character": 0},
                            },
                            "newText": "replacement text",
                        },
                    ],
                },
            },
        },
    )
