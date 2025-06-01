from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    avatar_url = db.Column(db.String(255))
    
    plants = db.relationship('UserPlant', back_populates='user', cascade='all, delete-orphan')
    articles = db.relationship('Article', back_populates='author')
    reminders = db.relationship('Reminder', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100))
    type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255))
    care_instructions = db.Column(db.Text)
    optimal_temperature = db.Column(db.String(20))
    watering_interval = db.Column(db.Integer)
    light_requirements = db.Column(db.String(50))
    humidity_requirements = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))
    toxicity = db.Column(db.Boolean, default=False)
    
    user_plants = db.relationship('UserPlant', back_populates='plant')
    articles = db.relationship('Article', back_populates='plant')

class UserPlant(db.Model):
    __tablename__ = 'user_plants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    nickname = db.Column(db.String(100))
    last_watered = db.Column(db.DateTime)
    next_watering = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    health_status = db.Column(db.String(50), default='good')
    custom_image_url = db.Column(db.String(255))
    
    user = db.relationship('User', back_populates='plants')
    plant = db.relationship('Plant', back_populates='user_plants')
    reminders = db.relationship('Reminder', back_populates='user_plant')

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    plant = db.relationship('Plant', back_populates='articles')
    author = db.relationship('User', back_populates='articles')

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_plant_id = db.Column(db.Integer, db.ForeignKey('user_plants.id'))
    reminder_type = db.Column(db.String(50), nullable=False)  # watering, fertilizing, pruning, etc.
    due_date = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    user = db.relationship('User', back_populates='reminders')
    user_plant = db.relationship('UserPlant', back_populates='reminders')

# Создаем индексы для улучшения производительности
event.listen(User.__table__, 'after_create', db.DDL('CREATE INDEX idx_user_email ON users (email)'))
event.listen(Plant.__table__, 'after_create', db.DDL('CREATE INDEX idx_plant_type ON plants (type)'))
event.listen(UserPlant.__table__, 'after_create', 
             db.DDL('CREATE INDEX idx_user_plant ON user_plants (user_id, plant_id)'))
