#!/usr/bin/python3
"""API routes for states"""
from api.v1.views import app_views
from flask import request, jsonify
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states_list():
    """Returns a list of all State objects in a json representation"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """Return a state by its id"""
    state = storage.get(State, state_id)

    if not state:
        return '', 404

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a state using its id"""
    state = storage.get(State, state_id)

    if not state:
        return '', 404

    state.delete()
    storage.save()

    return {}, 200


@app_views.route("/states", methods=["POST"])
def create_state():
    """Creates a new state"""
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400

    if 'name' not in data:
        return "Missing name", 400

    state = State(**data)
    state.save()
    return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a state"""
    state = storage.get(State, state_id)

    if not state:
        return '', 404

    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()

    return state.to_dict(), 200
