from flask import Blueprint, request, jsonify
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
