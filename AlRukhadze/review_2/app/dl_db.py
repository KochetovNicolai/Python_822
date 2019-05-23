# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Time, Date

from app import db

# class Registration(db.Model):
#     __tablename__ = 'user'
#     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     user_name = Column(String, unique=True)
# Это могло бы стать точкой расширения: e.g., добавление регистрации пользователей


class Deadline(db.Model):
    __tablename__ = 'deadlines_list'
    d_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    d_title = db.Column(db.String(30))        # условие not null внесено для title, date и time при
    d_details = db.Column(db.String(60))      # добавлении информации
    # d_date = db.Column(db.Date)
    # d_time = db.Column(db.Time)

    # def __init__(self, title, details, date, time):
    def __init__(self, title, details):
        self.d_title = title
        self.d_details = details
        # self.d_date = date
        # self.d_time = time

    def save_deadline(self):
        db.session.add(self)        # вызов add() добавляет объект
        db.session.commit()         # завершение транзакции

    def get_deadlines(self):
        self.query.order_by(self.d_title).all()   # получаем list приближающихся дедлайнов
