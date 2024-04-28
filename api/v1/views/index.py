#!/usr/bin/python3
"""index"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User


@app_views.route("/status", strict_slashes=False)
def getStatus():
    """/status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def getStates():
    """ retrieves the number of each objects by type"""
    stat = {
            'amenities': storage.count(Amenity),
            'cities': storage.count(City),
            'places': storage.count(Place),
            'reviews': storage.count(Review),
            'states': storage.count(State),
            'users': storage.count(User),
           }
    return jsonify(stat)
