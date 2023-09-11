import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_rss_structure(client):
    rv = client.get('/get_rss_structure')
    assert rv.status_code == 200
    # Additional assertions based on expected response structure

def test_get_articles(client):
    rv = client.get('/get_articles', query_string={'country': 'us', 'topic': 'general', 'lang': 'en'})
    assert rv.status_code == 200
    # Additional assertions based on expected response structure

def test_get_rss_articles(client):
    rv = client.get('/rss', query_string={'country': 'us', 'topic': 'general'})
    assert rv.status_code == 200
    # Additional assertions based on expected response structure