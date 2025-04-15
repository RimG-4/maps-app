from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import T_User
from app.services.auth_service import AuthService
from app.utils.db import db
from flask import current_app
from app.forms.auth_forms import RegisterForm, LoginForm


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

# Регистрация
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            existing_user = T_User.query.filter_by(login=username).first()
            if existing_user:
                flash("Пользователь с таким логином уже существует.", "warning")
                return redirect(url_for('auth.register'))

            new_user = T_User(login=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Регистрация прошла успешно! Теперь войдите.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            current_app.logger.error("Ошибка при регистрации", exc_info=True)
            flash("Произошла ошибка при регистрации. Попробуйте снова.", "danger")
    return render_template('auth/register.html', form=form)



# Вход
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = T_User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли!', 'success')
            return redirect(url_for('navigation.map'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('auth/login.html', form=form)


# Выход
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))
