#!/usr/bin/python3
""" connect index.py to API """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves the number of each objects by type"""
    dic = {}

    classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}

    for cls in classes:
        dic[cls] = storage.count(classes[cls])

    return (dic)
