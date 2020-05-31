import click
from flask.cli import with_appcontext
from flask import current_app
from flask_sqlalchemy import SQLAlchemy,SessionBase

db = SQLAlchemy()
Session:SessionBase = db.session

def close_db(e=None):
    db.session.close()

def init_db(app):
    from . import model
    db.drop_all()
    model.init_key_dir(app)
    db.create_all()
    model.init_key()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db(current_app)
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)