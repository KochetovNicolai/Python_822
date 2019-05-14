import json
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class ImdbApiHandler:
    url = 'http://www.omdbapi.com/?'
    api_key = config['imdb_api']['key']

    @staticmethod
    def find_film_by_name(name):
        params = {'apikey':ImdbApiHandler.api_key, 't': name}
        response = requests.get(ImdbApiHandler.url, params=params)
        if str(response.status_code)[0] != '2':
            return {'Response':'False'}
        try:
            return response.json()
        except Exception:
            return {'Response':'False'}

    @staticmethod
    def find_films_by_name(name):
        params = {'apikey':ImdbApiHandler.api_key, 's': name}
        response = requests.get(ImdbApiHandler.url, params=params)
        return response.json()
