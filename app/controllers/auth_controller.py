from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import T_User
from app.services.auth_service import AuthService
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
            user = auth_service.register_user(username, password)
            if user:
                login_user(user)
                return redirect(url_for('navigation.show_map'))
            flash('Пользователь уже существует!', 'danger')
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")  # вот это добавь
            flash('Произошла ошибка при регистрации', 'danger')
    return render_template('auth/register.html', form=form)


# Вход
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = auth_service.login_user(username, password)
        if user:
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect(url_for('navigation.show_map'))
        flash('Неверные данные!', 'danger')
    return render_template('auth/login.html', form=form)

# Выход
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))
