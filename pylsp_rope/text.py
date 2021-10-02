def Position(line, character=None, _default_character=0):
    """
    Returns a [Position](https://microsoft.github.io/language-server-protocol/specification#position)
    object for a document.

    `pos` can be:

    - Tuple[line, character] are passed directly to the object
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
        assert (
            character is None
        ), "If `line` is a tuple, then `character` must not be supplied"
        line, character = line

    if character is None:
        character = _default_character

    if character == "$":
        line += 1
        character = 0

    return {
        "line": line,
        "character": character,
    }


def Range(start, end=None):
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
        "start": Position(start, _default_character=0),
        "end": Position(end, _default_character="$"),
    }
