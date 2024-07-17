#!/usr/bin/env python3
""" basic flask app"""
from flask import Flask, jsonify, request, session, abort, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()
app.secret_key = 'my_secret_key'


@app.route("/", methods=['GET'], strict_slashes=False)
def gretting():
    """ basic route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ register a user with email and password"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return {"email": email, "message": "user created"}


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ create a new session for the user and store it as cookie"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email, "message":
                                          "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
