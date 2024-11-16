from flask import request
from flask_restx import Namespace, Resource, fields
from routes.dependencies import validated_dependency
from models.time_logs import TimeLog, TimeLogRequest


timelogs_ns = Namespace("timelogs", description="TimeLog related operations")


timelog_create_model = timelogs_ns.model(*TimeLogRequest.model())
timelog_model = timelogs_ns.model(*TimeLog.model())
timelog_list_model = timelogs_ns.model(
    "TimeLogsList", {"timelogs": fields.List(fields.Nested(timelog_model))}
)


@timelogs_ns.route("/")
class ListTimeLogs(Resource):
    @validated_dependency(
        namespace=timelogs_ns,
        request_model=timelog_create_model,
        response_model=timelog_model,
    )
    def post(self):
        timelog = TimeLog.create(TimeLogRequest(**request.json))
        return timelog.json(), 201

    @validated_dependency(namespace=timelogs_ns, response_model=timelog_model)
    def get(self):
        timelogs = TimeLog.list_all()
        return {"timelogs": [timelog.json() for timelog in timelogs]}, 200


@timelogs_ns.route("/<int:id>")
class TimeLogResource(Resource):
    @validated_dependency(namespace=timelogs_ns, response_model=timelog_model)
    def get(self, id):
        timelog = TimeLog.get(id)
        return timelog.json(), 200

    @validated_dependency(
        namespace=timelogs_ns,
        request_model=timelog_create_model,
        response_model=timelog_model,
    )
    def put(self, id):
        timelog = TimeLog.get(id).json()
        updated_timelog = TimeLogRequest(**request.json)
        timelog.update(updated_timelog)
        timelog = TimeLog(**timelog)
        timelog = timelog.save()
        return timelog.json(), 200

    @validated_dependency(namespace=timelogs_ns)
    def delete(self, id):
        timelog = TimeLog.get(id)
        timelog.delete()
        return {"message": "TimeLog deleted"}, 200
