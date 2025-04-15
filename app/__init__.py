from flask import Flask, redirect, url_for
from app.controllers.navigation_controller import navigation_bp
from flask_migrate import Migrate
import os
import sys
from app.utils import config
from app.utils.config import DATABASE_URL
from app.models import *
from app.utils.db import db
from flask_login import current_user
from flask_login import LoginManager


migrate = Migrate()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'default-secret')

    db.init_app(app)
    Migrate(app, db)

    # Регистрация блюпринтов
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(navigation_bp, url_prefix='/navigation')

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return T_User.query.get(int(user_id))

    # Роут для главной страницы
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('navigation.show_map'))
        return redirect(url_for('auth.login'))

    return app
