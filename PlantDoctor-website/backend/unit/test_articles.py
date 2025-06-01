# -*- coding: utf-8 -*-

def test_get_all_articles(client, test_user):
    response = client.get('/articles')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_articles_for_plant(client, test_plant):
    response = client.get(f'/articles/plant/{test_plant.id}')
    assert response.status_code == 200
    assert isinstance(response.json, list)