import hashlib
from datetime import timedelta
from typing import Optional

from flask import Request, Response
from my_pypi.utils import num_convert

auth_cookie_name = "mypypi_user"

def set_auth(response: Response, user_id: int):
    ''' hash the user id and set it has a cookie '''
    hash_val = __hash_text(str(user_id))
    val = "{}:{}".format(user_id, hash_val)
    response.set_cookie(auth_cookie_name, val)

def __hash_text(text: str) -> str:
    text = 'salty__' + text + '__text'
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


def __add_cookie_callback(_, response: Response, name: str, value: str):
    response.set_cookie(name, value, max_age=timedelta(days=30))

def get_user_id_via_cookie(request: Request) -> Optional[int]:
    if auth_cookie_name not in request.cookies:
        return None
    
    val = request.cookies[auth_cookie_name]
    parts = val.split(':')
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]
    if hash_val != __hash_text(user_id):
        print("Warning: hash mismatch")
        return None
    return num_convert.try_int(user_id)

def logout(response: Response):
    response.delete_cookie(auth_cookie_name)