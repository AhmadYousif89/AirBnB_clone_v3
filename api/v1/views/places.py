#!/usr/bin/python3
"""API routes for places"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """Returns a list of places of a specific City"""
    city = storage.get('City', city_id)

    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id):
    """Return a place by its id"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<id>", methods=["DELETE"], strict_slashes=False)
def delete_place(id):
    """Deletes a place using its id"""
    place = storage.get('Place', id)

    if not place:
        abort(404)

    place.delete()
    storage.save()

    return {}, 200


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Creates a new place that is a part of a specific city"""
    from models.place import Place

    city = storage.get('City', city_id)

    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400

    if 'user_id' not in data:
        return "Missing user_id", 400

    user = storage.get('User', data['user_id'])

    if not user:
        abort(404)

    if 'name' not in data:
        return "Missing name", 400

    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return place.to_dict(), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return place.to_dict(), 200


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
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400

    states_ids = data.get("states")
    cities_ids = data.get("cities")
    amenities_ids = data.get("amenities")

    if not (states_ids or cities_ids or amenities_ids):
        places = [place.to_dict() for place in storage.all('Place').values()]
        return jsonify(places)

    list_places = []

    if states_ids:
        states = (storage.get('State', s_id) for s_id in states_ids)
        states_obj = filter(None, states)
        for state in states_obj:
            for city in state.cities:
                list_places.extend(city.places)

    if cities_ids:
        cities = (storage.get('City', c_id) for c_id in cities_ids)
        city_obj = filter(None, cities)
        for city in city_obj:
            for place in city.places:
                if place not in list_places:
                    list_places.append(place)

    if amenities_ids:
        if not list_places:
            list_places = list(storage.all('Place').values())

        amenities_obj = [
            storage.get('Amenity', a_id) for a_id in amenities_ids
        ]
        list_places = [
            place
            for place in list_places
            if all(am in place.amenities for am in amenities_obj)
        ]

    places = [p.to_dict() for p in list_places]
    for place in places:
        place.pop('amenities', None)

    return jsonify(places)
