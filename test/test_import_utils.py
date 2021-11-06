from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_text_edits,
    assert_single_document_edit,
)


def test_organize_import(config, workspace, document, code_action_context):
    document = create_document(workspace, "redundant_import.py")
    line = 1
    start_col = 0
    end_col = 0
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Organize import",
        "kind": "source.organizeImports",
        "command": {
            "title": "Organize import",
            "command": commands.COMMAND_SOURCE_ORGANIZE_IMPORT,
            "arguments": [
                {
                    "document_uri": document.uri,
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
    new_text = assert_text_edits(document_edits, target="simple.py")
    assert document.source.count("import sys") == 2
    assert new_text.count("import sys") == 1
