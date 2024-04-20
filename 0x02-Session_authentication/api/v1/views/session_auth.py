#!/usr/bin/env python3
"""This module handles all routes for session authectication"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """handles authectication"""
    # check if email exists
    if 'email' not in request.form:
        return make_response(jsonify({"error": "email missing"}), 400)
    # check if password exists
    if 'password' not in request.form:
        return make_response(jsonify({"error": "password missing"}), 400)
    # retrive email and password
    email = request.form.get('email')
    password = request.form.get('password')

    from models.user import User
    instance = User.search(attributes={"email": email})
    # if no user found return error msg
    if len(instance) < 1:
        return make_response(
                jsonify({"error": "no user found for this email"}),
                404
            )
    # check passwoed if its valid for the instance
    is_valid_password = instance[0].is_valid_password(password)
    if not is_valid_password:
        return make_response(jsonify({"error": "wrong password"}), 401)
    # get the user id
    user_id = instance[0].id
    # create a session id
    from api.v1.auth.session_auth import SessionAuth
    session_auth = SessionAuth()
    session_id = session_auth.create_session(user_id)

    # convert to dictionary
    dict_representation = instance[0].to_json()
    response = make_response(dict_representation)

    # get cookie name
    cookie_name = os.getenv('SESSION_NAME')
    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def dell():
    """Delete session for a user"""
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if destroyed:
        return make_response(jsonify({}), 200)
    abort(404)
