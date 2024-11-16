from flask import request
from flask_restx import Namespace, Resource
from models.departments import Department, DepartmentRequest
from models.projects import Project, ProjectRequest
from models.time_logs import TimeLog, TimeLogRequest
from routes.dependencies import validated_dependency
from models.users import User, UserRequest
from routes.users import user_create_model, user_list_model, user_model
from routes.time_logs import timelog_create_model, timelog_list_model, timelog_model
from routes.projects import project_create_model, project_model, project_list_model
from routes.departments import (
    department_create_model,
    department_model,
    department_list_model,
)

admin_ns = Namespace("admin", description="Admin only operations")


@admin_ns.route("/users")
class ListUsers(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=user_list_model, requires_admin=True
    )
    def get(self):
        users = User.list_all()
        return {"results": [user.json() for user in users]}, 200


@admin_ns.route("/users/<int:id>")
class UserResource(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=user_model, requires_admin=True
    )
    def get(self, id):
        user = User.get(id)
        return user.json(), 200

    @validated_dependency(
        namespace=admin_ns,
        request_model=user_create_model,
        response_model=user_model,
        requires_admin=True,
    )
    def put(self, id):
        user = User.get(id).json()
        updated_user = UserRequest(**request.json).model_dump()
        user.update(updated_user)
        user = User(**user)
        user = user.save()
        return user.json(), 200

    @validated_dependency(namespace=admin_ns, requires_admin=True)
    def delete(self, id):
        user = User.get(id)
        user.delete()
        return {"message": "User deleted"}, 200


@admin_ns.route("/timelogs")
class ListTimeLogs(Resource):
    @validated_dependency(
        namespace=admin_ns,
        request_model=timelog_create_model,
        response_model=timelog_model,
        requires_admin=True,
    )
    def post(self):
        timelog = TimeLog.create(TimeLogRequest(**request.json))
        return timelog.json(), 201

    @validated_dependency(
        namespace=admin_ns, response_model=timelog_list_model, requires_admin=True
    )
    def get(self):
        timelogs = TimeLog.list_all()
        return {"results": [timelog.json() for timelog in timelogs]}, 200


@admin_ns.route("/timelogs/<int:id>")
class TimeLogResource(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=timelog_model, requires_admin=True
    )
    def get(self, id):
        timelog = TimeLog.get(id)
        return timelog.json(), 200

    @validated_dependency(
        namespace=admin_ns,
        request_model=timelog_create_model,
        response_model=timelog_model,
        requires_admin=True,
    )
    def put(self, id):
        timelog = TimeLog.get(id).json()
        updated_timelog = TimeLogRequest(**request.json)
        timelog.update(updated_timelog)
        timelog = TimeLog(**timelog)
        timelog = timelog.save()
        return timelog.json(), 200

    @validated_dependency(namespace=admin_ns, requires_admin=True)
    def delete(self, id):
        timelog = TimeLog.get(id)
        timelog.delete()
        return {"message": "TimeLog deleted"}, 200


@admin_ns.route("/")
class ListProjects(Resource):
    @validated_dependency(
        namespace=admin_ns,
        request_model=project_create_model,
        response_model=project_list_model,
        requires_admin=True,
    )
    def post(self):
        project = Project.create(ProjectRequest(**request.json))
        return project.json(), 201

    @validated_dependency(
        namespace=admin_ns, response_model=project_model, requires_admin=True
    )
    def get(self):
        projects = Project.list_all()
        return {"projects": [project.json() for project in projects]}, 200


@admin_ns.route("/<int:id>")
class ProjectResource(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=project_model, requires_admin=True
    )
    def get(self, id):
        project = Project.get(id)
        return project.json(), 200

    @validated_dependency(
        namespace=admin_ns,
        request_model=project_create_model,
        response_model=project_model,
        requires_admin=True,
    )
    def put(self, id):
        project = Project.get(id).json()
        updated_project = ProjectRequest(**request.json)
        project.update(updated_project)
        project = Project(**project)
        project = project.save()
        return project.json(), 200

    @validated_dependency(namespace=admin_ns, requires_admin=True)
    def delete(self, id):
        project = Project.get(id)
        project.delete()
        return {"message": "Project deleted"}, 200


@admin_ns.route("/")
class ListDepartments(Resource):
    @validated_dependency(
        namespace=admin_ns,
        request_model=department_create_model,
        response_model=department_list_model,
        requires_admin=True,
    )
    def post(self):
        department = Department.create(DepartmentRequest(**request.json))
        return department.json(), 201

    @validated_dependency(
        namespace=admin_ns, response_model=department_model, requires_admin=True
    )
    def get(self):
        departments = Department.list_all()
        return {"departments": [department.json() for department in departments]}, 200


@admin_ns.route("/<int:id>")
class DepartmentResource(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=department_model, requires_admin=True
    )
    def get(self, id):
        department = Department.get(id)
        return department.json(), 200

    @validated_dependency(
        namespace=admin_ns,
        request_model=department_create_model,
        response_model=department_model,
        requires_admin=True,
    )
    def put(self, id):
        department = Department.get(id).json()
        updated_department = DepartmentRequest(**request.json)
        department.update(updated_department)
        department = Department(**department)
        department = department.save()
        return department.json(), 200

    @validated_dependency(namespace=admin_ns, requires_admin=True)
    def delete(self, id):
        department = Department.get(id)
        department.delete()
        return {"message": "Department deleted"}, 200
