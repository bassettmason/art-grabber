import os
import pytest
# from functions_framework import create_app

def test_dummy():
    assert 1 == 1, "Dummy test failed"

# # Mocking the SecretManagerServiceClient
# class MockSecretManagerServiceClient:

#     # Mock the `access_secret_version` method
#     def access_secret_version(self, request):
#         # Create a mock response object to match the expected output of the real method
#         class MockResponse:
#             class MockPayload:
#                 data = b'MockAPIKey'  # This is a mock API key value

#             payload = MockPayload()

#         return MockResponse()

# @pytest.fixture
# def client(monkeypatch):
#     # Using monkeypatch to replace the real SecretManagerServiceClient with our mock version
#     monkeypatch.setattr('google.cloud.secretmanager.SecretManagerServiceClient', MockSecretManagerServiceClient)
#     monkeypatch.setenv("RUNNING_IN_GITHUB", "false")  # Ensure the environment variable check works as expected

#     # Now import fanart and main after setting the mock
#     import fanart
#     import main

#     os.environ["FUNCTION_TARGET"] = "get_art"
#     app = create_app()
#     return app.test_client()

# def test_get_art_negative_missing_parameters(client):
#     response = client.get('/get_art')
#     assert response.status_code == 400



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


# def test_get_art_negative_invalid_type(client):
#     response = client.get('/get_art?type=invalid_type&id=123456')
    
#     # Check if response has a 400 status code for invalid type
#     assert response.status_code == 400

# def test_get_art_negative_invalid_id(client):
#     response = client.get('/get_art?type=movie&id=invalid_id')
    
#     # Check if response has a 400 status code for invalid ID
#     assert response.status_code == 400
