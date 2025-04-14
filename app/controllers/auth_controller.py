from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db
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
        if auth_service.register_user(username, password):
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        flash('Username already exists!', 'danger')
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
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials!', 'danger')
    return render_template('auth/login.html', form=form)

# Выход
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
