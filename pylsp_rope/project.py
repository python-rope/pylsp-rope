from functools import cache

from pylsp import uris
from rope.base import libutils
from rope.base.project import Project


@cache
def get_project(workspace):
    project = Project(workspace.root_path)
    project.validate()
    return project


def get_resource(workspace, document_uri):
    document = workspace.get_document(document_uri)
    resource = libutils.path_to_resource(get_project(workspace), document.path)
    return document, resource


def rope_changeset_to_workspace_changeset(workspace, rope_changeset):
    workspace_changeset = {}
    for change in rope_changeset.changes:
        doc = workspace.get_document(uris.from_fs_path(change.resource.real_path))
        document_changes = workspace_changeset.setdefault(doc.uri, [])
        document_changes.append(
            {
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": len(doc.lines), "character": 0},
                },
                "newText": change.new_contents,
            }
        )
    return workspace_changeset
