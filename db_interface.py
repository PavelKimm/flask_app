import sqlite3
from flask import current_app, g

DATABASE = 'films.db'


# def init_db():
#     db = get_db()
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def write_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    cur.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
