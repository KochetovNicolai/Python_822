# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, TimeField, DateField, SelectField, FieldList
from wtforms.validators import DataRequired, Length


class DeadlineForm(FlaskForm):
    title = StringField('Title:',
                       validators=[DataRequired(message="Add a title"),
                                   Length(min=2, max=30,
                                          message='From 2 to 30 symbols')])
    details = TextAreaField('Details',
                       validators=[DataRequired(message="Add some details"),
                                   Length(min=2, max=70,
                                          message='From 2 to 70 symbols')])
    date = DateField('Date',
                       validators=[DataRequired(message="Select date")])

    time = TimeField('Time',
                       validators=[DataRequired(message="Select time")])

    # Была совершена попытка передавать форму в шаблон вместо использования html-евских 'textarea' и пр.,
    # что не решило проблему с неработающим добавлением объектов в бд
