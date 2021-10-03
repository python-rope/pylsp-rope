import difflib
from pylsp_rope.text import Position


def _difflib_ops_to_text_edit_ops(ops, lines):
    op, start_old, end_old, start_new, end_new = ops

    if op == "replace" or op == "insert":
        new_text = "".join(lines[start_new:end_new])
    elif op == "delete":
        new_text = ""
    else:
        assert False, ops

    return {
        "range": {"start": Position(start_old), "end": Position(end_old)},
        "newText": new_text,
    }


def lsp_diff(lines_old, lines_new):
    """
    Given two sequences of lines, produce a [TextEdit][1] changeset.

    [1]: https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textEdit
    """
    matcher = difflib.SequenceMatcher(a=lines_old, b=lines_new)
    for ops in matcher.get_opcodes():
        if ops[0] == "equal":
            continue

        text_edit_ops = _difflib_ops_to_text_edit_ops(ops, lines_new)
        yield text_edit_ops
