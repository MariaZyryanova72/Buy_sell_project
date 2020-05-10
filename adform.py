from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class AdvertisingForm(FlaskForm):
    title = StringField("Название объявления")
    vk = StringField("Ссылка на vk")
    instagram = StringField("Ссылка на instagram")
    site = StringField("Ссылка на сайт")
    telephone = StringField("Телефон для связи", validators=[DataRequired()])
    price = StringField("Цена товара")
    text = TextAreaField("Текст объявления")
    category = StringField("Категория товара")
    image = FileField("Изображение товара", validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Выбранный файл не картинка!')])
    submit = SubmitField('Опубликовать')

    def validate_telephone(self, field):
        global res
        telefon = field.data
        telefon = "".join(telefon.split(" "))
        telefon = "".join(telefon.split("\t"))
        telefon = "".join(telefon.split("\n"))
        res = ""
        start_check(telefon)
        try:
            res = int(res)
        except Exception:
            pass
        if type(res) != int:
            raise ValidationError(res)

    def validate_text(self, field):
        text = field.data
        if text == '':
            raise ValidationError(text)

    def validate_title(self, field):
        title = field.data
        if title == '':
            raise ValidationError(title)

    def validate_vk(self, field):
        title = field.data
        if title[:15] != 'https://vk.com/' and title != '':
            raise ValidationError("Проверьте ссылку,  возможно, она не верная")

    def validate_instagram(self, field):
        title = field.data
        if title[:26] != 'https://www.instagram.com/' and title != '':
            raise ValidationError("Проверьте ссылку, возможно, она не верная")

    def validate_site(self, field):
        title = field.data
        if title[:8] != 'https://' and title[:7] != 'http://' and title != '':
            raise ValidationError("Проверьте ссылку,  возможно, она не верная")


def start_check(tel):
    global flag
    if tel[:1] == "+":
        tel = tel[1:]
        if tel[:3] == "359" or tel[:2] == "55" or tel[0] == "1":
            parenthesis_check(tel)
        elif tel[0] == "7":
            flag = True
            parenthesis_check(tel)
        else:
            result_return("не определяется код страны")
    elif tel[0] == "8":
        tel = "7" + tel[1:]
        flag = True
        parenthesis_check(tel)
    else:
        result_return("неверный формат")


def parenthesis_check(tel):
    if tel.count("(") == 1 and tel.count(")") == 1 \
            or tel.count("(") == 0 and tel.count(")") == 0:
        while "(" in tel:
            tel = tel.replace("(", "")
        while ")" in tel:
            tel = tel.replace(")", "")
        dash_check(tel)
    else:
        result_return("неверный формат")


def dash_check(tel):
    if tel.find("--") != -1:
        result_return("неверный формат")
    elif tel[-1] == "-":
        result_return("неверный формат")
    else:
        while "-" in tel:
            tel = tel.replace("-", "")
        number_check(tel)


def number_check(tel):
    if len(tel) == 11:
        try:
            if tel.isdigit():
                result_return(tel)
        except ValueError:
            result_return("неверный формат")

    else:
        result_return("неверное количество цифр")


def result_return(result):
    global res
    res = result
