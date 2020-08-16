import os
import sys
import flask
from flask import make_response, jsonify
from flask_cors import CORS

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import my_pypi.data.db_session as db_session
from my_pypi.config import DevelopmentConfig, ProductionConfig 
from my_pypi.log import fileHandler, streamHandler

def create_app():
    app = flask.Flask(__name__)
    CORS(app)
    register_blueprints(app)

    #configuration
    app.config.from_object(os.environ['FLASK_CONFIG'])
    app.config['CORS_HEADERS'] = 'Content-Type'
    db_session.global_init(app.config['SQLALCHEMY_DATABASE_URI'], False)

    #logger
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")

    @app.before_request
    def before_request():
        from flask import request
        context = {
            'url': request.path,
            'method': request.method,
        }
        app.logger.debug("Handling %(method)s request for %(url)s", context)

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error("User tried to enter this route: {}".format(flask.request.base_url))
        message = 'API endpoint not found'
        return make_response(jsonify(message), 404)
    
    return app

def register_blueprints(app):
    # API
    from my_pypi.api import packages, auth, users
    app.register_blueprint(packages.blueprint, url_prefix='/api/packages')
    app.register_blueprint(auth.blueprint, url_prefix='/api/auth')
    app.register_blueprint(users.blueprint, url_prefix='/api/users')



if __name__ == '__main__':
    app = create_app()
    app.run(port=80, host="0.0.0.0", use_reloader=True)
else:
    gunicorn_app = create_app()
        

