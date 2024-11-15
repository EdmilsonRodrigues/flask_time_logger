from dotenv import load_dotenv
import os


if os.path.exists(".env"):
    load_dotenv(".env")


DEBUG = os.getenv("DEBUG", "True").capitalize() == "True"
BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:5000")
