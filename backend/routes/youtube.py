from db.models.youtuber_db import YoutuberDB
from flask import Blueprint, request, jsonify, abort
import xml.etree.ElementTree as ET
from multiprocessing import Process, Manager
from utilities.youtube import YouTube
from utilities.websub import WebSub
from utilities.database import Database

youtube_bp = Blueprint('youtube', __name__)
manager = Manager()
vd = manager.Value(str, "")
yt = YouTube()
# db = Database()
db = YoutuberDB()
websub = WebSub()

#this function is for two purposes. The first one is to request/setup pubsub subscription to designated YT channel to wait for the update.
#this is required to generate ngrok connection in websub folder. 
#The second purpose is to track the live stream for extracting the livechat. 
#since the update contains JSON from websub server, we can start transaction.
@youtube_bp.route('/youtube-callback', methods=["GET", "POST"])
def youtube_callback():
    if request.method == "GET":
        hub = request.args.get("hub.challenge")
        return hub if hub else abort(400)

    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/atom+xml':
            root = ET.fromstring(request.data)
            video_id, channel_id = yt.get_videoId(root)

            if video_id is not None and yt.is_livestream(str(video_id)):
                vd = manager.Value(str, video_id)  # Store video ID
                ch_id = manager.Value(str, channel_id)  # Store channel ID
                
                p = Process(target=db.process_livechat, args=(vd, ch_id))
                p.start()
                p.join(timeout=60 * 60)
                if p.is_alive():
                    p.terminate()
                # db.set_sql_file('db/queries/summary.sql')
                # db.summerize_db_data(db.get_sql_file())
            return '', 204
        else:
            abort(415)




