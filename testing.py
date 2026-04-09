from igdb.wrapper import IGDBWrapper
import json 
import requests
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")     # I added a fallback so it supports both configs without changing anything

if not os.path.exists(config_path):
    config_path = os.path.join(BASE_DIR, "testing.config.json")

with open(config_path) as config:
    config = json.load(config)
client_id = config["igdb"]["client_id"]
client_secret = config["igdb"]["client_secret"]

def get_access_token(client_id, client_secret):
    url = f"https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    return response.json()["access_token"]

token = get_access_token(client_id, client_secret)


wrapper = IGDBWrapper(client_id, token)

def query(endpoint, fields):
    return wrapper.api_request(endpoint, fields)

response_1 = query('games', 'fields name, aggregated_rating; where aggregated_rating != null; limit 100; offset 0;')
json_data = json.loads(response_1.decode("utf-8"))
game_df = pd.DataFrame(json_data)
print(game_df.to_string())

response_2 = query('genres', 'fields name; limit 10;')
json_data = json.loads(response_2.decode("utf-8"))
genre_df = pd.DataFrame(json_data)
print(genre_df.to_string())