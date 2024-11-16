from flask import request
from flask_restx import Namespace, Resource, fields
from models.users import User
from routes.dependencies import validated_dependency
from models.projects import Project, ProjectRequest


projects_ns = Namespace("projects", description="Project related operations")


project_create_model = projects_ns.model(*ProjectRequest.model())
project_model = projects_ns.model(*Project.model())
project_list_model = projects_ns.model(
    "ProjectsList", {"projects": fields.List(fields.Nested(project_model))}
)


@projects_ns.route("/")
class ListProjects(Resource):
    @validated_dependency(
        namespace=projects_ns,
        request_model=project_create_model,
        response_model=project_model,
        return_session=True,
    )
    def post(self, session: User):
        request.json["user_ids"] = [session.id]
        project = Project.create(ProjectRequest(**request.json))
        return project.json(), 201

    @validated_dependency(
        namespace=projects_ns, response_model=project_list_model, return_session=True
    )
    def get(self, session: User):
        projects: list[Project] = Project.list_all(user_ids=session.id)
        return {"results": [project.json() for project in projects]}, 200


@projects_ns.route("/<int:id>")
class ProjectResource(Resource):
    @validated_dependency(
        namespace=projects_ns, response_model=project_model, return_session=True
    )
    def get(self, id: int, session: User):
        project: Project = Project.get(id)
        if session.id not in project.user_ids:
            projects_ns.abort(403, "Unauthorized")
        return project.json(), 200

    @validated_dependency(
        namespace=projects_ns,
        request_model=project_create_model,
        response_model=project_model,
        return_session=True,
    )
    def put(self, id: int, session: User):
        project = Project.get(id).json()
        if session.id not in project["user_ids"]:
            projects_ns.abort(403, "Unauthorized")
        updated_project = ProjectRequest(**request.json)
        project.update(updated_project)
        project = Project(**project)
        project = project.save()
        return project.json(), 200

    @validated_dependency(namespace=projects_ns, return_session=True)
    def delete(self, id: int, session: User):
        project: Project = Project.get(id)
        if session.id not in project.user_ids:
            projects_ns.abort(403, "Unauthorized")
        project.delete()
        return {"message": "Project deleted"}, 200
