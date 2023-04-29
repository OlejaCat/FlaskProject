import os

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.exceptions import Unauthorized
from requests import delete, post, get, request

from data import db_session
from data.products import Products
from data.users import User
from forms.LoginForm import LoginForm
from forms.AddProductForm import AddProductForm
from forms.ClearProductForm import ClearProductForm
from forms.ProductsForm import ProductsForm
from forms.FinderForm import FinderForm
from forms.user import RegisterForm
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = '/static/images'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(Unauthorized)
def Unauthorized():
    return redirect("/login")


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/recipes")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Registration',
                                   form=form,
                                   message="Passwords")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Registration',
                                   form=form,
                                   message="There is already such a user")
        """post('http://localhost:5000/api/v2/users', json={
            'login': form.login.data,
            'email': form.email.data,
            'password': form.password.data}).json()
"""
        return redirect('/login')
    return render_template('registration.html', form=form)


add_product = []


@app.route('/recipe_finder', methods=['GET', 'POST'])
def recipe_finder():
    form = AddProductForm()
    form2 = ClearProductForm()
    if form.validate_on_submit() and form.submit.data:
        add_product.append(form.name.data)
        return render_template("recipe_finder.html",
                               form=form,
                               form2=form2,
                               add_product=add_product)
    if form2.submit.data:
        add_product.clear()
        return render_template("recipe_finder.html",
                               form=form,
                               form2=form2,
                               add_product=add_product)
    return render_template('recipe_finder.html', form=form, form2=form2, add_product=add_product)


@app.route('/products', methods=['GET', 'POST'])
def products():
    form = FinderForm()
    additional_form = ProductsForm()
    product = None

    if form.validate_on_submit() and form.submit.data:
        db_sess = db_session.create_session()
        search = form.name.data[1:]
        results = db_sess.query(Products).all()
        for element in results:
            if search in element.name:
                product = element

    return render_template('products.html', form=form, additional_form=additional_form, product=product)


def main():
    db_session.global_init("db/mars_explorer.db")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
