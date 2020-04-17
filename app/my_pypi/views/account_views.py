import flask

from my_pypi.app import app
from my_pypi.infrastructure.view_modifiers import response
from my_pypi.services import user_service
from my_pypi.infrastructure import cookie_auth
from my_pypi.infrastructure import request_dict
from my_pypi.viewmodels.account.index_viewmodel import IndexViewModel
from my_pypi.viewmodels.account.register_viewmodel import RegisterViewModel
from my_pypi.viewmodels.account.login_viewmodel import LoginViewModel
from my_pypi.viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = flask.Blueprint('account', __name__, template_folder='templates')

# ################### INDEX #################################
@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')
    return vm.to_dict()


# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    if vm.user_id:
        return flask.redirect('/account')
    return vm.to_dict()

@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    vm = RegisterViewModel()
    vm.validate()
    if vm.error:
        return vm.to_dict()    

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The account could not be created'
        return vm.to_dict()
        
    response = flask.redirect('/account')
    cookie_auth.set_auth(response, user.id)
    app.logger.info("{} has registered".format(user.id))
    return response


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    vm = LoginViewModel()
    if vm.user_id:
        return flask.redirect('/account')
    return vm.to_dict()

@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    
    user = user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    response = flask.redirect('/account')
    cookie_auth.set_auth(response, user.id)
    app.logger.info("{} has logged in".format(user.id))
    return response


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    response = flask.redirect('/')
    user_id = cookie_auth.get_user_id_via_cookie(flask.request)
    app.logger.info("{} has logged out".format(user_id))
    cookie_auth.logout(response)
    return response


#################### USER-PAGE #################################

@blueprint.route('/account/<user_id>', methods=['GET'])
@response(template_file='account/userpage.html')
def userpage(user_id: str):
    vm = ViewModelBase()
    vm.user_details = user_service.find_user_by_id(user_id)
    if not vm.user_details:
        return flask.abort(404)
    return vm.to_dict()
