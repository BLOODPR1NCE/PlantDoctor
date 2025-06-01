from flask import Blueprint, request, jsonify
from extensions import db
from models import Reminder, UserPlant
from auth import SECRET_KEY
import jwt
from datetime import datetime


reminders_bp = Blueprint('reminders', __name__, url_prefix='/api/reminders')

@reminders_bp.route('/', methods=['GET'])
def get_user_reminders():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Требуется авторизация"}), 401
    
    token = auth_header.split(' ')[1]
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Получаем напоминания пользователя
        reminders = Reminder.query.filter_by(user_id=data['user_id']).order_by(Reminder.due_date).all()
        
        result = []
        for reminder in reminders:
            plant_info = None
            if reminder.user_plant_id:
                user_plant = UserPlant.query.get(reminder.user_plant_id)
                if user_plant:
                    plant_info = {
                        "id": user_plant.plant.id,
                        "name": user_plant.plant.name,
                        "image_url": user_plant.custom_image_url or user_plant.plant.image_url
                    }
            
            result.append({
                "id": reminder.id,
                "type": reminder.reminder_type,
                "due_date": reminder.due_date.isoformat(),
                "is_completed": reminder.is_completed,
                "notes": reminder.notes,
                "plant": plant_info
            })
        
        return jsonify(result)
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401

@reminders_bp.route('', methods=['POST'])
@reminders_bp.route('/', methods=['POST'])
def create_reminder():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Требуется авторизация"}), 401
    
    try:
        token = auth_header.split(' ')[1]
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        reminder_data = request.get_json()
        
        # Проверка данных
        if not reminder_data:
            return jsonify({"error": "Необходимо передать данные в формате JSON"}), 400
        
        if not all(key in reminder_data for key in ['type', 'due_date']):
            return jsonify({"error": "Необходимо указать тип и дату напоминания"}), 400
        
        # Проверка и преобразование даты
        try:
            due_date = datetime.fromisoformat(reminder_data['due_date'])
        except ValueError:
            return jsonify({"error": "Неверный формат даты. Используйте формат YYYY-MM-DDTHH:MM:SS"}), 400
        
        # Создание напоминания
        reminder = Reminder(
            user_id=data['user_id'],
            user_plant_id=reminder_data.get('user_plant_id'),
            reminder_type=reminder_data['type'],
            due_date=due_date,
            notes=reminder_data.get('notes', '')
        )
        
        db.session.add(reminder)
        db.session.commit()
        
        return jsonify({
            "message": "Напоминание создано",
            "reminder": {
                "id": reminder.id,
                "type": reminder.reminder_type,
                "due_date": reminder.due_date.isoformat()
            }
        }), 201
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ошибка сервера: {str(e)}"}), 500

@reminders_bp.route('/<int:reminder_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_reminder(reminder_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Требуется авторизация"}), 401
    
    try:
        token = auth_header.split(' ')[1]
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        reminder = Reminder.query.filter_by(
            id=reminder_id,
            user_id=data['user_id']
        ).first()
        
        if not reminder:
            return jsonify({"error": "Напоминание не найдено"}), 404
        
        if request.method == 'GET':
            return jsonify({
                "id": reminder.id,
                "type": reminder.reminder_type,
                "due_date": reminder.due_date.isoformat(),
                "notes": reminder.notes
            })
            
        elif request.method == 'PUT':
            update_data = request.get_json()
            
            if 'is_completed' in update_data:
                reminder.is_completed = update_data['is_completed']
            
            if 'due_date' in update_data:
                reminder.due_date = datetime.fromisoformat(update_data['due_date'])
            
            if 'notes' in update_data:
                reminder.notes = update_data['notes']
            
            db.session.commit()
            
            return jsonify({
                "message": "Напоминание обновлено",
                "reminder": {
                    "id": reminder.id,
                    "type": reminder.reminder_type,
                    "due_date": reminder.due_date.isoformat(),
                    "is_completed": reminder.is_completed
                }
            })
            
        elif request.method == 'DELETE':
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({"message": "Напоминание удалено"})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
