from flask import Blueprint, request, jsonify
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from datetime import datetime, timedelta
import jwt
import os


auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "plantdoctor-secret-key"

@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    
    # Проверка данных
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Необходимо указать имя пользователя, email и пароль"}), 400
    
    # Проверка, существует ли пользователь
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Пользователь с таким email уже существует"}), 400
    
    # Создание нового пользователя
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Генерация токена
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        "message": "Пользователь успешно зарегистрирован",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Необходимо указать email и пароль"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Неверный email или пароль"}), 401
    
    # Генерация токена
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm="HS256")
    
    try:
        print("Полученный токен:", token)  # Логируем токен
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        print("Ошибка декодирования токена:", str(e))

    return jsonify({
        "message": "Успешный вход",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })

@auth_bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    auth_header  = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Токен отсутствует или неверный формат"}), 401
    
    try:
        token = auth_header.split(' ')[1]
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = User.query.get(data['user_id'])
        
        if not user:
            return jsonify({"error": "Пользователь не найден"}), 404
        
        if request.method == 'GET':
            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data and data['password']:
                user.set_password(data['password'])
            
            db.session.commit()
            return jsonify({"message": "Профиль успешно обновлен"})
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # В JWT логаут реализуется на клиенте удалением токена
    return jsonify({"message": "Успешный выход"})