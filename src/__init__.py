from datetime import timedelta
from flask import Flask
import os
from src.routes.auth import auth
from src.routes.bookmarks import bookmarks
from src.error_handlers import errors
from src.models import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger,swag_from
from src.config.swagger import template, swagger_config
from src.config.config import config_by_name

def create_app(config_name):
    app = Flask(__name__,instance_relative_config=True) 
    # tells the app that configuration files are relative to the instance folder. 
    # The instance folder is located outside the flaskr package and can hold local data that shouldn’t be committed to version control, 
    # such as configuration secrets and the database file.
    app.config.from_object(config_by_name[config_name])

    
    #db.app = app
    db.init_app(app)
    create_database(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(errors)

    Swagger(app,config = swagger_config, template = template)

    return app    

# this is the first file that is executed. we delete the app file and put the startup file in 
# vs code extension as "src" so the first file that will be executed is this file.
def create_database(app):
    #db.create_all(app=app) # uncomment this line when you want to create tables in mysql db
    # db.drop_all(app=app)
    if os.getenv('FLASK_ENV') == 'development':
        if not os.path.exists('bookmarks.db'):
            db.create_all(app=app)
            print('Created Database!')
