#!/usr/bin/python3
"""API routes for places"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def city_places(city_id):
    """Returns a list of places of a specific City"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id):
    """Return a place by its id"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<id>", methods=["DELETE"], strict_slashes=False)
def delete_place(id):
    """Deletes a place using its id"""
    place = storage.get(Place, id)

    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Creates a new place that is a part of a specific city"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        place_data = request.get_json()
        if place_data is None:
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    if 'user_id' not in place_data:
        abort(400, "Missing user_id")

    user = storage.get(User, place_data['user_id'])

    if not user:
        abort(404)

    if 'name' not in place_data:
        abort(400, "Missing name")

    new_place = Place(**place_data)
    new_place.city_id = city_id

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    try:
        new_data = request.get_json()
        if new_data is None:
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON
    in the body of the request.

    The JSON body can contain 3 optional keys:
        states: list of State ids
        cities: list of City ids
        amenities: list of Amenity ids
    """
    from models.amenity import Amenity
    from models.state import State

    try:
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    places_list = []
    states_ids = data.get("states", [])
    cities_ids = data.get("cities", [])
    amenities_id = data.get("amenities", [])

    result = []

    for id in states_ids:
        state = storage.get(State, id)
        if not state:
            abort(404)
        for city in state.cities:
            places_list.extend(city.places)

    for id in cities_ids:
        city = storage.get(City, id)
        if not city:
            abort(404)
        if 'states' in data:
            if city.state_id in states_ids:
                continue
        places_list.extend(city.places)

    if not cities_ids and not states_ids:
        places_list = storage.all(Place).values()

    amenities_list = []

    for id in amenities_id:
        amenity_obj = storage.get(Amenity, id)
        if not amenity_obj:
            abort(404)

        amenities_list.append(amenity_obj)

    for place in places_list:
        add = True
        for amenity in amenities_list:
            if amenity not in place.amenities:
                add = False
                break
        if add:
            result.append(place)

    result = [place.to_dict() for place in result]
    return result, 200
