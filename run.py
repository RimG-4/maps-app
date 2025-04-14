from app import create_app
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Создаём экземпляр приложения
app = create_app()

if __name__ == "__main__":
    # Запускаем приложение в режиме отладки
    app.run(debug=True)
