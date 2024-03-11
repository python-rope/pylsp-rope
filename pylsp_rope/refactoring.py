import ast
from typing import List, Optional

from rope.contrib import generate
from rope.refactor import (
    extract,
    inline,
    method_object,
    usefunction,
    localtofield,
    importutils,
    introduce_parameter,
)

from pylsp_rope import typing, commands
from pylsp_rope.project import (
    WorkspaceEditFormat,
    get_project,
    get_resource,
    get_resources,
    apply_rope_changeset,
    DEFAULT_WORKSPACE_EDIT_FORMAT,
)
from pylsp_rope.typing import DocumentUri, CodeActionKind


class Command:
    name: str
    title: str
    kind: CodeActionKind

    def __init__(self, workspace, **arguments):
        self.workspace = workspace
        self.arguments = arguments
        self.__dict__.update(**arguments)

    def __call__(
        self,
        *,
        workspace_edit_format: List[
            WorkspaceEditFormat
        ] = DEFAULT_WORKSPACE_EDIT_FORMAT,
    ):
        rope_changeset = self.get_changes()
        if rope_changeset is not None:
            apply_rope_changeset(
                self.workspace,
                rope_changeset,
                workspace_edit_format,
            )

    def get_changes(self):
        """
        Calculate the rope changeset to perform this refactoring.
        """

    def validate(self, info) -> None:
        """
        Override this method to raise an exception if this refactoring command
        cannot be performed
        """

    def is_valid(self, info):
        try:
            self.validate(info)
        except Exception:
            return False
        else:
            return True
        return False

    def get_code_action(self, title: str) -> typing.CodeAction:
        return {
            "title": title,
            "kind": self.kind,
            "command": {
                "title": title,
                "command": self.name,
                "arguments": [self.arguments],
            },
        }

    @property  # FIXME: backport cached_property
    def project(self):
        if not hasattr(self, "_project"):
            self._project = get_project(self.workspace)
        return self._project


class CommandRefactorExtractMethod(Command):
    name = commands.COMMAND_REFACTOR_EXTRACT_METHOD
    kind: CodeActionKind = "refactor.extract"

    document_uri: DocumentUri
    range: typing.Range
    similar: bool
    global_: bool

    # FIXME: requires rope.refactor.extract._ExceptionalConditionChecker for proper checking
    # def _is_valid(self, info):
    #     ...

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = extract.ExtractMethod(
            project=self.project,
            resource=resource,
            start_offset=current_document.offset_at_position(self.range["start"]),
            end_offset=current_document.offset_at_position(self.range["end"]),
        )
        rope_changeset = refactoring.get_changes(
            extracted_name="extracted_method",
            similar=self.similar,
            global_=self.global_,
        )
        return rope_changeset

    @classmethod
    def get_code_actions(cls, workspace, document, range):
        return {
            "Extract method including similar statements": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=False,
                similar=True,
            ),
            "Extract method": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=False,
                similar=False,
            ),
            "Extract global method including similar statements": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=True,
                similar=True,
            ),
            "Extract global method": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=True,
                similar=False,
            ),
        }


class CommandRefactorExtractVariable(Command):
    name = commands.COMMAND_REFACTOR_EXTRACT_VARIABLE
    kind: CodeActionKind = "refactor.extract"

    document_uri: DocumentUri
    range: typing.Range
    similar: bool
    global_: bool

    def validate(self, info):
        # FIXME: requires rope.refactor.extract._ExceptionalConditionChecker for proper checking
        ast.parse(info.selected_text, mode="eval")

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = extract.ExtractVariable(
            project=self.project,
            resource=resource,
            start_offset=current_document.offset_at_position(self.range["start"]),
            end_offset=current_document.offset_at_position(self.range["end"]),
        )
        rope_changeset = refactoring.get_changes(
            extracted_name="extracted_variable",
            similar=self.similar,
            global_=self.global_,
        )
        return rope_changeset

    @classmethod
    def get_code_actions(cls, workspace, document, range):
        return {
            "Extract variable including similar statements": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=False,
                similar=True,
            ),
            "Extract variable": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=False,
                similar=False,
            ),
            "Extract global variable including similar statements": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=True,
                similar=True,
            ),
            "Extract global variable": cls(
                workspace,
                document_uri=document.uri,
                range=range,
                global_=True,
                similar=False,
            ),
        }


