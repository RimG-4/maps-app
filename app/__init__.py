from app.models.user import T_User
from app.models.user import db
from flask import Flask, redirect, url_for
from app.controllers.navigation_controller import navigation_bp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Max.40WSQL@localhost/maps'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your-secret-key'

    db.init_app(app)

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
