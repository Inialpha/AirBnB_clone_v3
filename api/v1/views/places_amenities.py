#!/usr/bin/python3
"""
Handles all default API actions for the link
between Place objects and Amenity objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity

place_class = "Place"
amenity_class = "Amenity"


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity info for a specific place"""
    place = storage.get(place_class, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    place = storage.get(place_class, place_id)
    amenity = storage.get(amenity_class, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get(place_class, place_id)
    amenity = storage.get(amenity_class, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
