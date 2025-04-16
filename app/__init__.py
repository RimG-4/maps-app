from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
import os
import sys
from app.utils.db import db
from app.utils.config import Config
from app.models.user import T_User
from app.models.route import T_Route
from app.models.trip_history import T_TripHistory
from app.models.traffic_data import T_TrafficData
from app.controllers.navigation_controller import navigation_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.route_controller import route_bp
from app.controllers.geolocation_controller import geolocation_bp

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Настройки из config.py
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Регистрация блюпринтов
    app.register_blueprint(auth_bp)
    app.register_blueprint(navigation_bp, url_prefix='/navigation')
    app.register_blueprint(route_bp)
    app.register_blueprint(geolocation_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return T_User.query.get(int(user_id))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('navigation.show_map'))
        return redirect(url_for('auth.login'))

    return app
