from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

#
# class ProductionConfig:
#     FLASK_ENV = "prod"
#     DEBUG = False
#     TESTING = False
#     SQLALCHEMY_DATABASE_URI = (
#         f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
#         f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
#     )


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class TestConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('TEST_DB_NAME')}"
    )


def create_app(config = "config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config)

    migrate = Migrate(app, db)
    api = Api(app)

    [api.add_resource(*r) for r in routes]

    return app
