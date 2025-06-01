from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Plant, Article
from auth import SECRET_KEY
import jwt
from datetime import datetime


admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def is_admin(token):
    if not token:
        return False
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = User.query.get(data['user_id'])
        return user and user.username == 'admin'
    except:
        return False

@admin_bp.route('/plants', methods=['POST'])
def add_plant():
    token = request.headers.get('Authorization')
    if not is_admin(token):
        return jsonify({"error": "Доступ запрещен"}), 403
    
    plant_data = request.get_json()
    if not plant_data or not plant_data.get('name') or not plant_data.get('type'):
        return jsonify({"error": "Необходимо указать название и тип растения"}), 400
    
    plant = Plant(
        name=plant_data['name'],
        type=plant_data['type'],
        scientific_name=plant_data.get('scientific_name'),
        image_url=plant_data.get('image_url', '/static/default-plant.jpg'),
        care_instructions=plant_data.get('care_instructions', ''),
        optimal_temperature=plant_data.get('optimal_temperature', ''),
        watering_interval=plant_data.get('watering_interval', 7),
        light_requirements=plant_data.get('light_requirements', ''),
        humidity_requirements=plant_data.get('humidity_requirements', ''),
        difficulty_level=plant_data.get('difficulty_level', ''),
        toxicity=plant_data.get('toxicity', False)
    )
    
    db.session.add(plant)
    db.session.commit()
    
    return jsonify({
        "message": "Растение добавлено",
        "plant": {
            "id": plant.id,
            "name": plant.name,
            "type": plant.type
        }
    }), 201

@admin_bp.route('/plants/<int:plant_id>', methods=['PUT', 'DELETE'])
def manage_plant(plant_id):
    token = request.headers.get('Authorization')
    if not is_admin(token):
        return jsonify({"error": "Доступ запрещен"}), 403
    
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({"error": "Растение не найдено"}), 404
    
    if request.method == 'PUT':
        update_data = request.get_json()
        
        if 'name' in update_data:
            plant.name = update_data['name']
        if 'type' in update_data:
            plant.type = update_data['type']
        if 'scientific_name' in update_data:
            plant.scientific_name = update_data['scientific_name']
        if 'image_url' in update_data:
            plant.image_url = update_data['image_url']
        if 'care_instructions' in update_data:
            plant.care_instructions = update_data['care_instructions']
        if 'optimal_temperature' in update_data:
            plant.optimal_temperature = update_data['optimal_temperature']
        if 'watering_interval' in update_data:
            plant.watering_interval = update_data['watering_interval']
        if 'light_requirements' in update_data:
            plant.light_requirements = update_data['light_requirements']
        if 'humidity_requirements' in update_data:
            plant.humidity_requirements = update_data['humidity_requirements']
        if 'difficulty_level' in update_data:
            plant.difficulty_level = update_data['difficulty_level']
        if 'toxicity' in update_data:
            plant.toxicity = update_data['toxicity']
        
        db.session.commit()
        
        return jsonify({
            "message": "Растение обновлено",
            "plant": {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type
            }
        })
    
    elif request.method == 'DELETE':
        db.session.delete(plant)
        db.session.commit()
        
        return jsonify({"message": "Растение удалено"})

@admin_bp.route('/users', methods=['GET'])
def get_users():
    token = request.headers.get('Authorization')
    if not is_admin(token):
        return jsonify({"error": "Доступ запрещен"}), 403
    
    users = User.query.all()
    result = []
    
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
            "plants_count": len(user.plants),
            "articles_count": len(user.articles)
        })
    
    return jsonify(result)

@admin_bp.route('/articles/featured', methods=['PUT'])
def feature_article():
    token = request.headers.get('Authorization')
    if not is_admin(token):
        return jsonify({"error": "Доступ запрещен"}), 403
    
    data = request.get_json()
    if not data or 'article_id' not in data or 'featured' not in data:
        return jsonify({"error": "Необходимо указать ID статьи и статус"}), 400
    
    article = Article.query.get(data['article_id'])
    if not article:
        return jsonify({"error": "Статья не найдена"}), 404
    
    article.is_featured = data['featured']
    db.session.commit()
    
    return jsonify({
        "message": "Статус статьи обновлен",
        "article": {
            "id": article.id,
            "title": article.title,
            "is_featured": article.is_featured
        }
    })