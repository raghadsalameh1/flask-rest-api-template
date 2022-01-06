from os import access
from flask import Blueprint, request,jsonify
from flask_jwt_extended.utils import get_jwt_identity
from src.constants import http_status_codes as status
import validators
import src.services.user_service as user_service
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required


auth = Blueprint("auth",__name__, url_prefix = "/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username'] 
    email = request.json['email']
    password = request.json['password']

    if len(password)<6:
        return jsonify({"error":"Password is too short. It should be at least 6 characters"}), status.HTTP_400_BAD_REQUEST
    if len(username)<3:
        return jsonify({"error":"Username is too short. It should be at least 3 characters"}), status.HTTP_400_BAD_REQUEST
    if not username.isalnum() or " " in username:
        return jsonify({"error":"Username should contains alphabites and numbers only"}), status.HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return jsonify({"error":"Email is not valid"}), status.HTTP_400_BAD_REQUEST
    if user_service.user_email_exist(email):
        return jsonify({"error":"Email is already exist"}), status.HTTP_409_CONFLICT
    elif user_service.username_exist(username):
        return jsonify({"error":"Username is already exist"}), status.HTTP_409_CONFLICT
    else:
        hashed_password = generate_password_hash(password)
        if user_service.add(username,email,hashed_password):
            return jsonify({"message":"User created successfully",
                            "user":{
                                "username":username, "email":email
                            } }), status.HTTP_201_CREATED
        else:
            return jsonify({"error":"Something went wrong"}), status.HTTP_500_INTERNAL_SERVER_ERROR


@auth.post('/login')
def login():
    # we need to handle the DTO
    email = request.json['email']
    password = request.json['password']
    user = user_service.get(email)
    if user:
        is_password_correct = check_password_hash(user.password,password)
        if is_password_correct:
            refresh = create_refresh_token(identity= [user.id,user.email])
            access = create_access_token(identity= [user.id,user.email])
            # we need to handle the output
            return jsonify({
                "user":{
                    "access_token": access,
                    "refresh_token": refresh,
                    "username":user.username,
                    "email":user.email
            }}), status.HTTP_200_OK
    return jsonify({"error":"Eather email or password is not correct"}), status.HTTP_404_NOT_FOUND   

@auth.get('/me')
@jwt_required()
def profile():
    user = get_jwt_identity()
    user = user_service.get(user[1])
    if user:
        return jsonify({
                "user":{
                    "username":user.username,
                    "email":user.email
            }}), status.HTTP_200_OK
    return jsonify({"error":"Something went wrong"}), status.HTTP_404_NOT_FOUND

@auth.get('/refresh-token')
@jwt_required(refresh=True)
def refresh_token():
    user = get_jwt_identity()
    access = create_access_token(identity= [user[0],user[1]])
    return jsonify({"access_token": access}), status.HTTP_200_OK