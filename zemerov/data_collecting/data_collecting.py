import pandas as pd
import numpy as np


class DataCollector:
    APIKEY = 'U6W7I94TRQJ77YYU'  # Уникальный номер для получения данных

    def __init(self):
        self.frame = pd.DataFrame()  # Таблица, в которой будут храниться данные

    def pull_data(self, name):
        """Принимает на вход название компании в виде идентификатора"""

        self.frame = pd.read_csv(
            'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={}&apikey={}&datatype=csv'.format(name, DataCollector.APIKEY),
        )  # Отправляем запрос

    def save_data(self, name):
        """Сохраняем данные в папке data"""

        self.frame.to_csv('data/{}.csv'.format(name))

