from flask import request
from flask_restx import Namespace, Resource, fields
from dependencies import validated_dependency
from models.projects import Project, ProjectRequest


projects_ns = Namespace("projects", description="Project related operations")


project_create_model = projects_ns.model(ProjectRequest.model())
project_model = projects_ns.model(Project.model())
project_list_model = projects_ns.model(
    "ProjectsList", {"projects": fields.List(fields.Nested(project_model))}
)


@projects_ns.route("/")
class ListProjects(Resource):
    @validated_dependency(
        namespace=projects_ns,
        request_model=project_create_model,
        response_model=project_model,
    )
    def post(self):
        project = Project.create(ProjectRequest(**request.json))
        return project.json(), 201

    @validated_dependency(namespace=projects_ns, response_model=project_model)
    def get(self):
        projects = Project.list_all()
        return {"projects": [project.json() for project in projects]}, 200


@projects_ns.route("/<int:id>")
class ProjectResource(Resource):
    @validated_dependency(namespace=projects_ns, response_model=project_model)
    def get(self, id):
        project = Project.get(id)
        return project.json(), 200

    @validated_dependency(
        namespace=projects_ns,
        request_model=project_create_model,
        response_model=project_model,
    )
    def put(self, id):
        project = Project.get(id).json()
        updated_project = ProjectRequest(**request.json)
        project.update(updated_project)
        project = Project(**project)
        project = project.save()
        return project.json(), 200

    @validated_dependency(namespace=projects_ns)
    def delete(self, id):
        project = Project.get(id)
        project.delete()
        return {"message": "Project deleted"}, 200
