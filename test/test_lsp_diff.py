from pylsp_rope.lsp_diff import _difflib_ops_to_text_edit_ops, lsp_diff
from test.conftest import create_document


def test_lsp_diff(workspace):
    expected = [
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

    old_document = create_document(workspace, "many_changes.py")
    new_document = create_document(workspace, "many_changes_inlined.py")

    changes = list(lsp_diff(old_document.lines, new_document.lines))
    assert changes == expected


def test_difflib_ops_to_text_edit_ops_insert(workspace):
    expected = {
        "range": {
            "start": {"line": 5, "character": 0},
            "end": {"line": 5, "character": 0},
        },
        "newText": 'are = "here"\nred = "here"\n',
    }

    new_document = create_document(workspace, "many_changes_inlined.py")

    difflib_ops = ("insert", 5, 5, 6, 8)
    text_edit_ops = _difflib_ops_to_text_edit_ops(difflib_ops, new_document.lines)

    assert text_edit_ops == expected


def test_difflib_ops_to_text_edit_ops_delete(workspace):
    expected = {
        "range": {
            "start": {"line": 2, "character": 0},
            "end": {"line": 3, "character": 0},
        },
        "newText": "",
    }

    new_document = create_document(workspace, "many_changes_inlined.py")

    difflib_ops = ("delete", 2, 3, 2, 2)
    text_edit_ops = _difflib_ops_to_text_edit_ops(difflib_ops, new_document.lines)

    assert text_edit_ops == expected


def test_difflib_ops_to_text_edit_ops_replace(workspace):
    expected = {
        "range": {
            "start": {"line": 4, "character": 0},
            "end": {"line": 5, "character": 0},
        },
        "newText": 'print("world")\n',
    }

    new_document = create_document(workspace, "many_changes_inlined.py")

    difflib_ops = ("replace", 4, 5, 3, 4)
    text_edit_ops = _difflib_ops_to_text_edit_ops(difflib_ops, new_document.lines)

    assert text_edit_ops == expected
