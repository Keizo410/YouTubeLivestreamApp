from flask import Blueprint, abort
from utilities.database import Database

channels_bp = Blueprint('channels', __name__)
db = Database()

#return list of listeners of the channels
@channels_bp.route('/api/channels/listeners', methods=['POST'])
def view_channel_listners():
    success, _ = db.read_channelListener()
    if(success):
        return "", 200
    return abort(400)