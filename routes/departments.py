from flask import request
from flask_restx import Namespace, Resource, fields
from models.users import User
from routes.dependencies import validated_dependency
from models.departments import Department, DepartmentRequest


departments_ns = Namespace("departments", description="Department related operations")

model = departments_ns.model(*DepartmentRequest.model())
department_create_model = departments_ns.model(*DepartmentRequest.model())
department_model = departments_ns.model(*Department.model())
department_list_model = departments_ns.model(
    "DepartmentsList", {"departments": fields.List(fields.Nested(department_model))}
)


@departments_ns.route("/")
class ListDepartments(Resource):
    @validated_dependency(
        namespace=departments_ns,
        request_model=department_create_model,
        response_model=department_list_model,
        return_session=True,
    )
    def post(self, session: User):
        request.json["user_ids"] = [session.id]
        department = Department.create(DepartmentRequest(**request.json))
        return department.json(), 201

    @validated_dependency(
        namespace=departments_ns, response_model=department_model, return_session=True
    )
    def get(self, session: User):
        departments = Department.list_all(user_ids=session.id)
        return {"departments": [department.json() for department in departments]}, 200


@departments_ns.route("/<int:id>")
class DepartmentResource(Resource):
    @validated_dependency(
        namespace=departments_ns, response_model=department_model, return_session=True
    )
    def get(self, id: int, session: User):
        department: Department = Department.get(id)
        if session.id not in department.user_ids:
            departments_ns.abort(403, "Unauthorized")
        return department.json(), 200

    @validated_dependency(
        namespace=departments_ns,
        request_model=department_create_model,
        response_model=department_model,
        return_session=True,
    )
    def put(self, id: int, session: User):
        department = Department.get(id).json()
        if session.id not in department["user_ids"]:
            departments_ns.abort(403, "Unauthorized")
        updated_department = DepartmentRequest(**request.json)
        department.update(updated_department)
        department = Department(**department)
        department = department.save()
        return department.json(), 200

    @validated_dependency(namespace=departments_ns, return_session=True)
    def delete(self, id: int, session: User):
        department: Department = Department.get(id)
        if session.id not in department.user_ids:
            departments_ns.abort(403, "Unauthorized")
        department.delete()
        return {"message": "Department deleted"}, 200
