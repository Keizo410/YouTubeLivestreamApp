from flask import Blueprint, request, jsonify, abort
from utilities.database import Database
from utilities.youtube import YouTube
from utilities.websub import WebSub

subscriptions_bp = Blueprint('subscriptions', __name__)

db = Database()
yt = YouTube()
websub = WebSub()

@subscriptions_bp.route('/api/subscriptions', methods=['POST'])
def subscribe():
    if not request.json or 'youtuber' not in request.json:
        abort(400)
    youtuber = request.json['youtuber']
    id, title, persons, status_code = yt.get_channelId(youtuber)
    status_code = websub.subscribe_to_channel(id)
    if status_code == 201:
        success, _ = db.create_subscription(id, title, persons)
        message = f'id: {id} & title: {title} subscribed successfully'
        return jsonify({'message': message}), status_code if success else (jsonify({'message': message + ". But database operation failed."}), status_code)
    return abort(403)

@subscriptions_bp.route('/api/subscriptions', methods=['DELETE'])
def unsubscribe():
    return "Unsubscribe functionality not implemented yet", 501

@subscriptions_bp.route('/api/subscriptions/youtubers', methods=['GET'])
def view_youtubers():
    success, result = db.read_youtuber()
    return (jsonify(result), 200) if success else abort(400)

@subscriptions_bp.route('/api/subscriptions/channels', methods=['GET'])
def view_channels():
    success, result = db.read_channel()
    return (jsonify(result), 200) if success else abort(400)
