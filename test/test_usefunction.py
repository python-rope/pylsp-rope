from pylsp_rope import plugin, commands
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_changeset,
    assert_is_apply_edit_request,
    assert_modified_documents,
    assert_single_document_edit,
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

    expected = {
        "title": "Use function",
        "kind": "refactor",
        "command": {
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

    command = expected["command"]["command"]
    arguments = expected["command"]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    workspace_changeset = assert_is_apply_edit_request(edit_request)
    assert_modified_documents(workspace_changeset, {document.uri, document2.uri})

    new_text = assert_changeset(
        workspace_changeset[document.uri], target="use_function.py"
    )
    assert "{add(a, b)}" in new_text

    new_text = assert_changeset(
        workspace_changeset[document2.uri], target="method_object_use_function.py"
    )
    assert "import function" in new_text
    assert "{function.add(a, b)}" in new_text