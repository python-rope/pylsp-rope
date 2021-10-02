from rope.base.project import Project
from rope.base import libutils
from functools import cache


@cache
def get_project(workspace):
    project = Project(workspace.root_path)
    project.validate()
    return project


def get_resource(workspace, document_uri):
    document = workspace.get_document(document_uri)
    resource = libutils.path_to_resource(get_project(workspace), document.path)
    return document, resource
