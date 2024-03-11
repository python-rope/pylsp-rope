from typing import (
    Any,
    Collection,
    List,
)
from unittest.mock import ANY, call

from pylsp.workspace import Workspace, Document

from pylsp_rope.typing import (
    CodeAction,
    DocumentContent,
    DocumentUri,
    WorkspaceEditWithChanges,
    TextEdit,
)
from test.conftest import read_fixture_file


def assert_code_actions_do_not_offer(response: List[CodeAction], command: str) -> None:
    for action in response:
        assert action["command"] is not None
        assert (
            action["command"]["command"] != command
        ), f"CodeAction should not offer {action}"


def assert_text_edits(document_edits: List[TextEdit], target: str) -> DocumentContent:
    new_text = read_fixture_file(target)
    for change in document_edits:
        assert change["newText"] in new_text
    return DocumentContent(new_text)


def assert_single_document_edit(
    edit_request: Any, document: Document
) -> List[TextEdit]:
    workspace_edit = assert_is_apply_edit_request(edit_request)

    document_uri: DocumentUri = document.uri
    assert_modified_documents(
        workspace_edit,
        document_uris={document_uri},
    )

    assert len(workspace_edit["changes"]) == 1
    document_edits = workspace_edit["changes"][document_uri]
    assert isinstance(document_edits, list)
    return document_edits


def assert_is_apply_edit_request(edit_request: Any) -> WorkspaceEditWithChanges:
    assert edit_request == call(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": ANY,
            },
        },
    )

    workspace_edit: WorkspaceEditWithChanges = edit_request[0][1]["edit"]
    for document_uri, document_edits in workspace_edit["changes"].items():
        assert is_document_uri(document_uri)
        for change in document_edits:
            assert change == {
                "range": {
                    "start": {"line": ANY, "character": ANY},
                    "end": {"line": ANY, "character": ANY},
                },
                "newText": ANY,
            }

    return workspace_edit


def is_document_uri(uri: DocumentUri) -> bool:
    return isinstance(uri, str) and uri.startswith("file://")


def assert_modified_documents(
    workspace_edit: WorkspaceEditWithChanges,
    document_uris: Collection[DocumentUri],
) -> None:
    assert workspace_edit["changes"].keys() == set(document_uris)


def assert_unmodified_document(
    workspace_edit: WorkspaceEditWithChanges,
    document_uri: DocumentUri,
) -> None:
    assert is_document_uri(document_uri)
    assert document_uri not in workspace_edit["changes"]


def assert_no_execute_command(workspace: Workspace) -> None:
    workspace._endpoint.request.assert_not_called()
