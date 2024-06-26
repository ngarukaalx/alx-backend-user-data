#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.debug = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth = getenv('AUTH_TYPE')
if auth == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
if auth == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if auth == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
if auth == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()


@app.before_request
def filter_request() -> None:
    """filter request before request"""
    # if auth is none do nothing
    if auth is None:
        pass
    path_auth = auth.require_auth(request.path,
                                  ['/api/v1/status/',
                                      '/api/v1/unauthorized/',
                                      '/api/v1/forbidden/',
                                      '/api/v1/auth_session/login/'])
    if path_auth:
        pass
    cookie = auth.session_cookie(request)
    header_auth = auth.authorization_header(request)
    if header_auth and cookie is None:
        abort(401)
    if path_auth and header_auth is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if path_auth and request.current_user is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """error handler for unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def fordidden(error) -> str:
    """access not allowed to a resource"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
