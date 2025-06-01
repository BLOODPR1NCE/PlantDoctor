import pytest
import jwt
from datetime import datetime, timedelta
from backend.auth import SECRET_KEY

# -*- coding: utf-8 -*-

def test_register(client, init_database):
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpass123'
    })
    assert response.status_code == 201
    assert 'token' in response.get_json()

def test_register_missing_data(client):
    response = client.post('/register', 
        json={'username': 'incomplete'},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400  # Ожидаем 400 Bad Request для неполных данных

def test_login(client, test_user):
    response = client.post('/login', 
        json={'email': 'test@example.com', 'password': 'testpass'},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data

def test_login_invalid_credentials(client, test_user):
    response = client.post('/login',
        json={'email': 'test@example.com', 'password': 'wrongpass'},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 401
    response_data = response.get_json()
    assert 'error' in response_data
    assert 'Неверный email или пароль' in response_data['error']

def test_profile(client, test_user):
    # Сначала получаем токен
    login_resp = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    token = login_resp.json['token']
    
    # Тестируем получение профиля
    response = client.get('/profile', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'

def test_profile_update(client, auth_headers):
    response = client.put('/profile',
        json={'username': 'updateduser'},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert 'Профиль успешно обновлен' in response.get_json()['message']