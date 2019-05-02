import sqlite3
from singleton import Singleton


class BotDatabase(metaclass=Singleton):
    def __init__(self):
        conn = sqlite3.connect('users_data.db')
        cur = conn.cursor()
        self.create_tables(cur, conn)
        conn.close()

    def create_tables(self, cur, conn):
        cur.execute('''
                CREATE TABLE IF NOT EXISTS films_watched (
                    user_id INTEGER,
                    film_name VARCHAR(255),
                    PRIMARY KEY(user_id, film_name)
                )
                ''')
        cur.execute('''
                CREATE TABLE IF NOT EXISTS films_wished (
                    user_id INTEGER,
                    film_name VARCHAR(255), 
                    PRIMARY KEY(user_id, film_name)
                )
                ''')
        cur.execute('''
                CREATE TABLE IF NOT EXISTS users_dialogs (
                    user_id INTEGER PRIMARY KEY,
                    dialog_state VARCHAR(255)
                )
                ''')
        conn.commit()

    def add_to_wished(self, user_id, film_name):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
            INSERT INTO films_wished
            VALUES ({0}, '{1}')
                    '''.format(str(user_id), film_name))
            conn.commit()

    def add_to_watched(self, user_id, film_name, rating=None):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            query = '''
             INSERT INTO films_watched
                VALUES ({0}, '{1}', {2})
                        '''
            if rating is None:
                cur.execute(query.format(str(user_id), film_name, 'NULL'))
            else:
                cur.execute(query.format(str(user_id), film_name, str(rating)))

            conn.commit()

    def get_watched(self, user_id):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                          SELECT film_name
                          FROM films_watched
                          WHERE user_id={0}
                                  '''.format(str(user_id)))
            return cur.fetchall()

    def get_wished(self, user_id):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                          SELECT film_name
                          FROM films_wished
                          WHERE user_id={0}
                                  '''.format(str(user_id)))
            return cur.fetchall()

    def is_new_user(self, user_id):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                          SELECT *
                          FROM users_dialogs
                          WHERE user_id={0}
                          LIMIT 1
                                  '''.format(str(user_id)))
            return len(cur.fetchall()) == 0

    def set_user_dialog_state(self, user_id, dialog_state):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                       UPDATE users_dialogs
                       SET dialog_state='{0}'
                       WHERE user_id={1}
                               '''.format(str(dialog_state), str(user_id)))
            conn.commit()

    def get_user_dialog_state(self, user_id):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                          SELECT dialog_state
                          FROM users_dialogs
                          WHERE user_id={0}
                                  '''.format(str(user_id)))
            return cur.fetchone()

    def insert_new_user(self, user_id, dialog_state):
        with sqlite3.connect('users_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                          INSERT INTO users_dialogs(user_id, dialog_state)
                          VALUES ({0}, '{1}')
                                  '''.format(str(user_id), dialog_state))
            return cur.fetchone()
