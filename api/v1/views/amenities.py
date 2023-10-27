#!/usr/bin/python3
"""this module handles all default RESTFul API actions for the Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/', methods=['GET'])
def get_amenities():
    """retrieves all Amenity objects"""
    dic = ([amenity.to_dict() for amenity in storage.all(Amenity).values()])
    return (jsonify(dic))


@app_views.route('/amenities/<id>', methods=['GET'])
def get_amenity(id):
    """retrieves one Amenity objects"""
    obj = storage.get(Amenity, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<id>', methods=['DELETE'])
def delete_amenity(id):
    """deletes a Amenity object"""
    obj = storage.get(Amenity, id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """create a new Amenity object"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort("Missing name")

    new = Amenity()
    new.name = request.get_json()['name']
    storage.new(new)
    storage.save()

    return (jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<id>', methods=['PUT'])
def update_amenities(id):
    """update Amenities object"""
    dic = request.get_json()
    obj = storage.get(Amenity, id)
    if obj is None:
        abort(404)
    
    if not dic:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key != "created_at" and key != "updated_at" and key != "id":
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
