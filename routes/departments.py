from flask import request
from flask_restx import Namespace, Resource, fields
from dependencies import validated_dependency
from models.departments import Department, DepartmentRequest


departments_ns = Namespace("departments", description="Department related operations")


department_create_model = departments_ns.model(DepartmentRequest.model())
department_model = departments_ns.model(Department.model())
department_list_model = departments_ns.model(
    "DepartmentsList", {"departments": fields.List(fields.Nested(department_model))}
)


@departments_ns.route("/")
class ListDepartments(Resource):
    @validated_dependency(
        namespace=departments_ns,
        request_model=department_create_model,
        response_model=department_model,
    )
    def post(self):
        department = Department.create(DepartmentRequest(**request.json))
        return department.json(), 201

    @validated_dependency(namespace=departments_ns, response_model=department_model)
    def get(self):
        departments = Department.list_all()
        return {"departments": [department.json() for department in departments]}, 200


@departments_ns.route("/<int:id>")
class DepartmentResource(Resource):
    @validated_dependency(namespace=departments_ns, response_model=department_model)
    def get(self, id):
        department = Department.get(id)
        return department.json(), 200

    @validated_dependency(
        namespace=departments_ns,
        request_model=department_create_model,
        response_model=department_model,
    )
    def put(self, id):
        department = Department.get(id).json()
        updated_department = DepartmentRequest(**request.json)
        department.update(updated_department)
        department = Department(**department)
        department = department.save()
        return department.json(), 200

    @validated_dependency(namespace=departments_ns)
    def delete(self, id):
        department = Department.get(id)
        department.delete()
        return {"message": "Department deleted"}, 200
