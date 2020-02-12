import flask

from my_pypi.infrastructure.view_modifiers import response
from my_pypi.services import user_service
blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    return {}


# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {}


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    r = flask.request

    name = r.form.get('name')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password').lower().strip()
    
    if not name or not email or not password:
        return {
            'name': name,
            'password': password,
            'email': email,
            'error': "Some required fields are missing."
        }

    user = user_service.create_user(name, email, password)
    if not user:
        return {
            'name': name,
            'password': password,
            'email': email,
            'error': "A user with that email already exists."
        }

    return flask.redirect('/account')


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    return {}


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    return {}
