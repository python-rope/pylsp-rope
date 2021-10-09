import difflib
from typing import Iterator, List, Tuple, cast

from pylsp_rope.text import Position
from pylsp_rope.typing import TextEdit, Line, LineNumber


_DifflibOpcode = Tuple[str, LineNumber, LineNumber, LineNumber, LineNumber]


def _difflib_ops_to_text_edit_ops(
    opcode: _DifflibOpcode, lines: List[Line]
) -> TextEdit:
    op, start_old, end_old, start_new, end_new = opcode

    if op == "replace" or op == "insert":
        new_text = "".join(lines[start_new:end_new])
    elif op == "delete":
        new_text = ""
    else:
        assert False, opcode

    return {
        "range": {"start": Position(start_old), "end": Position(end_old)},
        "newText": new_text,
    }


def lsp_diff(lines_old: List[Line], lines_new: List[Line]) -> Iterator[TextEdit]:
    """
    Given two sequences of lines, produce a [TextEdit][1] changeset.

    [1]: https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textEdit
    """
    matcher = difflib.SequenceMatcher(a=lines_old, b=lines_new)
    for opcode in matcher.get_opcodes():
        if opcode[0] == "equal":
            continue

        text_edit_ops = _difflib_ops_to_text_edit_ops(
            cast(_DifflibOpcode, opcode), lines_new
        )
        yield text_edit_ops
