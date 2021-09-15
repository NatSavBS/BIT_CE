import sqlite3
from werkzeug.security import generate_password_hash

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialsed the database')

@click.command('add-user')
@click.argument('name')
@click.argument('pwd')
@with_appcontext
def add_user_command(name, pwd):
    print(name, pwd)
    db = get_db()
    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)", (name, generate_password_hash(pwd)),
        )
        db.commit()
    except db.IntegrityError:
        click.echo(f"User {name} is already registered.")
    else:
        click.echo(f"successfully added {name}")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_user_command)
