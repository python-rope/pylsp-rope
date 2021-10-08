from unittest.mock import ANY, call

from test.conftest import read_fixture_file


def assert_code_actions_do_not_offer(response, command):
    for action in response:
        assert action["command"] != command, f"CodeAction should not offer {action}"


def assert_changeset(document_changeset, target):
    new_text = read_fixture_file(target)
    for change in document_changeset:
        assert change["newText"] in new_text
    return new_text


def assert_single_document_edit(edit_request, document):
    workspace_changeset = assert_is_apply_edit_request(edit_request)

    assert_modified_documents(
        workspace_changeset,
        document_uris={document.uri},
    )

    assert len(workspace_changeset) == 1
    (document_changeset,) = workspace_changeset.values()
    return document_changeset


def assert_is_apply_edit_request(edit_request):
    assert edit_request == call(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": ANY,
            },
        },
    )

    workspace_changeset = edit_request[0][1]["edit"]["changes"]
    for document_uri, document_changeset in workspace_changeset.items():
        assert is_document_uri(document_uri)
        for change in document_changeset:
            assert change == {
                "range": {
                    "start": {"line": ANY, "character": ANY},
                    "end": {"line": ANY, "character": ANY},
                },
                "newText": ANY,
            }

    return workspace_changeset


def is_document_uri(uri):
    return isinstance(uri, str) and uri.startswith("file://")


def assert_modified_documents(workspace_changeset, document_uris):
    assert workspace_changeset.keys() == set(document_uris)


def assert_unmodified_document(workspace_changeset, document_uri):
    assert is_document_uri(document_uri)
    assert document_uri not in workspace_changeset
