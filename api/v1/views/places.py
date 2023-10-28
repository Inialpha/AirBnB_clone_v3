#!/usr/bin/python3
"""this module handles all default RESTFul API actions for Place"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_link_to_city(city_id):
    """retrieves all places linked to <city_id objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    dic = ([place.to_dict() for place in city.places])
    return (jsonify(dic))


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """retrieves one Place objects"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a new place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    if 'user_id' not in req:
        abort(400, "Missing user_id")
    user_id = req['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in req:
        abort(400, 'Missing name')
    req['city_id'] = city_id
    new_place = Place(**req)
    # for attr, value in req.items():
        # setattr(new_place, attr, value)
    storage.new(new_place)

    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(id):
    """update a place object"""
    dic = request.get_json()
    obj = storage.get(Place, id)
    if obj is None:
        abort(404)

    if not dic:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key not in ["created_at", "updated_at", "id", "user_id", "city_id"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
