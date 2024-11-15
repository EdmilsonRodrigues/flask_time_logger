from flask import Flask
from config import DEBUG
from routes.test import test_ns
from flask_restx import Api


app = Flask(__name__)
api = Api(
    app, title="Test API", description="A simple test API", version="1.0", doc="/doc"
)

api.add_namespace(test_ns)

if __name__ == "__main__":
    app.run(debug=DEBUG)
