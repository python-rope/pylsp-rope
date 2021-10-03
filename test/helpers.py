from unittest.mock import ANY, call


def assert_code_actions_do_not_offer(response, command):
    for action in response:
        assert action["command"] != command, f"CodeAction should not offer {action}"


def assert_wholefile_changeset(document_changeset, target):
    assert len(document_changeset) == 1
    (change,) = document_changeset
    new_text = open(target, "r").read()
    assert change["newText"].strip() == new_text.strip()
    return new_text


def assert_changeset(document_changeset, target):
    new_text = open(target, "r").read()
    for change in document_changeset:
        assert change["newText"] in new_text
    return new_text


def assert_single_document_edit(edit_request, document):
    assert edit_request == call(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": {
                    document.uri: ANY,
                },
            },
        },
    )

    (document_changeset,) = edit_request[0][1]["edit"]["changes"].values()
    for change in document_changeset:
        assert change == {
            "range": {
                "start": {"line": ANY, "character": ANY},
                "end": {"line": ANY, "character": ANY},
            },
            "newText": ANY,
        }

    return document_changeset
