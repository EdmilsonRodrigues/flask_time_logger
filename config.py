from dotenv import load_dotenv
import os


if os.path.exists(".env"):
    load_dotenv(".env")


VERSION = "1.0.0"
DESCRIPTION = "An API for tracking time logs of home work projects"
TITLE = "Time Tracker API"

DEBUG = os.getenv("DEBUG", "True").capitalize() == "True"
DB = os.getenv("DB", "db.sqlite3")
BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:5000")
SECRET_KEY = os.getenv("SECRET_KEY", "This is my secre key")

if __name__ == "__main__":
    print(DEBUG)
    print(BASE_API_URL)
    print(SECRET_KEY)
