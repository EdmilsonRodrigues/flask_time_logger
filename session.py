import sqlite3

from services.database import Database


def get_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn


db = Database(get_db)
