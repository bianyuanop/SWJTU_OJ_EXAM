from flask import Flask, g
from . import db, _cmd

def create_app(config_filename):
    app = Flask(__name__)
#    if config_filename:
#        app.config.from_pyfile(config_filename)

    #TODO: add db init_app
#    db.init_app(app)

    g.session = db.get_session()

    @app.route("/")
    def index():
        return '{"content": "Hello, World"}'

    _cmd.init_app(app)

    return app
