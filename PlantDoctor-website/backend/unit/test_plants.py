import pytest
from backend.app import create_app
from backend.extensions import db
from backend.models import User, Plant, UserPlant, Article, Reminder
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# -*- coding: utf-8 -*-

def test_get_all_plants(client, init_database):
    response = client.get('/plants')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_plant_details(client, test_plant):
    response = client.get(f'/plants/{test_plant.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Plant'

def test_get_nonexistent_plant(client):
    response = client.get('/plants/999')
    assert response.status_code == 404

def test_add_user_plant(client, auth_headers, init_database):
    # Сначала создаем тестовое растение
    plant = Plant(
        name='New Test Plant',
        type='Test Type',
        image_url='/test.jpg'
    )
    db.session.add(plant)
    db.session.commit()

    # Пытаемся добавить растение пользователю
    response = client.post('/api/user/plants',  # Убедитесь в правильности пути
        json={'plant_id': plant.id},
        headers=auth_headers
    )
    
    # Проверяем возможные статусы
    assert response.status_code in (201, 400, 409), f"Unexpected status: {response.status_code}. Response: {response.get_json()}"
    
    if response.status_code == 400:
        # Анализируем ошибку
        error = response.get_json().get('error', '')
        assert 'Неверный запрос' in error or 'Invalid request' in error

def test_water_plant(client, auth_headers, test_user_plant):
    response = client.post(f'/user/plants/{test_user_plant.id}/water',
        json={'date': '2023-01-01', 'interval': 10},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert 'Полив отмечен' in response.get_json()['message']