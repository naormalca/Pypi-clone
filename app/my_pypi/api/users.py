import flask
from flask_cors import cross_origin
from my_pypi.infrastructure import request_dict
from my_pypi.services import user_service
from my_pypi.data.schemas import UserSchema

blueprint = flask.Blueprint(
    'api_users', __name__, url_prefix='/api/users')


@blueprint.route('/')
@cross_origin()
def get_users():
    '''
    API to reterive users:
    /users?order=logged_at&limit=N => returns the N latest logged users 
    /users?order=created_at&limit=N => returns the N new_users
    /users?id={userId} => return a single user by id 
    '''
    req_dict = request_dict.create('')
    if req_dict.order:
        userSchema = UserSchema(exclude=("hashed_password",
                                         "profile_image_url",
                                         "email", "created_date",
                                         "profile_image_url", "last_login"
                                         ))
        #latest users
        if req_dict.order == 'logged_at':
            limit = req_dict.limit if req_dict.limit else 10
            latest_logged = user_service.get_latest_logged(limit)
            users = userSchema.dumps(latest_logged, many=True)
            if users:
                response_obj = users
                return response_obj, 200
            else:
                response_obj = {'error': 'No users exist'}
                return response_obj, 201
        #new_users
        elif req_dict.order == 'created_at':
            limit = req_dict.limit if req_dict.limit else 10
            new_users = user_service.get_new_users(limit)
            users = userSchema.dumps(new_users, many=True)
            if users:
                response_obj = users
                return response_obj, 200
            else:
                response_obj = {'error': 'No users exist'}
                return response_obj, 201
    #single user
    elif req_dict.id:
        userSchema = UserSchema(only=("name", "last_login", "email"))
        user = user_service.find_user_by_id(req_dict.id)
        if not user:
            print(1)
            response_obj = {'error': 'User not exists'}
            return response_obj, 201
        else:
            res = userSchema.dumps(user)
            response_obj = res
            return response_obj, 200
    response_obj = {'error': ''}
    return response_obj, 201
