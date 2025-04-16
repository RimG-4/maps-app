from dotenv import load_dotenv
from app import create_app, db
from flask_migrate import Migrate, upgrade
import logging

load_dotenv()

app = create_app()

migrate = Migrate(app, db)

if not app.debug:
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('error.log')
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

def run_with_migrations():
    with app.app_context():
        upgrade()

if __name__ == "__main__":
    run_with_migrations()
    app.run(host='0.0.0.0', port=5000, debug=True)


