#!/usr/bin/python3
"""API routes for places amenities"""
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage, storage_type


@app_views.route("/places/<place_id>/amenities")
def get_place_amenities(place_id):
    """Returns all amenities of a place by its id"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity from a place"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if storage_type == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)

    place.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def add_amenity_to_place(place_id, amenity_id):
    """Adds an amenity to a specific place object using its id"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return amenity.to_dict(), 200

    if storage_type == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)

    place.save()
    return jsonify(amenity.to_dict()), 201
