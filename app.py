import os
from flask_migrate import Migrate
from src import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'development')

app.app_context().push()

migrate = Migrate(app, db)


