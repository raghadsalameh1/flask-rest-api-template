import os

from src import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

app.app_context().push()



