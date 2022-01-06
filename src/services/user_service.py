from src.models.User import User
from src.models import db

def add_user(username,email,hashed_password):
    new_user = User(email= email, username = username,password = hashed_password)
    try:
        db.session.add(new_user) # add new item to database
        db.session.commit() # save the changes on database
        return True
    except ValueError:
        print('Error adding user')
        return False


def user_email_exist(email):
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return True
    else:
        return False

def username_exist(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return True
    else:
        return False

def get_user(email):
    user = User.query.filter_by(email=email).first()
    return user