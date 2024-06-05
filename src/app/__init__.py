import logging
from flask import Flask
from .config import Config
import sys
import os
from app.handlers import handler_blueprint
from app.routes import routes_blueprint


def create_app(config_class: type[Config] = Config) -> Flask:
    """
    Basic Flask app factory

    :param config: Configuration type, either basic for the regular app or testing for pytest.
    :returns: Flask app with configured logger.
    """

    template_dir = os.path.abspath('/swagger/templates')
    static_dir = os.path.abspath('/swagger/static')
    app = Flask(__name__, template_folder=template_dir,
                static_folder=static_dir)
    app.logger.info("Flask app started.")

    app.config.from_object(config_class)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info("Configs and logger loaded.")

    app.register_blueprint(handler_blueprint)
    app.register_blueprint(routes_blueprint)
    app.logger.info("Blueprintes registered.")
    return app
