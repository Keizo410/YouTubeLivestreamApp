from db.models.listener_db import ListenerDB
from flask import Blueprint, abort,jsonify

channels_bp = Blueprint('channels', __name__)
db = ListenerDB()

#return list of listeners of the channels
@channels_bp.route('/api/channels/listeners', methods=['GET'])
def view_channel_listners():
    success, result = db.read_listeners()
    if(success):
        return jsonify(result), 200
    return jsonify({"error": "Failed to retrieve listeners"}), 400