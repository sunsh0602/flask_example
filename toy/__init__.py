import os

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import redis

api = Api(
    version='1.0',
    title='toy_project',
    prefix='/api',
    contact='',
    contact_email='email address',
    description="desc",
)

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

jwt_redis = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0, decode_responses=True)


def create_app():
    app = Flask(__name__)

    # restx api
    api.init_app(app)

    # bcrypt
    bcrypt.init_app(app)

    # jwt
    jwt.init_app(app)

    # config (start.sh 명시)
    config = app.config.get('ENV')
    if config == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config == 'testing':
        app.config.from_object('config.TestingConfig')
    else:  # development
        app.config.from_object('config.DevelopmentConfig')

    # database
    from toy.models import example_models
    db.init_app(app)
    migrate.init_app(app, db)

    # routes list for blueprint
    # from .routes import routes_list
    # routes_list(app)

    # routes list for restx
    from .routes import routes_list
    routes_list(api)

    # general error handler
    from .common.errors import error_handle
    error_handle(api)

    return app