from unittest.mock import Mock

import pytest
from pylsp import uris
from pylsp.config.config import Config
from pylsp.workspace import Workspace, Document


DOC_URI = uris.from_fs_path(__file__)
DOC = """\
import sys
def main():
    print(sys.stdin.read())
"""

@pytest.fixture
def config(workspace):
    """Return a config object."""
    cfg = Config(workspace.root_uri, {}, 0, {})
    cfg._plugin_settings = {
        "plugins": {
            "pylint": {
                "enabled": False,
                "args": [],
                "executable": None,
            },
        },
    }
    return cfg


@pytest.fixture
def workspace(tmpdir):
    """Return a workspace."""
    ws = Workspace(uris.from_fs_path(str(tmpdir)), Mock())
    ws._config = Config(ws.root_uri, {}, 0, {})
    return ws


@pytest.fixture
def document(workspace):
    return Document(DOC_URI, workspace, DOC)


@pytest.fixture
def code_action_context():
    # https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#codeActionKind
    code_action_kind = [
        "",
        "quickfix",
        "refactor",
        "refactor.extract",
        "refactor.inline",
        "refactor.rewrite",
        "source",
        "source.organizeImports",
        "source.fixAll",
    ]

    return {
        "diagnostics": [],
        "only": code_action_kind,
    }
