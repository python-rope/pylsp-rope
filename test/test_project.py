from rope.refactor import inline

from pylsp_rope.project import (
    get_project,
    get_resource,
    rope_changeset_to_workspace_edit,
)
from pylsp_rope.typing import (
    is_workspace_edit_with_changes,
    is_workspace_edit_with_document_changes,
)
from test.conftest import create_document


EXPECTED_EDITS = [
    {
        "range": {
            "start": {"line": 2, "character": 0},
            "end": {"line": 3, "character": 0},
        },
        "newText": "",
    },
    {
        "range": {
            "start": {"line": 4, "character": 0},
            "end": {"line": 5, "character": 0},
        },
        "newText": 'print("world")\n',
    },
    {
        "range": {
            "start": {"line": 15, "character": 0},
            "end": {"line": 16, "character": 0},
        },
        "newText": '    os.path.join("world", roses)\n',
    },
]


def test_rope_changeset_to_workspace_changeset_changes(workspace):
    document = create_document(workspace, "many_changes.py")
    rope_changeset = get_rope_changeset(workspace, document)
    workspace_edit = rope_changeset_to_workspace_edit(
        workspace,
        rope_changeset,
        workspace_edit_format=["changes"],
    )

    assert is_workspace_edit_with_changes(workspace_edit)
    assert workspace_edit["changes"] == {
        document.uri: EXPECTED_EDITS,
    }


def test_rope_changeset_to_workspace_changeset_document_changes(workspace):
    document = create_document(workspace, "many_changes.py")
    rope_changeset = get_rope_changeset(workspace, document)
    workspace_edit = rope_changeset_to_workspace_edit(
        workspace,
        rope_changeset,
        workspace_edit_format=["documentChanges"],
    )

    assert is_workspace_edit_with_document_changes(workspace_edit)
    assert workspace_edit["documentChanges"] == [
        {
            "textDocument": {
                "uri": document.uri,
                "version": None,
            },
            "edits": EXPECTED_EDITS,
        },
    ]


def get_rope_changeset(workspace, document):
    _, resource = get_resource(workspace, document.uri)
    offset = document.source.index("hello = ")

    refactoring = inline.create_inline(
        project=get_project(workspace),
        resource=resource,
        offset=offset,
    )
    rope_changeset = refactoring.get_changes()
    return rope_changeset
