import os
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://default_user:password@localhost/default_db")
