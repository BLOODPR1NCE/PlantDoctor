from flask import Blueprint, request, jsonify
from extensions import db
from models import Plant, UserPlant
from datetime import datetime, timedelta
from auth import SECRET_KEY
import jwt

plants_bp = Blueprint('plants', __name__)

@plants_bp.route('/plants', methods=['GET'])
def get_all_plants():
    plants = Plant.query.all()
    result = []
    for plant in plants:
        result.append({
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "image_url": plant.image_url,
            "care_instructions": plant.care_instructions,
            "optimal_temperature": plant.optimal_temperature,
            "watering_interval": plant.watering_interval
        })
    return jsonify(result)

@plants_bp.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant_details(plant_id):
    try:
        plant = Plant.query.get(plant_id)
        if not plant:
            return jsonify({"error": "Растение не найдено"}), 404
        
        return jsonify({
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "image_url": plant.image_url,
            "care_instructions": plant.care_instructions,
            "optimal_temperature": plant.optimal_temperature,
            "watering_interval": plant.watering_interval
        })
    except Exception as e:
        print(f"Ошибка при получении растения {plant_id}: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

@plants_bp.route('/user/plants', methods=['GET', 'POST'])
def handle_user_plants():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Требуется авторизация"}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = data['user_id']
        
        if request.method == 'GET':
            user_plants = UserPlant.query.filter_by(user_id=data['user_id']).all()
        
            result = []
            for user_plant in user_plants:
                plant = Plant.query.get(user_plant.plant_id)
                result.append({
                    "id": user_plant.id,
                    "plant_id": plant.id,
                    "name": plant.name,
                    "type": plant.type,
                    "image_url": plant.image_url,
                    "last_watered": user_plant.last_watered.isoformat() if user_plant.last_watered else None,
                    "next_watering": user_plant.next_watering.isoformat() if user_plant.next_watering else None,
                    "notes": user_plant.notes
                })
        
            return jsonify(result)
        
        elif request.method == 'POST':
            plant_data = request.get_json()
        
            if not plant_data or not plant_data.get('plant_id'):
                return jsonify({"error": "Необходимо указать ID растения"}), 400
        
            # Проверяем, есть ли уже такое растение у пользователя
            existing = UserPlant.query.filter_by(
                user_id=data['user_id'],
                plant_id=plant_data['plant_id']
            ).first()
        
            if existing:
                return jsonify({"error": "Это растение уже добавлено в ваш профиль"}), 400
        
            # Получаем информацию о растении
            plant = Plant.query.get(plant_data['plant_id'])
            if not plant:
                return jsonify({"error": "Растение не найдено"}), 404
        
            # Создаем запись о растении пользователя
            user_plant = UserPlant(
                user_id=data['user_id'],
                plant_id=plant_data['plant_id'],
                notes=plant_data.get('notes', '')
            )
        
            db.session.add(user_plant)
            db.session.commit()
        
            return jsonify({
                "message": "Растение успешно добавлено",
                "plant": {
                    "id": user_plant.id,
                    "plant_id": plant.id,
                    "name": plant.name,
                    "type": plant.type,
                    "image_url": plant.image_url
                }
        }), 201
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@plants_bp.route('/user/plants/<int:user_plant_id>/water', methods=['POST'])
def water_plant(user_plant_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Требуется авторизация"}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_plant = UserPlant.query.get(user_plant_id)
        
        if not user_plant or user_plant.user_id != data['user_id']:
            return jsonify({"error": "Растение не найдено"}), 404
        
        # Получаем данные из тела запроса
        request_data = request.get_json()
        watering_date = datetime.strptime(request_data.get('date'), '%Y-%m-%d') if request_data and 'date' in request_data else datetime.utcnow()
        
        # Получаем информацию о растении для интервала полива
        plant = Plant.query.get(user_plant.plant_id)
        watering_interval = int(request_data.get('interval')) if request_data and 'interval' in request_data else (plant.watering_interval if plant else 7)
        
        # Обновляем даты полива
        user_plant.last_watered = watering_date
        user_plant.next_watering = watering_date + timedelta(days=watering_interval)
        
        db.session.commit()
        
        return jsonify({
            "message": "Полив отмечен",
            "last_watered": user_plant.last_watered.isoformat(),
            "next_watering": user_plant.next_watering.isoformat()
        })
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401
    except ValueError as e:
        return jsonify({"error": f"Неверный формат даты: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@plants_bp.route('/user/plants/<int:user_plant_id>', methods=['DELETE'])
def remove_user_plant(user_plant_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Требуется авторизация"}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_plant = UserPlant.query.get(user_plant_id)
        
        if not user_plant or user_plant.user_id != data['user_id']:
            return jsonify({"error": "Растение не найдено"}), 404
        
        db.session.delete(user_plant)
        db.session.commit()
        
        return jsonify({"message": "Растение удалено из вашего профиля"})
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500