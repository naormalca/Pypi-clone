import os
import sys
import flask 

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import my_pypi.data.db_session as db_session
from my_pypi.config import DevelopmentConfig 
from my_pypi.utils.custom_filters import regex_replace

app = flask.Flask(__name__)

def main():
    register_blueprints()
    app.config.from_object(DevelopmentConfig)
    db_session.global_init(app.config['SQLALCHEMY_DATABASE_URI'], False)
    app.jinja_env.filters['regex_replace'] = regex_replace
    app.run(port=5000, host="0.0.0.0", use_reloader=True)
    

def register_blueprints():
    from my_pypi.views import home_views
    from my_pypi.views import package_views
    from my_pypi.views import cms_views
    from my_pypi.views import account_views
    from my_pypi.views import stats_views

    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(cms_views.blueprint)
    app.register_blueprint(stats_views.blueprint)

if __name__ == '__main__':
    main()
