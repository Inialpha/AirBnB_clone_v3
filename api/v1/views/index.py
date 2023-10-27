#!/usr/bin/python3
""" connect index.py to API """


from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
