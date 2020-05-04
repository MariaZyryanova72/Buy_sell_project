from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class AdvertisingForm(FlaskForm):
    title = StringField("Название объявления", validators=[DataRequired()])
    vk = StringField("Ссылка на vk", validators=[DataRequired()])
    instagram = StringField("Ссылка на instagram", validators=[DataRequired()])
    site = StringField("Ссылка на сайт", validators=[DataRequired()])
    telephone = StringField("Телефон для связи", validators=[DataRequired()])
    price = StringField("Цена товара", validators=[DataRequired()])
    text = TextAreaField("Текст объявления", validators=[DataRequired()])
    id_category = IntegerField("Категория товара", validators=[DataRequired()])
    #image = StringField("Изображение товара", validators=[DataRequired()])

    submit = SubmitField('Опубликовать')
