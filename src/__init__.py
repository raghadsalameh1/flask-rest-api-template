from flask import Flask
import os
from src.routes.auth import auth
from src.routes.bookmarks import bookmarks
from src.models import db
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True) 
    # tell app that we might have some configuration which is defined in the config folder
    if(test_config is None):
        app.config.from_mapping(
            SECRET_KEY= os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLAlchemy_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    
    #db.app = app
    db.init_app(app)
    create_database(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app    

# this is the first file that is executed. we delete the app file and put the startup file in 
# vs code extension as "src" so the first file that will be executed is this file.
def create_database(app):
    # db.drop_all(app=app)
    if not os.path.exists('src/bookmarks.db'):
        db.create_all(app=app)
        print('Created Database!')
