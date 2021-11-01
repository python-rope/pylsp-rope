import logging
from functools import lru_cache
from typing import List, Dict, Tuple

from pylsp import uris, workspace
from rope.base import libutils
from rope.base.fscommands import FileSystemCommands

from pylsp_rope import rope
from pylsp_rope.lsp_diff import lsp_diff
from pylsp_rope.typing import WorkspaceEdit, DocumentUri, TextEdit, Line


logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_project(workspace) -> rope.Project:
    fscommands = WorkspaceFileCommands(workspace)
    return rope.Project(workspace.root_path, fscommands=fscommands)


def get_resource(
    workspace, document_uri: DocumentUri
) -> Tuple[workspace.Document, rope.Resource]:
    document = workspace.get_document(document_uri)
    resource = libutils.path_to_resource(get_project(workspace), document.path)
    return document, resource


def get_resources(workspace, documents: List[DocumentUri]) -> List[rope.Resource]:
    if documents is None:
        return None
    return [get_resource(workspace, document_uri)[1] for document_uri in documents]


def get_document(workspace, resource: rope.Resource) -> workspace.Document:
    return workspace.get_document(uris.from_fs_path(resource.real_path))


def rope_changeset_to_workspace_edit(
    workspace, rope_changeset: rope.ChangeSet
) -> WorkspaceEdit:
    def _get_contents(change: rope.Change) -> Tuple[List[Line], List[Line]]:
        old = change.old_contents
        new = change.new_contents
        if old is None:
            if change.resource.exists():
                old = change.resource.read()
            else:
                old = ""
        return old.splitlines(keepends=True), new.splitlines(keepends=True)

    workspace_changeset: Dict[DocumentUri, List[TextEdit]] = {}
    for change in rope_changeset.changes:
        lines_old, lines_new = _get_contents(change)

        document = get_document(workspace, change.resource)
        document_changes = workspace_changeset.setdefault(document.uri, [])
        document_changes.extend(lsp_diff(lines_old, lines_new))

    return {
        "changes": workspace_changeset,
    }


def apply_rope_changeset(workspace, rope_changeset: rope.ChangeSet) -> None:
    workspace_edit = rope_changeset_to_workspace_edit(
        workspace,
        rope_changeset,
    )

    logger.info("applying workspace edit: %s", workspace_edit)
    workspace.apply_edit(workspace_edit)


class WorkspaceFileCommands(object):
    def __init__(self, workspace):
        self.workspace = workspace
        self.normal_actions = FileSystemCommands()

    def create_file(self, path):
        return self.normal_actions.create_file(path)

    def create_folder(self, path):
        return self.normal_actions.create_folder(path)

    def move(self, path, new_location):
        return self.normal_actions.move(path, new_location)

    def remove(self, path):
        return self.normal_actions.remove(path)

    def write(self, path, data):
        return self.normal_actions.write(path, data)

    def read(self, path):
        document_uri = uris.from_fs_path(path)
        document = self.workspace.get_maybe_document(document_uri)
        if document is None:
            content = self.normal_actions.read(path)
            logger.info('reading from filesystem: "%s":', path)
            return content
        else:
            content = document.source.encode("utf-8")
            logger.info('reading from workspace: "%s":', path)
            return content
