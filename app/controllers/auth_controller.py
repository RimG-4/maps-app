from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from app.models.user import T_User
from app.utils.db import db
from app.forms.auth_forms import RegisterForm, LoginForm
import logging

logging.basicConfig(level=logging.DEBUG)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            existing_user = T_User.query.filter_by(login=username).first()
            if existing_user:
                flash('Этот логин уже занят', 'error')
                return render_template('auth/register.html', form=form)

            new_user = T_User(
                login=username,
                password=generate_password_hash(password, method='scrypt')
            )

            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = T_User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли!', 'success')
            return redirect(url_for('navigation.show_map'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))