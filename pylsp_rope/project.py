import logging
from functools import lru_cache

from pylsp import uris
from rope.base import libutils
from rope.base.project import Project

from pylsp_rope.lsp_diff import lsp_diff


logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def _get_project(workspace):
    project = Project(workspace.root_path)
    return project


def get_project(workspace):
    project = _get_project(workspace)
    project.validate()
    return project


def get_resource(workspace, document_uri):
    document = workspace.get_document(document_uri)
    resource = libutils.path_to_resource(get_project(workspace), document.path)
    return document, resource


def get_document(workspace, resource):
    return workspace.get_document(uris.from_fs_path(resource.real_path))


def rope_changeset_to_workspace_changeset(workspace, rope_changeset):
    def _get_contents(change):
        old = change.old_contents
        new = change.new_contents
        if old is None:
            if change.resource.exists():
                old = change.resource.read()
            else:
                old = ""
        return old.splitlines(keepends=True), new.splitlines(keepends=True)

    workspace_changeset = {}
    for change in rope_changeset.changes:
        lines_old, lines_new = _get_contents(change)

        document = get_document(workspace, change.resource)
        document_changes = workspace_changeset.setdefault(document.uri, [])
        document_changes.extend(lsp_diff(lines_old, lines_new))

    return workspace_changeset


def apply_rope_changeset(workspace, rope_changeset):
    workspace_changeset = rope_changeset_to_workspace_changeset(
        workspace,
        rope_changeset,
    )

    workspace_edit = {
        "changes": workspace_changeset,
    }

    logger.info("applying workspace edit: %s", workspace_edit)
    workspace.apply_edit(workspace_edit)
