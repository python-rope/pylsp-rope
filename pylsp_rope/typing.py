from typing import TypedDict, List, Dict, Optional, NewType


DocumentUri = NewType('DocumentUri', str)


class Position(TypedDict):
    line: int
    character: int


class Range(TypedDict):
    start: Position
    end: Position


class TextEdit(TypedDict):
    range: Range
    newText: str


class WorkspaceEdit(TypedDict):
    changes: Optional[Dict[DocumentUri, List[TextEdit]]]
    # documentChanges: ...
    # changeAnnotations: ...
