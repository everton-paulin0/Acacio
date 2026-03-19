import os

estrutura = {
    "app/__init__.py": """from flask import Flask
from .extensions import db, migrate, jwt
from .config import Config
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    return app
""",

    "app/config.py": """import os

class Config:
    SECRET_KEY = 'supersecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret'
""",

    "app/extensions.py": """from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
""",

    "app/models/__init__.py": "",
    
    "app/models/user.py": """from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
""",

    "app/repositories/__init__.py": "",
    
    "app/repositories/user_repository.py": """from app.models.user import User
from app.extensions import db

def get_by_username(username):
    return User.query.filter_by(username=username).first()

def create(user):
    db.session.add(user)
    db.session.commit()
    return user
""",

    "app/services/__init__.py": "",
    
    "app/services/auth_service.py": """from app.repositories.user_repository import get_by_username, create
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
""",

    "app/routes/__init__.py": """from .auth_routes import auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
""",

    "app/routes/auth_routes.py": """from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import register, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        user = register(request.json)
        return jsonify({'msg': 'User created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login_user():
    try:
        user = login(request.json)
        token = create_access_token(identity=user.id)
        return jsonify({'access_token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 401
""",

    "run.py": """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
""",

    "requirements.txt": """flask
flask-sqlalchemy
flask-migrate
flask-jwt-extended
werkzeug
""",

    "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
""",

    "docker-compose.yml": """version: '3.9'

services:
  api:
    build: .
    container_name: flask_api
    ports:
      - "5000:5000"
    volumes:
      - .:/app
""",

    ".dockerignore": """__pycache__
*.pyc
venv
.env
"""
}

for caminho, conteudo in estrutura.items():
    dir_path = os.path.dirname(caminho)
    if dir_path:  # Só cria diretório se não for vazio
        os.makedirs(dir_path, exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)

print('🚀 API ENTERPRISE criada com Docker + SQLite!')
