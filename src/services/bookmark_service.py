from src.models.Bookmark import Bookmark
from src.models import db

def get(url):
    bookmark = Bookmark.query.filter_by(url=url).first()
    return bookmark

def add(body,url,user_id):
    bookmark = Bookmark(body=body,url=url,user_id=user_id)
    try:
        db.session.add(bookmark) # add new item to database
        db.session.commit() # save the changes on database
        added_bookmark= get(url)
        return added_bookmark
    except ValueError:
        print('Error adding bookmark')
        return None

def get_all(user_id=None):
    bookmarks = []
    if(user_id is not None):
        bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    else:
        bookmarks = Bookmark.query.all()
    return bookmarks
