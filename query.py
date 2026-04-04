from igdb.wrapper import IGDBWrapper
import json 
import requests
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
# this could be modified to append limit and offset to fields so we don't have to keep spamming it
def query(endpoint, fields, limit, offset):
    fields = f'{fields} limit {limit}; offset {offset};'
    return wrapper.api_request(endpoint, fields)

def query_to_df(endpoint, fields, limit = 100, offset = 0):
    response = query(endpoint, fields, limit, offset)
    data = json.loads(response.decode("utf-8"))
    df = pd.DataFrame(data)
    return df

def df_to_feature(dataframe, feature):
    templist = dataframe[feature].to_list()
    feature = ",".join(map(str, templist))
    return feature