import os
import random

from flask import Flask, request, render_template, redirect, abort
import logging
import datetime
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from adform import AdvertisingForm
from data import db_session
from alice.main import dialog_alice
from data.advertisings import Advertising
from data.users import User
from loginform import LoginForm
from registerform import RegisterForm

logging.basicConfig(level=logging.INFO)
sessionStorage = {}

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'bfhdjwiskoldjEFE4GUJFTYGGG5G5G65H6G565F3222JGTHGRFDJSKE;ROJELAGTRH4TF'


def main():
    db_session.global_init("db/buy_sell_db.sqlite")
    app.run(port=5055)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            city=form.city.data,
            address=form.address.data,
            hashed_password=form.password.data,
            create_date=datetime.datetime.now()
        )

        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/new_ad', methods=['GET', 'POST'])
def new_ad():
    form = AdvertisingForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        session = db_session.create_session()
        advertising = Advertising()
        advertising.title = form.title.data
        advertising.text = form.text.data
        advertising.id_category = form.id_category.data
        advertising.price = form.price.data
        advertising.vk = form.vk.data
        advertising.instagram = form.instagram.data
        advertising.site = form.site.data
        advertising.telephone = form.telephone.data
        f = form.image.data
        t = str(int(datetime.datetime.now().replace().timestamp() * 1000000 + random.randint(1, 1000)))\
            + "." + f.filename.split('.')[-1]
        f.save(os.path.join('static/img/', t))
        advertising.image = t
        advertising.create_date = datetime.datetime.now()
        advertising.id_user = current_user.id
        session.add(advertising)
        session.commit()
        return redirect('/my_advertising')
    return render_template('advertising.html', title='Создаем объявление',
                           form=form)


@app.route('/my_advertising', methods=['GET'])
def my_advertising():
    session = db_session.create_session()
    if current_user.is_authenticated:
        advertising = session.query(Advertising).filter(Advertising.id_user == current_user.id).order_by(
           Advertising.create_date.desc())
    else:
        return redirect("/login")
    return render_template("my_advertising.html", advertisings=advertising)


@app.route('/my_advertising/edit_ad/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def edit_ad(ad_id):
    if current_user.is_authenticated:
        form = AdvertisingForm()
        session = db_session.create_session()
        advertising = session.query(Advertising).filter(Advertising.id == ad_id).first()

        if advertising:
            image = advertising.image
            if request.method == "GET":
                form.title.data = advertising.title
                form.text.data = advertising.text
                form.id_category.data = advertising.id_category
                form.price.data = advertising.price
                form.vk.data = advertising.vk
                form.instagram.data = advertising.instagram
                form.site.data = advertising.site
                form.telephone.data = advertising.telephone
            else:
                print(form.validate_on_submit())
                if form.validate_on_submit():
                    advertising.title = form.title.data
                    advertising.text = form.text.data
                    advertising.id_category = form.id_category.data
                    advertising.price = form.price.data
                    advertising.vk = form.vk.data
                    advertising.instagram = form.instagram.data
                    advertising.site = form.site.data
                    advertising.telephone = form.telephone.data
                    if not form.image.data is None:
                        f = form.image.data
                        t = str(int(datetime.datetime.now().replace().timestamp() * 1000000 + random.randint(1, 1000))) \
                            + "." + f.filename.split('.')[-1]
                        f.save(os.path.join('static/img/', t))
                        advertising.image = t
                        try:
                            os.remove(os.path.abspath(os.curdir + '/static/img/' + image))
                        except Exception:
                            pass
                    session.commit()
                    print(image)

                    return redirect('/my_advertising')
        else:
            abort(404)
        return render_template('advertising.html', title='Редактирование работы', form=form, image=image)
    return redirect('/login')


@app.route('/my_advertising/delete_ad/<int:ad_id>', methods=['GET'])
@login_required
def delete_jobs(ad_id):
    if current_user.is_authenticated:
        session = db_session.create_session()
        advertising = session.query(Advertising).filter(Advertising.id == ad_id).first()
        if advertising:
            session.delete(advertising)
            session.commit()
        else:
            abort(404)
        return redirect('/my_advertising')
    return redirect('/login')


@app.route('/ad/<int:ad_id>', methods=['GET'])
def advertising_page(ad_id):
    session = db_session.create_session()
    advertising = session.query(Advertising).filter(Advertising.id == ad_id).first()
    return render_template('advertising_page.html', title='Объявление', advertising=advertising)


@app.route('/alice', methods=['POST'])
def alice():
    return dialog_alice(request)


if __name__ == '__main__':
    main()
