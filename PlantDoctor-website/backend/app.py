from flask import Flask, jsonify, request, render_template  
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from extensions import db
import os


def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Authorization"],
            "supports_credentials": True
        }
    })

    # Конфигурация
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///../database/plantdoctor.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'plantdoctor-secret-key')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '../uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    # Инициализация базы данных
    db.init_app(app)


    with app.app_context():
        from auth import auth_bp
        from plants import plants_bp
        from articles import articles_bp
        from reminders import reminders_bp
        from admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plants_bp, url_prefix='/api')
    app.register_blueprint(articles_bp,  url_prefix='/api')
    app.register_blueprint(reminders_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
         return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    # Создаем папку для загрузок, если ее нет
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)