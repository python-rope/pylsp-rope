import ast
from pylsp.lsp import MessageType
import logging

import rope.base.exceptions
from pylsp import hookimpl
from rope.refactor import extract, inline, method_object, usefunction

from pylsp_rope import commands
from pylsp_rope.project import (
    get_project,
    get_resource,
    get_resources,
    apply_rope_changeset,
)


logger = logging.getLogger(__name__)


@hookimpl
def pylsp_settings():
    logger.info("Initializing pylsp_rope")

    # Disable default plugins that conflicts with our plugin
    return {
        "plugins": {
            # "autopep8_format": {"enabled": False},
            # "definition": {"enabled": False},
            # "flake8_lint": {"enabled": False},
            # "folding": {"enabled": False},
            # "highlight": {"enabled": False},
            # "hover": {"enabled": False},
            # "jedi_completion": {"enabled": False},
            # "jedi_rename": {"enabled": False},
            # "mccabe_lint": {"enabled": False},
            # "preload_imports": {"enabled": False},
            # "pycodestyle_lint": {"enabled": False},
            # "pydocstyle_lint": {"enabled": False},
            # "pyflakes_lint": {"enabled": False},
            # "pylint_lint": {"enabled": False},
            # "references": {"enabled": False},
            # "rope_completion": {"enabled": False},
            # "rope_rename": {"enabled": False},
            # "signature": {"enabled": False},
            # "symbols": {"enabled": False},
            # "yapf_format": {"enabled": False},
        },
    }


@hookimpl
def pylsp_commands(config, workspace):
    return [getattr(commands, cmd) for cmd in dir(commands) if not cmd.startswith("_")]


@hookimpl
def pylsp_code_actions(config, workspace, document, range, context):
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)

    class info:
        current_document, resource = get_resource(workspace, document.uri)
        position = range["start"]
        start_offset = current_document.offset_at_position(range["start"])
        end_offset = current_document.offset_at_position(range["end"])
        selected_text = document.source[start_offset:end_offset]

    commands = {
        "Extract method": CommandRefactorExtractMethod(
            workspace,
            document_uri=document.uri,
            range=range,
        ),
        "Extract variable": CommandRefactorExtractVariable(
            workspace,
            document_uri=document.uri,
            range=range,
        ),
        "Inline method/variable/parameter": CommandRefactorInline(
            workspace,
            document_uri=document.uri,
            position=info.position,
        ),
        "Use function": CommandRefactorUseFunction(
            workspace,
            document_uri=document.uri,
            position=info.position,
        ),
        "Use function for current file only": CommandRefactorUseFunction(
            workspace,
            document_uri=document.uri,
            position=info.position,
            documents=[document.uri],
        ),
        "To method object": CommandRefactorMethodToMethodObject(
            workspace,
            document_uri=document.uri,
            position=info.position,
        ),
    }

    return [
        cmd.get_code_action(title=title)
        for title, cmd in commands.items()
        if cmd.is_valid(info)
    ]


@hookimpl
def pylsp_execute_command(config, workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s", command, arguments)

    commands = {cmd.name: cmd for cmd in Command.__subclasses__()}

    try:
        return commands[command](workspace, **arguments[0])()
    except Exception as exc:
        logger.exception(
            "Exception when doing workspace/executeCommand: %s",
            str(exc),
            exc_info=exc,
        )
        workspace.show_message(
            f"pylsp-rope: {exc}",
            msg_type=MessageType.Error,
        )


class Command:
    def __init__(self, workspace, **arguments):
        self.workspace = workspace
        self.arguments = arguments
        self.__dict__.update(**arguments)

    def is_valid(self, info):
        try:
            self.validate(info)
        except Exception:
            return False
        else:
            return True
        return False

    def validate(self, info):
        pass

    def get_code_action(self, title):
        return {
            "title": title,
            "kind": self.kind,
            "command": {
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
    kind = "refactor.extract"

    # FIXME: requires rope.refactor.extract._ExceptionalConditionChecker for proper checking
    # def _is_valid(self, info):
    #     ...

    def __call__(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = extract.ExtractMethod(
            project=self.project,
            resource=resource,
            start_offset=current_document.offset_at_position(self.range["start"]),
            end_offset=current_document.offset_at_position(self.range["end"]),
        )
        rope_changeset = refactoring.get_changes(
            extracted_name="extracted_method",
        )
        apply_rope_changeset(self.workspace, rope_changeset)


class CommandRefactorExtractVariable(Command):
    name = commands.COMMAND_REFACTOR_EXTRACT_VARIABLE
    kind = "refactor.extract"

    def validate(self, info):
        # FIXME: requires rope.refactor.extract._ExceptionalConditionChecker for proper checking
        ast.parse(info.selected_text, mode="eval")

    def __call__(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = extract.ExtractVariable(
            project=self.project,
            resource=resource,
            start_offset=current_document.offset_at_position(self.range["start"]),
            end_offset=current_document.offset_at_position(self.range["end"]),
        )
        rope_changeset = refactoring.get_changes(
            extracted_name="extracted_variable",
        )
        apply_rope_changeset(self.workspace, rope_changeset)


class CommandRefactorInline(Command):
    name = commands.COMMAND_REFACTOR_INLINE
    kind = "refactor.inline"

    def validate(self, info):
        inline.create_inline(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(info.position),
        )

    def __call__(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = inline.create_inline(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes()
        apply_rope_changeset(self.workspace, rope_changeset)


class CommandRefactorUseFunction(Command):
    name = commands.COMMAND_REFACTOR_USE_FUNCTION
    kind = "refactor"

    def validate(self, info):
        usefunction.UseFunction(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(info.position),
        )

    def __call__(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = usefunction.UseFunction(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes(
            resources=get_resources(self.workspace, getattr(self, "documents", None)),
        )
        apply_rope_changeset(self.workspace, rope_changeset)


class CommandRefactorMethodToMethodObject(Command):
    name = commands.COMMAND_REFACTOR_METHOD_TO_METHOD_OBJECT
    kind = "refactor.rewrite"

    def validate(self, info):
        method_object.MethodObject(
            project=self.project,
            resource=info.resource,
            offset=info.current_document.offset_at_position(self.position),
        )

    def __call__(self):
        current_document, resource = get_resource(self.workspace, self.document_uri)

        refactoring = method_object.MethodObject(
            project=self.project,
            resource=resource,
            offset=current_document.offset_at_position(self.position),
        )
        rope_changeset = refactoring.get_changes(classname="NewMethodObject")
        apply_rope_changeset(self.workspace, rope_changeset)
