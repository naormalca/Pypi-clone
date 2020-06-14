import flask
from flask import request
from flask_cors import cross_origin
from my_pypi.data import users
from my_pypi.services import user_service
from my_pypi.data.users import User
blueprint = flask.Blueprint(
    'auth_packages', __name__, url_prefix='/api/auth')

#INPUT: name, email, password.


@blueprint.route('/signup', methods=['POST'])
@cross_origin()
def signUp():
    post_data = request.get_json()
    user = user_service.create_user(post_data.get('name'),
                                    post_data.get('email'),
                                    post_data.get('password'))
    try:
        if user:
            auth_token = user.encode_auth_token()
            print(auth_token)
            if auth_token:
                response_obj = {
                    'status': 'success',
                    'auth_token': auth_token.decode()
                }
                print(response_obj)
                return response_obj, 201

        else:
            response_obj = {
                'status': 'failed',
                'error': 'User already exists.'
            }
            print(response_obj)
            return response_obj, 202
    except Exception as e:
        response_obj = {
            'status': 'failed',
            'error': e
        }
        print(response_obj)
        return response_obj, 401


@blueprint.route('/login', methods=['POST'])
@cross_origin()
def login():
    post_data = request.get_json()
    user = user_service.login_user(post_data.get('email'),
                                   post_data.get('password'))
    try:
        if user:
            auth_token = user.encode_auth_token()
            if auth_token:
                response_obj = {
                    'status': 'success',
                    'auth_token': auth_token.decode()
                }
                print(response_obj)
                return response_obj, 200

        else:
            response_obj = {
                'status': 'failed',
                'error': 'The account does not exist or the password is wrong.'
            }
            print(response_obj)
            return response_obj, 202
    except Exception as e:
        response_obj = {
            'status': 'failed',
            'error': e
        }
        print(response_obj)
        return response_obj, 401


@blueprint.route('/auto-login')
@cross_origin()
def auto_login():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = user_service.find_user_by_id(user_id=resp)
            response_obj = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                }
            }
            return response_obj, 200
        response_obj = {
            'status': 'fail',
            'error': resp
        }
        return response_obj, 401
    else:
        response_obj = {
            'status': 'fail',
            'error': 'Provide a valid auth token.'
        }
        return response_obj, 401
