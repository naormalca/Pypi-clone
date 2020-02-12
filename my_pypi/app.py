import os
import sys
import flask
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import my_pypi.data.db_session as db_session

app = flask.Flask(__name__)


def main():
    register_blueprints()
    setup_db()
    app.run(debug=True)


def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'pypi.sqlite')

    db_session.global_init(db_file)


def register_blueprints():
    from my_pypi.views import home_views
    from my_pypi.views import package_views
    from my_pypi.views import cms_views
    from my_pypi.views import account_views

    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(cms_views.blueprint)


if __name__ == '__main__':
    main()
