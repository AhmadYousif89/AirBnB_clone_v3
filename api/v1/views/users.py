#!/usr/bin/python3
"""API routes for users"""
from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/users", strict_slashes=False)
def users_list():
    """Returns a list of all User objects in a json representation"""
    users = storage.all('User')
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """Return a user by its id"""
    user = storage.get('User', user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user using its id"""
    user = storage.get('User', user_id)

    if not user:
        abort(404)

    user.delete()
    storage.save()

    return {}, 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a new user"""
    from models.user import User

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400

    if 'email' not in data:
        return 'Missing email', 400
    if 'password' not in data:
        return 'Missing password', 400

    user = User(**data)
    user.save()
    return user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a user"""
    user = storage.get('User', user_id)

    if not user:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)

    user.save()

    return user.to_dict(), 200
