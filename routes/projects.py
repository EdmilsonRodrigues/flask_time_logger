from flask import request
from flask_restx import Namespace, Resource, fields


test_ns = Namespace("test-api", description="Test API")


test_create_model = test_ns.model(
    "TestCreate",
    {
        "key": fields.String(required=True, description="A key", example="key"),
        "value": fields.String(required=True, description="A value", example="value"),
    },
)

test_model = test_ns.model(
    "Test",
    {
        "key": fields.String(readOnlu=True, description="A key", example="key"),
        "value": fields.String(readOnlu=True, description="A value", example="value"),
    },
)


@test_ns.route("/")
class TestAPI(Resource):
    @test_ns.expect(test_create_model)
    @test_ns.marshal_with(test_model)
    def post(self):
        data = request.get_json()
        return data
