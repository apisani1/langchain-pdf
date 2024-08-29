import click
import os
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()


@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]
        click.echo(f"Initializing db with uri: {db_uri}")

        # Handle SQLite
        if db_uri.startswith("sqlite:"):
            try:
                os.makedirs(current_app.instance_path, exist_ok=True)
            except OSError:
                pass

            # For SQLite, we don't need to create the database, just the tables
            db.drop_all()
            db.create_all()

        # Handle PostgreSQL
        elif db_uri.startswith("postgresql:"):
            engine = create_engine(db_uri)
            if not database_exists(engine.url):
                create_database(engine.url)

            # Connect to the database and create tables
            db.drop_all()
            db.create_all()

        else:
            click.echo(f"Unsupported database type: {db_uri}")
            return

    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
