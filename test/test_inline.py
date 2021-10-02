from pylsp_rope import plugin, commands
from pylsp_rope.text import Range
from test.conftest import fixtures_dir, create_document
from test.helpers import assert_single_document_edit, assert_wholefile_changeset


def test_inline(config, workspace, code_action_context):
    document = create_document(workspace, "simple_extract_method.py")
    line = 6
    start_col = end_col = document.lines[line].index("extracted_method")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected = {
        "title": "Inline method/variable",
        "kind": "refactor.inline",
        "command": commands.COMMAND_REFACTOR_INLINE,
        "arguments": [document.uri, selection],
    }

    assert expected in response

    command = expected["command"]
    arguments = expected["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_changeset = assert_single_document_edit(edit_request, document)
    new_text = assert_wholefile_changeset(
        document_changeset, target=fixtures_dir / "simple.py"
    )
    assert "extracted_method" not in new_text
