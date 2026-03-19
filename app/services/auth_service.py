from app.repositories.user_repository import get_by_username, create
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

def register(data):
    if get_by_username(data['username']):
        raise Exception('User already exists')

    user = User(
        username=data['username'],
        password=generate_password_hash(data['password'])
    )
    return create(user)

def login(data):
    user = get_by_username(data['username'])

    if not user or not check_password_hash(user.password, data['password']):
        raise Exception('Invalid credentials')

    return user
