#!/usr/bin/env python3
"""module constain app flask"""
from flask import (
        Flask, jsonify, make_response,
        request, abort, redirect, url_for
        )
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
        # update the user with its session_id
        response = make_response(
                jsonify({"email": email, "message": "logged in"})
                )
        response.set_cookie("session_id", value=session_id)
        return response
    # abort if credentials are incorrect
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logs out a user"""
    session_id = request.cookies.get('session_id')
    if session_id:
        # get user
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            # if user does not exist respond with 403
            abort(403)
        else:
            AUTH.destroy_session(user.id)
            # Redirect the user to the GET / route
            return redirect(url_for('user_profile'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def user_profile():
    """get user profile"""
    # get session_id form request
    session_id = request.cookies.get('session_id')
    # find user
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return make_response(jsonify({"email": user.email}), 200)
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get rest password token"""
    email = request.form.get("email")
    try:
        rest_token = AUTH.get_reset_password_token(email)
        return make_response(
                jsonify({"email": email, "reset_token": rest_token}), 200
                )
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        # update password
        AUTH.update_password(reset_token, new_password)
        return make_response(
                jsonify({"email": email, "message": "Password updated"}), 200
                )
    except ValueError:
        abort(403)


if __name__ == "__main__":
    """main function"""
    app.run(host="0.0.0.0", port="5000", debug=True)
