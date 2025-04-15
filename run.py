from dotenv import load_dotenv
from app import create_app, db
from flask_migrate import Migrate, upgrade

load_dotenv()

app = create_app()
migrate = Migrate(app, db)

def run_with_migrations():
    with app.app_context():
        upgrade()

if __name__ == "__main__":
    run_with_migrations()
    app.run(host='0.0.0.0', port=5000, debug=True)
