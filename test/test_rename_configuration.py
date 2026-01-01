"""
Integration test examples showing how to configure pylsp-rope rename functionality.

This file demonstrates the configuration patterns that users should follow
to enable and verify pylsp-rope's rename feature.
"""

import pytest
from pylsp_rope import typing
from pylsp_rope.plugin import pylsp_rename, pylsp_settings
from pylsp_rope.text import Position
from test.conftest import create_document
from test.helpers import assert_text_edits


class TestRenameConfigurationExamples:
    """Examples showing proper configuration of pylsp-rope rename."""

    def test_default_configuration_disables_rename(self, config, workspace):
        """Test that rename is disabled by default."""
        # Get default settings
        settings = pylsp_settings()
        assert settings["plugins"]["pylsp_rope"]["rename"] is False

        # Verify rename returns None when disabled
        document = create_document(workspace, "simple_rename.py")
        position = Position(0, 0)  # Position on "Test1"

        response = pylsp_rename(config, workspace, document, position, "NewName")
        assert response is None

    def test_enabling_rename_via_configuration(self, config, workspace):
        """Example of enabling rename through configuration."""
        # Simulate user configuration
        config._plugin_settings["plugins"]["pylsp_rope"] = {"rename": True}

        document = create_document(workspace, "simple_rename.py")
        line = 0
        pos = document.lines[line].index("Test1")
        position = Position(line, pos)

        response = pylsp_rename(
            config, workspace, document, position, "ShouldBeRenamed"
        )

        # Rename should now work
        assert response is not None
        assert typing.is_workspace_edit_with_changes(response)

        # Verify the rename happened
        changes = response["changes"]
        doc_uri = typing.DocumentUri(document.uri)
        assert doc_uri in changes
        new_text = assert_text_edits(changes[doc_uri], target="simple_rename_result.py")
        assert "class ShouldBeRenamed()" in new_text

    def test_configuration_with_other_rename_plugins_disabled(self, config):
        """Example showing complete rename configuration."""
        settings = pylsp_settings()

        # This is the recommended configuration pattern:
        config_dict = {
            "pylsp": {
                "plugins": {
                    "pylsp_rope": {"enabled": True, "rename": True},
                    "jedi_rename": {"enabled": False},
                }
            }
        }

        # Verify pylsp-rope settings match recommendation
        pylsp_rope_settings = settings["plugins"]["pylsp_rope"]
        assert pylsp_rope_settings["enabled"] is True
        assert (
            pylsp_rope_settings["rename"] is False
        )  # Default, user should set to True

    def test_disabling_rename_after_enabling(self, config, workspace):
        """Test that rename can be dynamically disabled."""
        # First enable rename
        config._plugin_settings["plugins"]["pylsp_rope"] = {"rename": True}

        document = create_document(workspace, "simple_rename.py")
        line = 0
        pos = document.lines[line].index("Test1")
        position = Position(line, pos)

        # Rename should work
        response = pylsp_rename(config, workspace, document, position, "NewName")
        assert response is not None

        # Now disable rename
        config._plugin_settings["plugins"]["pylsp_rope"] = {"rename": False}

        # Rename should not work
        response = pylsp_rename(config, workspace, document, position, "AnotherName")
        assert response is None

    def test_missing_configuration_key_defaults_to_disabled(self, config, workspace):
        """Test that missing configuration key defaults to disabled."""
        # Remove the rename key entirely
        plugin_settings = config.plugin_settings("pylsp_rope", "test://test.py")
        if "rename" in plugin_settings:
            del plugin_settings["rename"]

        document = create_document(workspace, "simple_rename.py")
        position = Position(0, 5)

        # Should return None when key is missing
        response = pylsp_rename(config, workspace, document, position, "NewName")
        assert response is None
