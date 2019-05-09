import pandas as pd
import numpy as np
from urllib.parse import urlencode


class DataCollector:

    APIKEY = open('config.txt', 'r').readline()  # Уникальный номер для получения данных

    def __init(self):
        self.frame = pd.DataFrame()  # Таблица, в которой будут храниться данные

    def pull_data(self, name):
        """Принимает на вход название компании в виде идентификатора"""
        query = {'function': 'TIME_SERIES_MONTHLY', 'symbol': name, 'apikey': DataCollector.APIKEY, 'datatype': 'csv'}

        url = 'https://www.alphavantage.co/query?' + urlencode(query)

        self.frame = pd.read_csv(url)  # Отправляем запрос

    def save_data(self, name):
        """Сохраняем данные в папке data"""

        # Использовалось для дебага
        self.frame.to_csv('data/{}.csv'.format(name))

