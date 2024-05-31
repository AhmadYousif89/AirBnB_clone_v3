#!/usr/bin/python3
"""API routes for cities"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def state_cities(state_id):
    """Returns a list of cities of a specific state"""
    state = storage.get(State, state_id)

    if not state:
        return '', 404

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """Return a city by its id"""
    city = storage.get(City, city_id)

    if not city:
        return '', 404

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city using its id"""
    city = storage.get(City, city_id)

    if not city:
        return '', 404

    city.delete()
    storage.save()

    return {}, 200


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """Creates a new city that is a part of a specific state"""
    state = storage.get(State, state_id)

    if not state:
        return '', 404

    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400

    if 'name' not in data:
        return "Missing name", 400

    new_city = City(**data)
    new_city.state_id = state_id

    storage.new(new_city)
    storage.save()

    return new_city.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    city = storage.get(City, city_id)

    if not city:
        return '', 404

    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()

    return city.to_dict(), 200
