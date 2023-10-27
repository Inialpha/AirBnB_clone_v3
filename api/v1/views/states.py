#!/usr/bin/python3
"""this module handles all default RESTFul API actions for the State"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage

@app_views.route('/states/', methods=['GET'])
def get_states():
    """retrieves all State objects"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])
