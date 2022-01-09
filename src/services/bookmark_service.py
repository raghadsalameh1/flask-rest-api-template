from src.models.Bookmark import Bookmark
from src.models import db
from sqlalchemy import and_

def get(url,id=None):
    if id is None:
        bookmark = Bookmark.query.filter_by(url=url).first()
    else:
        bookmark = Bookmark.query.where(and_(Bookmark.url == url, Bookmark.id != id)).first()
    return bookmark

def get_by_id(id, user_id):
    bookmark = Bookmark.query.filter_by(user_id=user_id, id=id).first()
    return bookmark

def get_by_shorturl(short_url):
    bookmark = Bookmark.query.filter_by(short_url=short_url).first()
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

def updated(id,user_id,body,url):
    bookmark = get_by_id(id,user_id)
    bookmark.url = url
    bookmark.body = body
    try:
        db.session.commit() # save the changes on database
        return True
    except ValueError:
        print('Error updating bookmark')
        return False

def delete(id,user_id):
    bookmark = get_by_id(id, user_id)
    if bookmark:
        try:
           db.session.delete(bookmark)
           db.session.commit()
           return True
        except ValueError:
            print('Error deleting bookmark')
            return False
    return False

def get_all(user_id=None):
    bookmarks = []
    if(user_id is not None):
        bookmarks = Bookmark.query.filter_by(user_id=user_id)
    else:
        bookmarks = Bookmark.query
    return bookmarks

def increment_visits(bookmark):
    bookmark.visits = bookmark.visits+1
    try:
        db.session.commit()
        return True
    except ValueError:
        print('Error incrementing visits for bookmark ', bookmark.id)
        return False
