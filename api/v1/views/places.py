#!/usr/bin/python3
"""this module handles all default RESTFul API actions for Place"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_linked_to_city(city_id):
    """retrieves all places linked to <city_id objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """retrieves one Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


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
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """update a place object"""
    req = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in ["created_at", "updated_at", "id", "user_id", "city_id"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """search for places based on the request JSON"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    request_data = request.get_json()

    states = request_data.get('states', [])
    cities = request_data.get('cities', [])
    amenities = request_data.get('amenities', [])

    places = []

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city not in cities:
                        cities.append(city)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    places.append(place)

    if amenities:
        amenities_objs = [storage.get(Amenity, amenity_id)
                          for amenity_id in amenities]
        places = [place for place in places if all(
                  amenity in place.amenities for amenity in amenities_objs)]

    return jsonify([place.to_dict() for place in places])
