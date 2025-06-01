import pytest
from backend.app import create_app
from backend.extensions import db
from backend.models import User, Plant, UserPlant, Article, Reminder
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# -*- coding: utf-8 -*-

def test_user_plant_model(app, test_user_plant):
    with app.app_context():
        assert test_user_plant.user.username == 'testuser'
        assert test_user_plant.plant.name == 'Test Plant'
        assert isinstance(test_user_plant.last_watered, datetime)

def test_plant_model(app, init_database):
    """Тест модели растения"""
    with app.app_context():
        plant = Plant.query.first()
        assert plant.name == 'Test Plant'
        assert plant.watering_interval == 7

def test_user_plant_model(app, test_user_plant):
    assert test_user_plant.user.username == 'testuser'
    assert test_user_plant.plant.name == 'Test Plant'
    assert isinstance(test_user_plant.last_watered, datetime)