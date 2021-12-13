from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.conftest import create_document
from test.helpers import (
    assert_code_actions_do_not_offer,
    assert_single_document_edit,
    assert_text_edits,
)


def test_extract_variable(config, workspace, code_action_context):
    document = create_document(workspace, "simple.py")
    line = 6
    start_col = document.lines[line].index("a + b")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract variable",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract variable",
            "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": False,
                    "similar": False,
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
    new_text = assert_text_edits(document_edits, target="simple_extract_variable.py")
    assert "extracted_variable = " in new_text
    assert new_text.count("a + b") == 3


def test_extract_variable_with_similar(config, workspace, code_action_context):
    document = create_document(workspace, "simple.py")
    line = 6
    start_col = document.lines[line].index("a + b")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract variable including similar statements",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract variable including similar statements",
            "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": False,
                    "similar": True,
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
    new_text = assert_text_edits(
        document_edits, target="simple_extract_variable_with_similar.py"
    )
    assert "extracted_variable = " in new_text
    assert new_text.count("a + b") == 2


def test_extract_global_variable(config, workspace, code_action_context):
    document = create_document(workspace, "method.py")
    line = 6
    start_col = document.lines[line].index("sys.stdin.read()")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract global variable",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract global variable",
            "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": True,
                    "similar": False,
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
    new_text = assert_text_edits(
        document_edits, target="method_with_global_variable.py"
    )
    assert "extracted_variable = " in new_text
    assert new_text.count("extracted_variable = sys.stdin.read()") == 1
    assert new_text.count("sys.stdin.read()") == 2


def test_extract_global_variable_with_similar(config, workspace, code_action_context):
    document = create_document(workspace, "method.py")
    line = 6
    start_col = document.lines[line].index("sys.stdin.read()")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract global variable including similar statements",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract global variable including similar statements",
            "command": commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": True,
                    "similar": True,
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
    new_text = assert_text_edits(
        document_edits, target="method_with_similar_global_variable.py"
    )
    assert "extracted_variable = " in new_text
    assert new_text.count("extracted_variable = sys.stdin.read()") == 1
    assert new_text.count("sys.stdin.read()") == 1


def test_extract_variable_not_offered_when_selecting_non_expression(
    config, workspace, document, code_action_context
):
    line = 6
    start_col = document.lines[line].index("print")
    end_col = document.lines[line].index("+")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    assert_code_actions_do_not_offer(
        response,
        command=commands.COMMAND_REFACTOR_EXTRACT_VARIABLE,
    )


def test_extract_method(config, workspace, code_action_context):
    document = create_document(workspace, "simple.py")
    selection = Range(6)

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract method",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract method",
            "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": False,
                    "similar": False,
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
    new_text = assert_text_edits(document_edits, target="simple_extract_method.py")
    assert "def extracted_method(" in new_text
    assert new_text.count("print(a + b)") == 2
    assert new_text.count("extracted_method(a, b)\n") == 1


def test_extract_method_with_similar(config, workspace, code_action_context):
    document = create_document(workspace, "simple.py")
    selection = Range(6)

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract method including similar statements",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract method including similar statements",
            "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": False,
                    "similar": True,
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
    new_text = assert_text_edits(
        document_edits, target="simple_extract_method_with_similar.py"
    )
    assert "def extracted_method(" in new_text
    assert new_text.count("print(a + b)") == 1
    assert new_text.count("extracted_method(a, b)\n") == 2


def test_extract_global_method(config, workspace, code_action_context):
    document = create_document(workspace, "method.py")
    line = 6
    start_col = document.lines[line].index("sys.stdin.read()")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract global method",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract global method",
            "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": True,
                    "similar": False,
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
    new_text = assert_text_edits(
        document_edits, target="method_with_global_function.py"
    )
    assert "def extracted_method(" in new_text
    assert new_text.count("return sys.stdin.read()") == 1
    assert new_text.count("sys.stdin.read()") == 2
    assert new_text.count("extracted_method()") == 2


def test_extract_method_global_with_similar(config, workspace, code_action_context):
    document = create_document(workspace, "method.py")
    line = 6
    start_col = document.lines[line].index("sys.stdin.read()")
    end_col = document.lines[line].index(")\n")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected: typing.CodeAction = {
        "title": "Extract global method including similar statements",
        "kind": "refactor.extract",
        "command": {
            "title": "Extract global method including similar statements",
            "command": commands.COMMAND_REFACTOR_EXTRACT_METHOD,
            "arguments": [
                {
                    "document_uri": document.uri,
                    "range": selection,
                    "global_": True,
                    "similar": True,
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
    new_text = assert_text_edits(
        document_edits, target="method_with_similar_global_function.py"
    )
    assert "def extracted_method(" in new_text
    assert new_text.count("return sys.stdin.read()") == 1
    assert new_text.count("sys.stdin.read()") == 1
    assert new_text.count("extracted_method()") == 3
