#!/usr/bin/python3
"""API routes for amenities"""
from api.v1.views import app_views
from flask import abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
def amenities_list():
    """Returns a list of all amenities in a json representation"""
    amenities = storage.all(Amenity)
    return [amenity.to_dict() for amenity in amenities.values()]


@app_views.route("/amenities/<id>", strict_slashes=False)
def get_amenity(id):
    """Returns an amenity by its id"""
    amenity = storage.get(Amenity, id)

    if not amenity:
        abort(404)

    return amenity.to_dict()


@app_views.route("/amenities/<id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(id):
    """Deletes am amenity using its id"""
    amenity = storage.get(Amenity, id)

    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    return {}, 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    try:
        amenity = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    if 'name' not in amenity:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity)

    storage.new(new_amenity)
    storage.save()

    return new_amenity.to_dict(), 201


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """Updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    try:
        new_data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()

    return amenity.to_dict(), 200
