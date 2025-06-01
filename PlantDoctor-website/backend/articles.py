from flask import Blueprint, request, jsonify
from extensions import db
from models import Article, Plant
from auth import SECRET_KEY
import jwt


articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles', methods=['GET'])
def get_all_articles():
    featured = request.args.get('featured', '').lower() == 'true'
    
    query = Article.query
    if featured:
        query = query.filter_by(is_featured=True)
    
    articles = query.order_by(Article.created_at.desc()).all()
    
    result = []
    for article in articles:
        plant_name = article.plant.name if article.plant else None
        result.append({
            "id": article.id,
            "title": article.title,
            "excerpt": article.content[:150] + '...' if len(article.content) > 150 else article.content,
            "plant_id": article.plant_id,
            "plant_name": plant_name,
            "author": article.author.username,
            "created_at": article.created_at.isoformat(),
            "is_featured": article.is_featured
        })
    
    return jsonify(result)

@articles_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": "Статья не найдена"}), 404
    
    plant_name = article.plant.name if article.plant else None
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "plant_id": article.plant_id,
        "plant_name": plant_name,
        "author": article.author.username,
        "created_at": article.created_at.isoformat(),
        "is_featured": article.is_featured
    })

@articles_bp.route('/articles/plant/<int:plant_id>', methods=['GET'])
def get_articles_for_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({"error": "Растение не найдено"}), 404
    
    articles = Article.query.filter_by(plant_id=plant_id).order_by(Article.created_at.desc()).all()
    
    result = []
    for article in articles:
        result.append({
            "id": article.id,
            "title": article.title,
            "excerpt": article.content[:150] + '...' if len(article.content) > 150 else article.content,
            "author": article.author.username,
            "created_at": article.created_at.isoformat()
        })
    
    return jsonify(result)

@articles_bp.route('/articles', methods=['POST'])
def create_article():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Токен отсутствует"}), 401
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        article_data = request.get_json()
        
        if not article_data or not article_data.get('title') or not article_data.get('content'):
            return jsonify({"error": "Необходимо указать заголовок и содержание статьи"}), 400
        
        article = Article(
            title=article_data['title'],
            content=article_data['content'],
            plant_id=article_data.get('plant_id'),
            author_id=data['user_id'],
            is_featured=article_data.get('is_featured', False)
        )
        
        db.session.add(article)
        db.session.commit()
        
        return jsonify({
            "message": "Статья успешно создана",
            "article": {
                "id": article.id,
                "title": article.title
            }
        }), 201
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Токен истек"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Неверный токен"}), 401