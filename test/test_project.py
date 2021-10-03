from rope.refactor import inline

from pylsp_rope.project import (
    get_project,
    get_resource,
    rope_changeset_to_workspace_changeset,
)
from test.conftest import create_document


def test_rope_changeset_to_workspace_changeset(workspace):
    document = create_document(workspace, "many_changes.py")
    rope_changeset = get_rope_changeset(workspace, document)
    workspace_changeset = rope_changeset_to_workspace_changeset(
        workspace,
        rope_changeset,
    )

    assert workspace_changeset == {
        document.uri: [
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
    }


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
