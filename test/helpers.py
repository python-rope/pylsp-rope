from typing import (
    Collection,
    Dict,
    List,
)
from unittest.mock import ANY, call

from pylsp_rope.typing import (
    DocumentUri,
    TextEdit,
    WorkspaceEdit,
)
from test.conftest import read_fixture_file


def assert_code_actions_do_not_offer(response, command):
    for action in response:
        assert action["command"] != command, f"CodeAction should not offer {action}"


def assert_text_edits(document_edits: List[TextEdit], target: str):
    new_text = read_fixture_file(target)
    for change in document_edits:
        assert change["newText"] in new_text
    return new_text


def assert_single_document_edit(edit_request, document) -> List[TextEdit]:
    workspace_edit = assert_is_apply_edit_request(edit_request)

    assert_modified_documents(
        workspace_edit,
        document_uris={document.uri},
    )

    assert len(workspace_edit["changes"]) == 1
    document_edits = next(iter(workspace_edit["changes"].values()))
    return document_edits


def assert_is_apply_edit_request(edit_request: Dict) -> WorkspaceEdit:
    assert edit_request == call(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": ANY,
            },
        },
    )

    workspace_edit = edit_request[0][1]["edit"]
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
    workspace_edit: WorkspaceEdit,
    document_uris: Collection[DocumentUri],
):
    assert workspace_edit["changes"].keys() == set(document_uris)


def assert_unmodified_document(
    workspace_edit: WorkspaceEdit,
    document_uri: DocumentUri,
):
    assert is_document_uri(document_uri)
    assert document_uri not in workspace_edit["changes"]
