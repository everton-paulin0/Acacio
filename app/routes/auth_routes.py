from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import register, login
from flask import Blueprint, request, jsonify

from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

# 🔥 variável global (SÓ PRA TESTE)
user_logged = None


@auth_bp.route('/login', methods=['POST'])
def login_post():
    global user_logged

    data = request.json
    user_logged = data.get("username")

    return jsonify({"msg": "login ok"})


@auth_bp.route('/login', methods=['GET'])
def login_get():
    return jsonify({
        "user": user_logged
    })