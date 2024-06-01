#!/usr/bin/python3
"""API routes for reviews"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_place_reviews(place_id):
    """Returns a list of reviews of a specific place"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """Return a review by its id"""
    review = storage.get('Review', review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """Deletes a review using its id"""
    review = storage.get('Review', review_id)

    if not review:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
)
def create_review(place_id):
    """Creates a new review that is a related to a specific place"""
    from models.review import Review

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400

    if 'user_id' not in data:
        return "Missing user_id", 400

    user = storage.get('User', data['user_id'])

    if not user:
        abort(404)

    if 'text' not in data:
        return "Missing text", 400

    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return review.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    review = storage.get('Review', review_id)

    if not review:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400

    for key, value in data.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue
        setattr(review, key, value)

    review.save()

    return review.to_dict(), 200
