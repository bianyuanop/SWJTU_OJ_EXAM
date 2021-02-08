import click
from . import db

@click.command("init-db")
def init_db_command():
    '''Clear existing data and create new tables.'''
    db.init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
