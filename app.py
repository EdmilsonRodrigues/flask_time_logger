from flask import Flask
from config import DEBUG, DESCRIPTION, TITLE, VERSION
from models.departments import Department
from models.projects import Project
from models.time_logs import TimeLog
from models.users import User
from routes.admin import admin_ns
from routes.auth import auth_ns
from routes.departments import departments_ns
from routes.projects import projects_ns
from routes.time_logs import timelogs_ns
from routes.users import users_ns
from flask_restx import Api
from session import get_db


app = Flask(__name__)

authorizations = {
    "bearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Bearer token authentication",
    }
}

api = Api(
    app,
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    doc="/docs",
    authorizations=authorizations,
    # prefix="/api",
)

api.add_namespace(auth_ns)
api.add_namespace(admin_ns)
api.add_namespace(users_ns)
api.add_namespace(departments_ns)
api.add_namespace(projects_ns)
api.add_namespace(timelogs_ns)


models = (User, TimeLog, Department, Project)


def init_db():
    with get_db() as db:
        for model in models:
            db.execute(model.create_table())
        db.commit()


init_db()


if __name__ == "__main__":
    app.run(debug=DEBUG)
