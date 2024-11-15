from importlib import import_module
from multiprocessing.resource_tracker import getfd
import sqlite3


def get_db():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn
