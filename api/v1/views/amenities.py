#!/usr/bin/python3
"""
 view for Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """list of all Amenity"""
    amenities_list = []
    if amenity_id is None:
        all_amenities = storage.all(Amenity).values()
        for value in all_amenities:
            amenities_list.append(value.to_dict())
        return jsonify(amenities_list)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a Amenity"""
    a_d = request.get_json(force=True, silent=True)
    if not a_d:
        abort(400, 'Not a JSON')
    if "name" not in a_d:
        abort(400, 'Missing name')

    n_amenity = Amenity(**amenities_data)
    n_amenity.save()
    return jsonify(n_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    a_d = request.get_json(force=True, silent=True)
    if not a_d:
        abort(400, 'Not a JSON')

    amenity.name = a_d.get("name", amenity.name)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
