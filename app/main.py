from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.dishs import DishsForm
from forms.user import RegisterForm, LoginForm
from data.dishs import Dishs
from data.users import User
from data import db_session
import sqlite3


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/dishs', methods=['GET', 'POST'])
@login_required
def add_dishs():
    form = DishsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dishs = Dishs()
        dishs.title = form.title.data
        dishs.content = form.content.data
        dishs.proteins = form.proteins.data
        dishs.fats = form.fats.data
        dishs.carbohydrates = form.carbohydrates.data
        dishs.calories = form.calories.data
        dishs.is_private = form.is_private.data
        current_user.dishs.append(dishs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('dishs.html', title='Добавление блюда', form=form)


@app.route('/dishs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dishs_delete(id):
    db_sess = db_session.create_session()
    dishs = db_sess.query(Dishs).filter(Dishs.id == id, Dishs.user == current_user).first()
    if dishs:
        db_sess.delete(dishs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/dishs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dishs(id):
    form = DishsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dishs = db_sess.query(Dishs).filter(Dishs.id == id, Dishs.user == current_user).first()
        if dishs:
            form.title.data = dishs.title
            form.content.data = dishs.content
            form.is_private.data = dishs.is_private
            form.proteins.data = dishs.proteins
            form.fats.data = dishs.fats
            form.carbohydrates.data = dishs.carbohydrates
            form.calories.data = dishs.calories
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dishs = db_sess.query(Dishs).filter(Dishs.id == id, Dishs.user == current_user).first()
        if dishs:
            dishs.title = form.title.data
            dishs.content = form.content.data
            dishs.is_private = form.is_private.data
            dishs.proteins = form.proteins.data
            dishs.fats = form.fats.data
            dishs.carbohydrates = form.carbohydrates.data
            dishs.calories = form.calories.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('dishs.html', title='Редактирование блюда', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        dishs = db_sess.query(Dishs).filter((Dishs.user == current_user) | (Dishs.is_private != True))
        id = str(current_user).split(' ')[1]
        con = sqlite3.connect("db/blogs.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT allergic FROM users WHERE id = {id}""").fetchall()
        allergies = str(result)[3:-4].split(', ')
        con.close()
        for allerg in range(len(allergies)):
            allerg1 = allergies[allerg]
            dishs = dishs.filter((Dishs.content.contains(allerg1) != True))
    else:
        dishs = db_sess.query(Dishs).filter(Dishs.is_private != True)
    return render_template("index.html", dishs=dishs)



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            height=form.height.data,
            weight=form.weight.data,
            email=form.email.data,
            allergic=form.allergic.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
