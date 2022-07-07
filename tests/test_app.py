# pylint: disable=redefined-outer-name
"""
This file is to test the robustness of the API
"""

# from turtle import reset
import sys
import json
import pytest
from fastapi.testclient import TestClient

try:
    from main import app
except ModuleNotFoundError:
    sys.path.append('./')
    from main import app

@pytest.fixture(scope="session")
def client():
    client = TestClient(app)
    return client

def test_get(client):
    """Test standard get"""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {'message': 'Hello'}

def test_incorrect_path(client):
    """Test response for non existent path"""

    res = client.get("/some_nonexistent_url")

    assert res.status_code != 200
    assert res.json() == {"detail":"Not Found"}


def test_post_above(client):
    """Test for salary above 50K"""

    res = client.post("/model", json={
                    "age": 55,
                    "workclass": "Private",
                    "fnlgt": 77516,
                    "education": "Masters",
                    "education-num": 16,
                    "marital-status": "Never-married",
                    "occupation": "Adm-clerical",
                    "relationship": "Not-in-family",
                    "race": "White",
                    "sex": "Female",
                    "capital-gain": 10000,
                    "capital-loss": 400,
                    "hours-per-week": 45,
                    "native-country": "United-States",
            })

    assert res.status_code == 200
    assert res.json() == {'Result': '>50K'}


def test_post_below(client):
    """Test for salary below 50K"""
    res = client.post("/model", json={
                    "age": 18,
                    "workclass": "Self-emp-not-inc",
                    "fnlgt": 77516,
                    "education": "HS-grad",
                    "education-num": 2,
                    "marital-status": "Never-married",
                    "occupation": "Adm-clerical",
                    "relationship": "Not-in-family",
                    "race": "White",
                    "sex": "Female",
                    "capital-gain": 50,
                    "capital-loss": 10,
                    "hours-per-week": 30,
                    "native-country": "United-States",
            })

    assert res.status_code == 200
    assert res.json() == {'Result': '<=50K'}


def test_broken_post(client):
    res = client.post("/model", json={
                    "age": 55,
                    "workclass": "Private",
                    "fnlgt": 77516,
                    "education": "Masters",
                    "education-num": 13,
                    "marital-status": "Never-married",
                    "occupation": "Adm-clerical",
                    "relationship": "Not-in-family",
                    "race": "White",
                    "sex": "Female",
                    "capital-gain": 2174,
                    "capital-loss": 0,
                    "hours-per-week": 40,
                    # "native-country": "United-States",
            })

    assert res.status_code != 200
    assert json.loads(res.content)['detail'][0]['type'] == "value_error.missing"