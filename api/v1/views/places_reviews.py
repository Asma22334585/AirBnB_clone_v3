#!/usr/bin/python3
"""new view for Review object that handles all
default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route("places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    reviewsList = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    for r in reviews:
        reviewsList.append(r.to_dict())
    return jsonify(reviewsList)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_review(review_id):
    """Retrieves a Review object"""
    r = storage.get(Review, review_id)
    if r is None:
        abort(404)
    return jsonify(r.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """Deletes a Review object"""
    objec = storage.get(Review, review_id)
    if objec is None:
        abort(404)
    storage.delete(objec)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    n_review = Review(place_id=place.id, **data)
    n_review.save()
    return jsonify(n_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    review.text = data.get("text", review.text)

    review.save()
    return jsonify(review.to_dict()), 200
