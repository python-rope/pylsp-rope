from typing import List, Dict, Optional, NewType
from typing_extensions import TypedDict


# LSP types
DocumentUri = NewType("DocumentUri", str)


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


class ApplyWorkspaceEditParams(TypedDict):
    label: Optional[str]
    edit: WorkspaceEdit


# pylsp-rope types
DocumentContent = NewType("DocumentContent", str)


class SimpleWorkspaceEdit(TypedDict):
    """ This is identical to WorkspaceEdit, but `changes` field is not optional. """
    changes: Dict[DocumentUri, List[TextEdit]]
