import pytest
from backend.app import create_app
from backend.extensions import db
from backend.models import User, Plant, UserPlant
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

import warnings
warnings.filterwarnings("ignore", message=".*SQLAlchemy.*")

@pytest.fixture(scope='module')
def app():
    """Создаем тестовое приложение с зарегистрированными маршрутами"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Явно регистрируем Blueprint (если нужно)
    from backend.auth import auth_bp
    from backend.plants import plants_bp
    from backend.articles import articles_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(plants_bp)
    app.register_blueprint(articles_bp)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Инициализация тестовых данных"""
    with app.app_context():
        # Очищаем базу
        db.session.query(UserPlant).delete()
        db.session.query(Plant).delete()
        db.session.query(User).delete()
        
        # Создаем тестового пользователя
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('testpass')
        )
        db.session.add(user)
        
        # Создаем тестовое растение
        plant = Plant(
            name='Test Plant',
            type='Test Type',
            image_url='/test.jpg',
            care_instructions='Test care',
            optimal_temperature='20-25°C',
            watering_interval=7
        )
        db.session.add(plant)
        db.session.commit()
        
        # Создаем связь пользователя и растения
        user_plant = UserPlant(
            user_id=user.id,
            plant_id=plant.id,
            last_watered=datetime.utcnow() - timedelta(days=2),
            next_watering=datetime.utcnow() + timedelta(days=5)
        )
        db.session.add(user_plant)
        db.session.commit()
        
@pytest.fixture
def test_user(app, init_database):
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        yield user

@pytest.fixture
def test_plant(app, init_database):
    with app.app_context():
        plant = Plant.query.first()
        yield plant

@pytest.fixture
def test_user_plant(app, init_database):
    with app.app_context():
        user_plant = UserPlant.query.first()
        yield user_plant 

@pytest.fixture
def auth_headers(client, test_user):
    login = client.post('/login',
        json={'email': 'test@example.com', 'password': 'testpass'},
        headers={'Content-Type': 'application/json'}
    )
    return {
        'Authorization': f'Bearer {login.get_json()["token"]}',
        'Content-Type': 'application/json'
    }       