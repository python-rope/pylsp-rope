from typing import Tuple, Union, overload, Optional

from pylsp_rope import typing
from pylsp_rope.typing import LineNumber, CharNumber, Literal


START_OF_LINE: Literal["^"] = "^"
END_OF_LINE: Literal["$"] = "$"


AutoLineNumber = Union[LineNumber, int]
AutoCharNumber = Union[CharNumber, int]


_CharNumberOrMarker = Union[AutoCharNumber, Literal["^", "$"]]
_PrimitiveLineCharNumber = Union[
    AutoLineNumber, Tuple[AutoLineNumber, Optional[_CharNumberOrMarker]]
]


@overload
def Position(
    line: Tuple[AutoLineNumber, Optional[_CharNumberOrMarker]],
    *,
    _default_character: _CharNumberOrMarker = CharNumber(0),
) -> typing.Position: ...


@overload
def Position(
    line: AutoLineNumber,
    *,
    _default_character: _CharNumberOrMarker = CharNumber(0),
) -> typing.Position: ...


@overload
def Position(
    line: AutoLineNumber,
    character: AutoCharNumber,
) -> typing.Position: ...


@overload
def Position(
    line: AutoLineNumber,
    character: Literal["^", "$"],
) -> typing.Position: ...


def Position(
    line: _PrimitiveLineCharNumber,
    character: Optional[_CharNumberOrMarker] = None,
    *,
    _default_character: _CharNumberOrMarker = CharNumber(0),
) -> typing.Position:
    """
    Returns a [Position](https://microsoft.github.io/language-server-protocol/specification#position)
    object for a document.

    `pos` can be:

    - Tuple[LineNumber, CharNumber] are passed directly to the object
    - int selects the start of the line
    - "^" the first non-blank character of the line
    - "$" the end of the line, which is the start of the next line

    Selects the start of line 4

        >>> a = Position(4)
        >>> b = Position(4, 0)
        >>> c = Position((4, 0))
        >>> assert a == b == c

    Selects the end of line 4:

        >>> c = Position(4, "$")
        >>> d = Position(5, 0)
        >>> assert c == d

    """
    if isinstance(line, tuple):
        # assert (
        #     character is None
        # ), "If `line` is a tuple, then `character` must not be supplied"
        lineno, character = line
    else:
        lineno = line

    if character is None:
        character = _default_character

    if character == "$":
        lineno = LineNumber(lineno + 1)
        character = CharNumber(0)
    assert character != "^", "not implemented yet"

    return {
        "line": lineno,
        "character": character,
    }


def Range(
    start: _PrimitiveLineCharNumber,
    end: Optional[_PrimitiveLineCharNumber] = None,
) -> typing.Range:
    """
    Returns a [Range](https://microsoft.github.io/language-server-protocol/specification#range)
    object for a document.

    `start` and `end` accepts the same arguments as Position object.

    If `start` or `end` is an int, then the whole line is selected.

    Selects the whole line 4, including the line ending

        >>> a = Range(4)
        >>> b = Range(4, 4)
        >>> c = Range((4, 0), (5, 0))
        >>> assert a == b == c

    Selects line 4-6

        >>> d = Range(4, 6)
        >>> e = Range((4, 0), (7, 0))
        >>> assert d == e

    """

    if end is None:
        end = start

    return {
        "start": Position(start, _default_character=CharNumber(0)),
        "end": Position(end, _default_character=END_OF_LINE),
    }
