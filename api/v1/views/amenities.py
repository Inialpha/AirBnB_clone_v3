#!/usr/bin/python3
"""Handles all default RESTFul API actions for the Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves all Amenity objects"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves one Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ["id", "created_at", "updated_at"]
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()

    return jsonify(amenity.to_dict()), 200
