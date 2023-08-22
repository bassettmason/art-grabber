import os
import pytest
from functions_framework import create_app
import main

@pytest.fixture
def client():
    os.environ["FUNCTION_TARGET"] = "get_art"
    app = create_app()
    return app.test_client()


def test_get_art(client):
    response = client.get('/')
    assert response.data == b'Hello, World!'

