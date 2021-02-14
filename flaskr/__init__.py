from flask import Flask, g, render_template
from . import db, _cmd

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.from_object('config.development')


    # register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    
    _cmd.init_app(app)

    @app.before_request
    def get_session():
        if not g.get('Session'):
            g.Session = db.get_session_factory()

#    @app.teardown_request
#    def pop_session():
#        if g.get('Session'):
#            g.pop(Session)
    

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
