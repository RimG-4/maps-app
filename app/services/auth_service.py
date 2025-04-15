from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import T_User
from app import db

class AuthService:

    # Регистрация нового пользователя
    def register_user(self, username, password):
        existing_user = T_User.query.filter_by(login=username).first()
        if existing_user:
            return None

        hashed_password = generate_password_hash(password)
        new_user = T_User(login=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    # Вход пользователя
    def login_user(self, username, password):
        user = T_User.query.filter_by(login=username).first()
        if not user:
            print(f"Пользователь '{username}' не найден")
            return None
        if not check_password_hash(user.password, password):
            print(f"Неверный пароль для пользователя '{username}'")
            return None
        return user

