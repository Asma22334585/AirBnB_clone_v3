#!/usr/bin/python3
""" new view for State objects that handles all
default RESTFul API actions"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def states(state_id=None):
    """Retrieves a State object"""
    statesList = []
    if state_id is None:
        all_objects = storage.all(State).values()
        for v in all_objects:
            statesList.append(v.to_dict())
        return jsonify(statesList)
    else:
        result = storage.get(State, state_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object"""
    objec = storage.get(State, state_id)
    if objec is None:
        abort(404)
    storage.delete(objec)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a State"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    n_state = State(**data)
    n_state.save()
    return jsonify(n_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    """Updates a State object"""
    objec = storage.get(State, state_id)
    if objec is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    objec.name = data.get("name", objec.name)
    objec.save()
    return jsonify(objec.to_dict()), 200
