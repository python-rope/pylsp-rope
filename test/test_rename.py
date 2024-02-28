import pytest
from pylsp_rope import typing
from pylsp_rope.plugin import pylsp_rename
from pylsp_rope.text import Position
from test.conftest import create_document
from test.helpers import assert_text_edits, assert_modified_documents


@pytest.fixture(autouse=True)
def enable_pylsp_rope_rename_plugin(config):
    config._plugin_settings["plugins"]["pylsp_rope"] = {"rename": True}
    return config


def test_rope_rename(config, workspace) -> None:
    document = create_document(workspace, "simple_rename.py")
    extra_document = create_document(workspace, "simple_rename_extra.py")
    line = 0
    pos = document.lines[line].index("Test1")
    position = Position(line, pos)

    response: typing.SimpleWorkspaceEdit = pylsp_rename(config, workspace, document, position, "ShouldBeRenamed")
    assert len(response.keys()) == 1

    assert_modified_documents(response, {document.uri, extra_document.uri})

    new_text = assert_text_edits(
        response["changes"][document.uri], target="simple_rename_result.py"
    )
    assert "class ShouldBeRenamed()" in new_text
    assert "class Test2(ShouldBeRenamed)" in new_text

    new_text = assert_text_edits(
        response["changes"][extra_document.uri], target="simple_rename_extra_result.py"
    )
    assert "from simple_rename import ShouldBeRenamed" in new_text
    assert "x = ShouldBeRenamed()" in new_text


def test_rope_rename_disabled(config, workspace) -> None:
    document = create_document(workspace, "simple_rename.py")
    extra_document = create_document(workspace, "simple_rename_extra.py")
    line = 0
    pos = document.lines[line].index("Test1")
    position = Position(line, pos)

    plugin_settings = config.plugin_settings("pylsp_rope", document.uri)
    plugin_settings["rename"] = False

    response: typing.SimpleWorkspaceEdit = pylsp_rename(config, workspace, document, position, "ShouldBeRenamed")

    assert response is None


def test_rope_rename_missing_key(config, workspace) -> None:
    document = create_document(workspace, "simple_rename.py")
    extra_document = create_document(workspace, "simple_rename_extra.py")
    line = 0
    pos = document.lines[line].index("Test1")
    position = Position(line, pos)

    plugin_settings = config.plugin_settings("pylsp_rope", document.uri)
    del plugin_settings["rename"]

    response: typing.SimpleWorkspaceEdit = pylsp_rename(config, workspace, document, position, "ShouldBeRenamed")

    assert response is None
