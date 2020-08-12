from typing import Optional, List
import datetime

import my_pypi.data.db_session as db_session
from my_pypi.data.users import User
from my_pypi.utils import crypto

def get_user_count() -> int:
    session = db_session.create_session()
    return session.query(User).count()

def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.email == email).first()

def find_user_by_id(user_id: str) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.id == user_id).first()

def create_user(name: str, email: str, password : str) -> Optional[User]:
    if find_user_by_email(email):
        return None
    
    user = User()  
    user.name = name
    user.email = email
    user.hashed_password = crypto.hash_text(password)
    
    session = db_session.create_session()
    session.add(user)
    session.commit()
    
    return user 

def login_user(email: str, password: str) -> Optional[User]:
    session = db_session.create_session()

    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    if not crypto.verify_hash(user.hashed_password , password):
        return None
    #update the login time
    user.last_login = datetime.datetime.now()
    session.commit()

    return user

def get_new_users(limit = 10) -> List[User]:
    session = db_session.create_session()

    users = session.query(User).order_by(User.created_date.desc()) \
        .limit(limit).all()
    
    session.close()

    return users

def get_latest_logged(limit = 10) -> List[User]:
    session = db_session.create_session()

    users = session.query(User).order_by(User.last_login.desc()) \
        .limit(limit).all()
    
    session.close()
    
    return users