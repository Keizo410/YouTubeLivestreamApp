import json
from flask import Blueprint, jsonify, abort
from utilities.database import Database

livestreams_bp = Blueprint('livestreams', __name__)
db = Database()

@livestreams_bp.route('/api/livestreams', methods=['GET'])
def view_livestreams():
    success, result = db.read_livestream()
    return jsonify(result), 200 if success else abort(400)

#return list of listeners of the livestrems
@livestreams_bp.route('/api/livestreams/listeners', methods=['POST'])
def view_livestream_listeners():
    success, _ = db.read_livestreamListener()
    if(success):
        return "", 200
    return abort(400)

@livestreams_bp.route('/api/livestreams/summary', methods=['GET'])
def view_livestreams_summary():
    success, result = db.read_livestream_summary()
    return jsonify(result), 200 if success else abort(400)