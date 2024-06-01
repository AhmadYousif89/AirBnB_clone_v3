#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False
)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place Object
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False
)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects depending of the JSON
    in the body of the request.

    The JSON body can contain 3 optional keys:
        states: list of State ids
        cities: list of City ids
        amenities: list of Amenity ids
    """
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400

    places_list = []
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
