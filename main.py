from flask import Flask
import click
import sqlite3
from flask import g
from flask.cli import with_appcontext
from flask import current_app
from flask import Flask, render_template

app = Flask(__name__)

# Work with SQlite
DATABASE = 'filmash.db'

# Connect to DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close hadler
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'test, World!'