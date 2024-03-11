import sys
from typing import List, Dict, Optional, NewType, Any, Union
try:
    from typing import TypeGuard
except ImportError:
    from typing_extensions import TypeGuard


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


class TextDocumentIdentifier(TypedDict):
    uri: DocumentUri


class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: Optional[int]


class TextEdit(TypedDict):
    range: Range
    newText: str


class TextDocumentEdit(TypedDict):
    textDocument: OptionalVersionedTextDocumentIdentifier

    edits: List[TextEdit]  # FIXME: should be: list[TextEdit| AnnotatedTextEdit]


class WorkspaceEditWithChanges(TypedDict):
    changes: Dict[DocumentUri, List[TextEdit]]
    # documentChanges: Optional[list[TextDocumentEdit]]  # FIXME: should be: (TextDocumentEdit | CreateFile | RenameFile | DeleteFile)[]
    # changeAnnotations: ...


class WorkspaceEditWithDocumentChanges(TypedDict):
    # changes: Optional[Dict[DocumentUri, List[TextEdit]]]
    documentChanges: List[
        TextDocumentEdit
    ]  # FIXME: should be: (TextDocumentEdit | CreateFile | RenameFile | DeleteFile)[]
    # changeAnnotations: ...


WorkspaceEdit = Union[WorkspaceEditWithChanges, WorkspaceEditWithDocumentChanges]


def is_workspace_edit_with_changes(
    workspace_edit: WorkspaceEdit,
) -> TypeGuard[WorkspaceEditWithChanges]:
    return "changes" in workspace_edit


def is_workspace_edit_with_document_changes(
    workspace_edit: WorkspaceEdit,
) -> TypeGuard[WorkspaceEditWithDocumentChanges]:
    return "documentChanges" in workspace_edit


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
