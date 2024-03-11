import sys
from typing import List, Dict, Optional, NewType, Any


if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal
else:
    from typing_extensions import TypedDict, Literal


##########################
### Standard LSP types ###
##########################

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


class Command(TypedDict):
    title: str
    command: str
    arguments: Optional[List[Any]]


CodeActionKind = Literal[
    "",
    "quickfix",
    "refactor",
    "refactor.extract",
    "refactor.inline",
    "refactor.rewrite",
    "source",
    "source.organizeImports",
    "source.fixAll",
]


class CodeAction(TypedDict):
    title: str
    kind: Optional[CodeActionKind]
    # diagnostics: Optional[List[Diagnostic]]
    # isPreferred: Optional[bool]
    # disabled: Optional[_CodeActionDisabledReason]
    # edit: Optional[WorkspaceEdit]
    command: Optional[Command]
    # data: Optional[Any]


########################
### pylsp-rope types ###
########################

DocumentContent = NewType("DocumentContent", str)
Line = NewType("Line", str)
LineNumber = NewType("LineNumber", int)
CharNumber = NewType("CharNumber", int)


class SimpleWorkspaceEdit(TypedDict):
    """This is identical to WorkspaceEdit, but `changes` field is not optional."""

    changes: Dict[DocumentUri, List[TextEdit]]
