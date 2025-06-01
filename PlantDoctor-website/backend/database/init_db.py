import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.models import User, Plant, Article, UserPlant, Reminder
from backend.app import create_app
from datetime import datetime, timedelta
from backend.extensions import db

app = create_app()

def init_sample_data():
    with app.app_context():
        # Очищаем базу данных
        db.drop_all()

        db.create_all()

        # Создаем тестового администратора
        admin = User(
            username='admin',
            email='admin@plantdoctor.com',
            avatar_url='/static/default-avatar.png'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Создаем тестового пользователя
        user = User(
            username='testuser',
            email='user@plantdoctor.com',
            avatar_url='/static/user-avatar.png'
        )
        user.set_password('test123')
        db.session.add(user)

        # Тестовые растения
        plants = [
            Plant(
                name="Орхидея Фаленопсис",
                scientific_name="Phalaenopsis",
                type="Орхидея",
                image_url="/static/orchid.jpg",
                care_instructions="Орхидеи требуют умеренного полива каждые 7-10 дней...",
                optimal_temperature="18-25°C",
                watering_interval=7,
                light_requirements="Яркий рассеянный свет",
                humidity_requirements="Высокая",
                difficulty_level="Средняя",
                toxicity=False
            ),
            Plant(
                name="Фикус Бенджамина",
                scientific_name="Ficus benjamina",
                type="Фикус",
                image_url="/static/ficus.jpg",
                care_instructions="Фикус Бенджамина любит регулярный полив...",
                optimal_temperature="20-25°C",
                watering_interval=5,
                light_requirements="Яркий свет",
                humidity_requirements="Средняя",
                difficulty_level="Легкая",
                toxicity=True
            ),
            Plant(
                name="Кактус",
                scientific_name="Cactaceae",
                type="Суккулент",
                image_url="/static/cactus.jpg",
                care_instructions="Кактусы требуют редкого полива...",
                optimal_temperature="15-30°C",
                watering_interval=14,
                light_requirements="Прямой солнечный свет",
                humidity_requirements="Низкая",
                difficulty_level="Очень легкая",
                toxicity=False
            )
        ]
        db.session.add_all(plants)
        db.session.commit()

        # Тестовые статьи
        articles = [
            Article(
                title="Как ухаживать за орхидеями",
                content="Орхидеи - прекрасные растения, но требуют особого ухода...",
                plant_id=1,
                author_id=1,
                is_featured=True,
                view_count=125,
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            Article(
                title="Общие советы по уходу за комнатными растениями",
                content="Комнатные растения требуют внимания и заботы...",
                author_id=1,
                is_featured=True,
                view_count=89,
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
            Article(
                title="Почему желтеют листья у фикуса?",
                content="Пожелтение листьев у фикуса может быть вызвано несколькими причинами...",
                plant_id=2,
                author_id=2,
                view_count=42,
                created_at=datetime.utcnow() - timedelta(days=1)
            )
        ]
        db.session.add_all(articles)
        db.session.commit()

        # Тестовые растения пользователя
        user_plants = [
            UserPlant(
                user_id=2,
                plant_id=1,
                nickname="Моя орхидея",
                last_watered=datetime.utcnow() - timedelta(days=2),
                next_watering=datetime.utcnow() + timedelta(days=5),
                notes="Поливать только утром",
                health_status="good"
            ),
            UserPlant(
                user_id=2,
                plant_id=3,
                nickname="Колючка",
                last_watered=datetime.utcnow() - timedelta(days=10),
                next_watering=datetime.utcnow() + timedelta(days=4),
                health_status="excellent"
            )
        ]
        db.session.add_all(user_plants)
        db.session.commit()

        # Тестовые напоминания
        reminders = [
            Reminder(
                user_id=2,
                user_plant_id=1,
                reminder_type="watering",
                due_date=datetime.utcnow() + timedelta(days=5),
                notes="Полить утром"
            ),
            Reminder(
                user_id=2,
                reminder_type="fertilizing",
                due_date=datetime.utcnow() + timedelta(days=3),
                notes="Удобрить все растения"
            )
        ]
        db.session.add_all(reminders)
        db.session.commit()
        
        print("База данных успешно инициализирована с тестовыми данными!")

if __name__ == '__main__':
    init_sample_data()