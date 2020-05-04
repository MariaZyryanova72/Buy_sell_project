from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class AdvertisingForm(FlaskForm):
    title = StringField("Название объявления", validators=[DataRequired()])
    vk = StringField("Ссылка на vk")
    instagram = StringField("Ссылка на instagram")
    site = StringField("Ссылка на сайт")
    telephone = StringField("Телефон для связи")
    price = StringField("Цена товара", validators=[DataRequired()])
    text = TextAreaField("Текст объявления", validators=[DataRequired()])
    id_category = IntegerField("Категория товара", validators=[DataRequired()])
    image = FileField("Изображение товара", validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Выбранный файл не картинка!')])
    submit = SubmitField('Опубликовать')


