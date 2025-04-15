from app.models.user import T_User
from flask import Flask, redirect, url_for
from app.controllers.navigation_controller import navigation_bp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sys
from app.utils import config
from app.utils.config import DATABASE_URL

db = SQLAlchemy()
migrate = Migrate()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'default-secret')

    db.init_app(app)
    migrate.init_app(app, db)

    # импорт моделей после инициализации
    with app.app_context():
        from app.models import user, route, trip_history, traffic_data
        db.create_all()

    # подключение блюпринтов
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # Регистрируем blueprint для навигации
    app.register_blueprint(navigation_bp, url_prefix='/navigation')

    @app.route('/')
    def index():
        return redirect(url_for('navigation.show_map'))

    return app
