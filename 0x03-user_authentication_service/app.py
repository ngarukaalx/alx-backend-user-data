#!/usr/bin/env python3
"""module constain app flask"""
from flask import Flask, jsonify, make_response, request, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def pay_load():
    """return JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """registers a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return make_response(
                jsonify({"message": "email already registered"}),
                400
                )


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def log_in():
    """login a registerd user"""
    email = request.form.get("email")
    password = request.form.get("password")
    # check if credentials are fine
    is_valid = AUTH.valid_login(email, password)
    if is_valid:
        session_id = AUTH.create_session(email)
        response = make_response(
                jsonify({"email": email, "message": "logged in"})
                )
        response.set_cookie("session_id", value=session_id)
        return response
    # abort if credentials are incorrect
    abort(401)


if __name__ == "__main__":
    """main function"""
    app.run(host="0.0.0.0", port="5000")
