from flask import request
from flask_restx import Namespace, Resource, fields
from models.users import User
from routes.dependencies import validated_dependency
from models.time_logs import TimeLog, TimeLogRequest


timelogs_ns = Namespace("timelogs", description="TimeLog related operations")


timelog_create_model = timelogs_ns.model(*TimeLogRequest.model())
timelog_model = timelogs_ns.model(*TimeLog.model())
timelog_list_model = timelogs_ns.model(
    "TimeLogsList", {"results": fields.List(fields.Nested(timelog_model))}
)
timelog_action_model = timelogs_ns.model(
    "TimeLogAction",
    {
        "action": fields.String(description="Action to perform. E.g. start, stop"),
        "project_id": fields.Integer(description="Project ID", required=False),
    },
)


@timelogs_ns.route("/")
class ListTimeLogs(Resource):
    @validated_dependency(
        namespace=timelogs_ns,
        request_model=timelog_create_model,
        response_model=timelog_model,
        return_session=True,
    )
    def post(self, session: User):
        request.json["user_id"] = session.id
        timelog = TimeLog.create(TimeLogRequest(**request.json))
        return timelog.json(), 201

    @validated_dependency(
        namespace=timelogs_ns, response_model=timelog_list_model, return_session=True
    )
    def get(self, session: User):
        timelogs = TimeLog.list_all(user_id=session.id)
        return {"results": [timelog.json() for timelog in timelogs]}, 200


@timelogs_ns.route("/actions")
class TimeLogActions(Resource):
    @validated_dependency(
        namespace=timelogs_ns, return_session=True, request_model=timelog_action_model
    )
    def post(self, session: User):
        action = request.json["action"]
        match action:
            case "start":
                project_id = request.json.get("project_id")
                TimeLog.start(session.id, project_id)
            case "stop":
                TimeLog.stop(session.id)
            case _:
                timelogs_ns.abort(400, "Invalid action")
        return {"message": f"Action {action} performed"}, 200


@timelogs_ns.route("/<int:id>")
class TimeLogResource(Resource):
    @validated_dependency(
        namespace=timelogs_ns, response_model=timelog_model, return_session=True
    )
    def get(self, id: int, session: User):
        timelog: TimeLog = TimeLog.get(id)
        if timelog.user_id != session.id:
            timelogs_ns.abort(403, "Unauthorized")
        return timelog.json(), 200

    @validated_dependency(
        namespace=timelogs_ns,
        request_model=timelog_create_model,
        response_model=timelog_model,
        return_session=True,
    )
    def put(self, id, session: User):
        timelog = TimeLog.get(id).json()
        if timelog["user_id"] != session.id:
            timelogs_ns.abort(403, "Unauthorized")
        updated_timelog = TimeLogRequest(**request.json)
        timelog.update(updated_timelog)
        timelog = TimeLog(**timelog)
        timelog = timelog.save()
        return timelog.json(), 200

    @validated_dependency(namespace=timelogs_ns, return_session=True)
    def delete(self, id: int, session: User):
        timelog: TimeLog = TimeLog.get(id)
        if timelog.user_id != session.id:
            timelogs_ns.abort(403, "Unauthorized")
        timelog.delete()
        return {"message": "TimeLog deleted"}, 200
