from dotenv import load_dotenv
from app import create_app, db
from flask_migrate import Migrate, upgrade
import logging
import sys
import os

# Загрузка переменных окружения
load_dotenv()

# Настройка обработки памяти
sys.setrecursionlimit(10000)
os.environ['OMP_NUM_THREADS'] = '1'  # Уменьшаем использование потоков OSMnx

app = create_app()
migrate = Migrate(app, db)

# Настройка логирования
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('error.log')
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


def run_with_migrations():
    with app.app_context():
        try:
            upgrade()
        except Exception as e:
            app.logger.error(f"Migration error: {str(e)}")
            raise


if __name__ == "__main__":
    # Применяем миграции только при явном запуске (не при hot-reload)
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        run_with_migrations()

    # Запуск приложения с оптимизацией для OSMnx
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=True,
        use_reloader=False,  # Отключаем reloader для экономии памяти
        threaded=False  # Отключаем многопоточность
    )