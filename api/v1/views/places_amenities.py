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


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def manage_place_amenity(place_id, amenity_id):
    """manage amenities"""
    place = storage.get(place_class, place_id)
    amenity = storage.get(amenity_class, amenity_id)

    if place is None:
        abort(404)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
