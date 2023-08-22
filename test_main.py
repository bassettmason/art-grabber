import os
import pytest
from functions_framework import create_app
import main

@pytest.fixture
def client():
    os.environ["FUNCTION_TARGET"] = "get_art"
    app = create_app()
    return app.test_client()

# def test_get_art_positive_movie(client):
#     # Assuming a known IMDb ID or Fanart ID for a movie
#     response = client.get('/get_art?type=movie&id=tt1517268')
    
#     # Check if response has a 200 status code for valid input
#     assert response.status_code == 200
#     assert "name" in response.get_json()  # Just a simple check to ensure the response contains fan art data

# def test_get_art_positive_tv(client):
#     # Assuming a known numeric TVDB ID
#     response = client.get('/get_art?type=tv&id=123456')
    
#     # Check if response has a 200 status code for valid input
#     assert response.status_code == 200
#     assert "name" in response.get_json()  # Just a simple check to ensure the response contains fan art data

def test_get_art_negative_missing_parameters(client):
    response = client.get('/get_art')
    
    # Check if response has a 400 status code for missing parameters
    assert response.status_code == 400

# def test_get_art_negative_invalid_type(client):
#     response = client.get('/get_art?type=invalid_type&id=123456')
    
#     # Check if response has a 400 status code for invalid type
#     assert response.status_code == 400

# def test_get_art_negative_invalid_id(client):
#     response = client.get('/get_art?type=movie&id=invalid_id')
    
#     # Check if response has a 400 status code for invalid ID
#     assert response.status_code == 400
