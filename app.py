#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List, Tuple

import click
from flask import g, request, redirect, url_for
from flask.cli import with_appcontext
from flask import Flask, render_template

from films_repository import get_films_to_compare, save_comparison, get_rating

app = Flask(__name__)


# @app.cli.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


# Close handler
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def vs():
    films = get_films_to_compare()
    return render_template('vs.html', films=films)


@app.route('/rating')
def rating():
    films = get_rating()
    return render_template('rating.html', enumerated_films=enumerate(films))


@app.route('/compare-films', methods=['POST'])
def add_comparison():
    win_id = int(request.form.get('win'))
    lose_id = int(request.form.get('lose'))
    print(request.form)
    save_comparison(win_id, lose_id)
    return redirect(url_for('vs'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
