from flask import Flask
from config import DEBUG
from models.departments import Department
from models.projects import Project
from models.time_logs import TimeLog
from models.users import User
from routes.test import test_ns
from flask_restx import Api
from session import get_db


app = Flask(__name__)
api = Api(
    app, title="Test API", description="A simple test API", version="1.0", doc="/doc"
)

api.add_namespace(test_ns)

models = (User, TimeLog, Department, Project)


def init_db():
    with get_db() as db:
        for model in models:
            db.execute(model.create_table())
        db.commit()


init_db()


if __name__ == "__main__":
    app.run(debug=DEBUG)
