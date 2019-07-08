from flask import Flask
from flask_googlemaps import GoogleMaps

import os

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route("/hello")
    def hello():
        return 'Hello World!'

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import address
    app.register_blueprint(address.bp)

    return app

if __name__ == "__main__":
    create_app().run()