import os
import sys
import flask 
from flask_cors import CORS

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import my_pypi.data.db_session as db_session
from my_pypi.config import DevelopmentConfig 
from my_pypi.log import fileHandler, streamHandler

app = flask.Flask(__name__)
CORS(app)
def main():
    register_blueprints()
    app.config.from_object(DevelopmentConfig)
    app.config['CORS_HEADERS'] = 'Content-Type'
    db_session.global_init(app.config['SQLALCHEMY_DATABASE_URI'], False)
    #error handling
    app.register_error_handler(404, page_not_found)
    #logger
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(port=5000, host="0.0.0.0", use_reloader=True)
    

def register_blueprints():
    # API
    from my_pypi.api import packages, auth, users
    app.register_blueprint(packages.blueprint, url_prefix='/api/packages')
    app.register_blueprint(auth.blueprint, url_prefix='/api/auth')
    app.register_blueprint(users.blueprint, url_prefix='/api/users')

@app.before_request
def before_request():
    from flask import request
    context = {
        'url': request.path,
        'method': request.method,
    }
    app.logger.debug("Handling %(method)s request for %(url)s", context)

def page_not_found(e):
    app.logger.error("User tried to enter this route: {}".format(flask.request.base_url))
    return flask.render_template('error/404.html'), 404

if __name__ == '__main__':
    main()
