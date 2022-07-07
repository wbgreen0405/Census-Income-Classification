"""
Example script for querying the live API hosted on
Heroku.
"""
import os
import requests

# URL = "https://award40-udacity.herokuapp.com"
URL = "http://127.0.0.1:8000"


response = requests.post(os.path.join(URL, "model"), json={
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

print(response.status_code)
print(response.json())