class CommandRefactorInline(Command):
    name = commands.COMMAND_REFACTOR_INLINE
    kind: CodeActionKind = "refactor.inline"

    document_uri: DocumentUri
    position: typing.Range

    def validate(self, info):
        inline.create_inline(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(info.position),
        )

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = inline.create_inline(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes()
        return rope_changeset


class CommandRefactorUseFunction(Command):
    name = commands.COMMAND_REFACTOR_USE_FUNCTION
    kind: CodeActionKind = "refactor"

    document_uri: DocumentUri
    documents: Optional[List[DocumentUri]] = None
    position: typing.Range

    def validate(self, info):
        usefunction.UseFunction(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(info.position),
        )

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = usefunction.UseFunction(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        resources = (
            get_resources(self.workspace, self.documents)
            if self.documents is not None
            else None
        )
        rope_changeset = refactoring.get_changes(
            resources=resources,
        )
        return rope_changeset


class CommandRefactorMethodToMethodObject(Command):
    name = commands.COMMAND_REFACTOR_METHOD_TO_METHOD_OBJECT
    kind: CodeActionKind = "refactor.rewrite"

    document_uri: DocumentUri
    position: typing.Range

    def validate(self, info):
        method_object.MethodObject(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(self.position),
        )

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = method_object.MethodObject(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes(classname="NewMethodObject")
        return rope_changeset


class CommandRefactorLocalToField(Command):
    name = commands.COMMAND_REFACTOR_LOCAL_TO_FIELD
    kind: CodeActionKind = "refactor.rewrite"

    document_uri: DocumentUri
    position: typing.Range

    def validate(self, info):
        localtofield.LocalToField(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(self.position),
        )

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = localtofield.LocalToField(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes()
        return rope_changeset


class CommandSourceOrganizeImport(Command):
    name = commands.COMMAND_SOURCE_ORGANIZE_IMPORT
    kind: CodeActionKind = "source.organizeImports"

    document_uri: DocumentUri

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        organizer = importutils.ImportOrganizer(
            project=self.project,
        )
        rope_changeset = organizer.organize_imports(
            resource=resource,
        )
        return rope_changeset


class CommandIntroduceParameter(Command):
    name = commands.COMMAND_INTRODUCE_PARAMETER
    kind: CodeActionKind = "refactor"

    document_uri: DocumentUri
    position: typing.Range

    def validate(self, info):
        introduce_parameter.IntroduceParameter(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(self.position),
        )

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = introduce_parameter.IntroduceParameter(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes(
            new_parameter="new_parameter",
        )
        return rope_changeset


class GenerateCode(Command):
    """
    Given an undefined symbol under cursor, generate an empty
    variable/function/class/module/package
    """

    name = commands.COMMAND_GENERATE_CODE
    kind: CodeActionKind = "quickfix"

    document_uri: DocumentUri
    position: typing.Range
    generate_kind: str

    def validate(self, info):
        generate.create_generate(
            kind=self.generate_kind,
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(self.position),
        )

    def get_changes(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = generate.create_generate(
            kind=self.generate_kind,
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes()
        return rope_changeset

    @classmethod
    def get_code_actions(cls, workspace, document, position):
        return {
            f"Generate {generate_kind}": cls(
                workspace,
                document_uri=document.uri,
                position=position,
                generate_kind=generate_kind,
            )
            for generate_kind in ["variable", "function", "class", "module", "package"]
        }
