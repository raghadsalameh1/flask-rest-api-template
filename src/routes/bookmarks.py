from flask import Blueprint,request,redirect
from flask.json import jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from src.constants import http_status_codes as status
from src.services import bookmark_service as bookmark_service
import validators
from flasgger import swag_from

bookmarks = Blueprint("bookmarks",__name__, url_prefix = "/api/v1/bookmarks")

@bookmarks.route('', methods = ['GET', 'POST'])
# we need to handle swagger for this kind of endpoints
@jwt_required()
def bookmarks_():
    current_user =  get_jwt_identity()
    user_id = current_user[0]
    if(request.method == 'POST'):
        body = request.json['body'] 
        url = request.json['url']

        if not validators.url(url):
            return jsonify({"error":"The provided URL is not valid"}), status.HTTP_400_BAD_REQUEST
        if bookmark_service.get(url):
            return jsonify({"error":"The provided URL is already exist"}), status.HTTP_409_CONFLICT
        bookmark = bookmark_service.add(body,url,user_id)
        if bookmark:
            return jsonify({"message":"Bookmark created successfully",
                            "Bookmark":{
                                "body":bookmark.body, 
                                "url":bookmark.url,
                                "short_url":bookmark.short_url,
                                "visits":bookmark.visits,
                                "created_at":bookmark.created_at,
                                "updated_at":bookmark.updated_at
                            } }), status.HTTP_201_CREATED
        else:
            return jsonify({"error":"Something went wrong"}), status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        page = request.args.get('page',1,type=int) # default current page is the first page
        per_page = request.args.get('per_page',5,type=int) # the default is 5 elements per page


        bookmarks = bookmark_service.get_all(user_id).paginate(page= page, per_page = per_page)
        data = []
        for bookmark in bookmarks.items:
            data.append({
                "id": bookmark.id,
                "body":bookmark.body, 
                "url":bookmark.url,
                "short_url":bookmark.short_url,
                "visits":bookmark.visits,
                "created_at":bookmark.created_at,
                "updated_at":bookmark.updated_at
            })
            
        meta = {
            'current_page': bookmarks.page,
            'total_pages': bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev,
        }
        return jsonify({"data":data, "meta":meta}), status.HTTP_200_OK

@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    user_id = current_user[0]
    bookmark = bookmark_service.get_by_id(id,user_id)
    if not bookmark:
        return jsonify({'message': 'Item not found'}), status.HTTP_404_NOT_FOUND
    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    }), status.HTTP_200_OK


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def editbookmark(id):
    current_user = get_jwt_identity()
    user_id = current_user[0]

    bookmark = bookmark_service.get_by_id(id,user_id)
    if not bookmark:
        return jsonify({'message': 'Item not found'}), status.HTTP_404_NOT_FOUND

    body = request.json['body'] 
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({"error":"The provided URL is not valid"}), status.HTTP_400_BAD_REQUEST
    
    # Check if the updated URL is not requested before
    if bookmark_service.get(url,id):
        return jsonify({"error":"The provided URL is already exist"}), status.HTTP_409_CONFLICT

    if bookmark_service.updated(id,user_id,body,url):
        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), status.HTTP_200_OK
    else:
        return jsonify({"error":"The provided URL is already exist"}), status.HTTP_400_BAD_REQUEST

@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = bookmark_service.delete(id,current_user[0])
    if not bookmark:
        return jsonify({'message': 'Item not found'}), status.HTTP_404_NOT_FOUND 
    return jsonify({}), status.HTTP_204_NO_CONTENT


@bookmarks.get('/<short_url>')
@swag_from('../docs/bookmarks/short_url.yml')
def redirect_to_url(short_url):
    bookmark = bookmark_service.get_by_shorturl(short_url)
    if bookmark:
        if bookmark_service.increment_visits(bookmark):
            return redirect(bookmark.url)
        else:
            return jsonify({ "error": "Something went wrong"}), status.HTTP_204_NO_CONTENT
    return jsonify({'message': 'Item not found'}), status.HTTP_404_NOT_FOUND 