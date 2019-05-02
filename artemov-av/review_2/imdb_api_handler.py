import json
import requests


class ImdbApiHandler:
    url_template = 'http://www.omdbapi.com/?apikey={0}&'
    api_key = '1112cec3'

    @staticmethod
    def find_film_by_name(name):
        url = ImdbApiHandler.url_template+'t={1}'
        response = requests.get(url.format(ImdbApiHandler.api_key, name))
        return response.json()

    @staticmethod
    def find_films_by_name(name):
        url = ImdbApiHandler.url_template+'t={1}'
        response = requests.get(url.format(ImdbApiHandler.api_key, name))
        return response.json()
