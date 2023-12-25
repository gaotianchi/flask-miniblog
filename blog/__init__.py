"""
Summary: The main program of the blog system.
Created at: 2023-12-19
Author: Gao Tianchi
"""


import click
from flask import Flask, g

from .config import get_config
from .controller import account_bp, author_bp, visitor_bp
from .extension import db
from .model.database import Category


def create_app(environment: str = None):
    config = get_config(environment)

    app = Flask(
        __package__,
        template_folder=config.PATH_TEMPLATE,
        static_folder=config.PATH_STATIC,
    )

    app.config.from_object(config)

    db.init_app(app)
    app.register_blueprint(visitor_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(author_bp)
    register_command(app)

    @app.context_processor
    def inject_current_user():
        return dict(current_user=g.current_user)

    return app


def register_command(app: Flask):
    @app.cli.command("initdb", help="Reset database.")
    def init_db():
        click.confirm(
            "This operation will delete all data in the database, do you want to continue?",
            abort=True,
        )
        db.drop_all()
        db.create_all()

        # Create default category.
        Category.create(
            "Uncategorized",
            "This category stores articles that have not been classified.",
        )

    @app.cli.command("fake", help="Generate fake data.")
    @click.option("--category", default=5, help="Generate fake category.")
    @click.option("--post", default=50, help="Generate fake post.")
    @click.option("--visitor", default=500, help="Generate fake visitor.")
    def fake(category: int, post: int, visitor: int):
        from .fakes.fakes import fake_category, fake_post, fake_user, fake_visitor

        db.drop_all()
        db.create_all()

        fake_user()

        fake_category(category)
        click.echo(f"Genearte {category} categories.")

        fake_post(post)
        click.echo(f"Generate {post} posts.")

        fake_visitor(visitor)
        click.echo(f"Generate {visitor} visitors.")

        click.echo("Done.")
