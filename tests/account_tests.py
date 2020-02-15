from flask import Response
from test_client import flask_app, client
from my_pypi.data.users import User
from my_pypi.viewmodels.account.register_viewmodel import RegisterViewModel
import unittest.mock

def test_register_validation_when_valid():
    # Arrange

    form_data = {
        'name': 'Naor',
        'email': 'm@mypypi.com',
        'password': 'xyzxyz'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'my_pypi.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()
    
    # Assert
    assert vm.error is None

def test_register_validation_when_email_already_exists(): 
    # Arrange

    form_data = {
        'name': 'Naor',
        'email': 'm@mypypi.com',
        'password': 'xyzxyz'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'my_pypi.services.user_service.find_user_by_email'
    test_user = User(email=form_data.get('email'))
    with unittest.mock.patch(target, return_value=test_user):
        vm.validate()
    
    # Assert
    assert vm.error is not None
    assert 'already exists' in vm.error


def test_register_view_new_user(): 
    # Arrange
    from my_pypi.views.account_views import register_post
    form_data = {
        'name': 'Naor',
        'email': 'm@mypypi.com',
        'password': 'xyzxyz'
    }

    target = 'my_pypi.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        target = 'my_pypi.services.user_service.create_user'
        with unittest.mock.patch(target, return_value=User()):
            with flask_app.test_request_context(path='/account/register', data=form_data):
                # Act
                response : Response = register_post()

    
    # Assert
    assert response.location == '/account'

def test_register_view_new_user_v2(): 
    # Arrange
    from my_pypi.views.account_views import register_post
    form_data = {
        'name': 'Naor',
        'email': 'm@mypypi.com',
        'password': 'xyzxyz'
    }

    target = 'my_pypi.services.user_service.find_user_by_email'
    find_user_mock = unittest.mock.patch(target, return_value=None) 
    target = 'my_pypi.services.user_service.create_user'
    create_user_mock = unittest.mock.patch(target, return_value=User())
    request = flask_app.test_request_context(path='/account/register', data=form_data)
    
    with find_user_mock, create_user_mock, request:        
        # Act
        response : Response = register_post()

    
    # Assert
    assert response.location == '/account'

def test_int_account_home_no_login(client):
    target = 'my_pypi.services.user_service.find_user_by_id'
    with unittest.mock.patch(target, return_value=None):
        resp: Response = client.get('/account')

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/account/login'

def test_int_account_home_with_login(client):
    target = 'my_pypi.services.user_service.find_user_by_id'
    test_user = User(name='Naor', email='m@gmail.com')
    with unittest.mock.patch(target, return_value=test_user):
        resp: Response = client.get('/account')

    assert resp.status_code == 200
    assert b'Naor' in resp.data