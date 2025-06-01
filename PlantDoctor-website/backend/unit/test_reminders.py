def test_create_reminder(client, auth_headers, test_user_plant):
    """Тест создания напоминания с правильным URL"""
    # Убедитесь, что URL точно соответствует маршруту (без слеша в конце)
    response = client.post('/api/reminders',
        json={
            'type': 'watering',
            'due_date': '2023-01-01T12:00:00',
            'user_plant_id': test_user_plant.id
        },
        headers=auth_headers
    )
    
    response = client.post('/api/reminders/',
        json={
            'type': 'watering',
            'due_date': '2023-01-01T12:00:00',
            'user_plant_id': test_user_plant.id
        },
        headers=auth_headers
    )
    print(f"Response status: {response.status_code}")  # Для отладки
    print(f"Response data: {response.get_json()}")     # Для отладки
    assert response.status_code == 201
    assert 'Напоминание создано' in response.get_json()['message']

def test_get_user_reminders(client, auth_headers):
    """Тест получения напоминаний с правильным URL"""
    response = client.get('/api/reminders',
        headers=auth_headers
    )
    response = client.get('/api/reminders/',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)