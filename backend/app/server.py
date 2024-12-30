from flask import Flask, request, abort, render_template, jsonify
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
from multiprocessing import Process, Manager, freeze_support
from emailHander import Email
from database import Database
from youtube import YouTube
from websub import WebSub
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, template_folder='../templates')

CORS(app)

@app.route('/')
def welcome():
    db.set_sql_file('./db/queries/initialize.sql')
    db.initialize_db(db.get_sql_file())
    db.set_sql_file('./db/queries/summary.sql')
    db.summerize_db_data(db.get_sql_file())
    return render_template("home.html")

@app.route('/create', methods=['GET'])
def create():
    db.set_sql_file('./db/queries/initialize.sql')
    return db.recreate_table(db.get_sql_file())

@app.route('/drop', methods=['GET'])
def drop():
    db.set_sql_file('./db/queries/drop.sql')
    return db.drop_table(db.get_sql_file())

@app.route('/add', methods=['GET'])
def add():
    db.set_sql_file('./db/queries/initialize.sql')
    return db.add_mock_table(db.get_sql_file())

@app.route('/view', methods=['GET'])
def view():
    db.set_sql_file('./db/queries/view.sql')
    message, response = db.view_table(db.get_sql_file())
    if(response==200):
        return render_template('view.html', data=message[0], columns=message[1])
    else:
        return message, response

@app.route('/send_email', methods=['GET'])
def send_email():
    csv_file_path = 'livechat_data.csv'
    email = Email()
    email.set_credentials(os.getenv("SENDER_EMAIL"), os.getenv('APP_PASSWORD'),os.getenv("RECEIVER_EMAIL"))
    email.set_draft("Test Subject", "New summary is generated.")
    db.set_sql_file('./db/queries/view.sql')
    csv_file_path = db.write_summary_to_csv(db.get_sql_file(), csv_filepath=csv_file_path)
    message, response = email.write_email(csv_file_path=csv_file_path)
    if(response == 200):
        return email.send_email()
    else:
        return message, 500

#this function is for two purposes. The first one is to request/setup pubsub subscription to designated YT channel to wait for the update.
#this is required to generate ngrok connection in websub folder. 
#The second purpose is to track the live stream for extracting the livechat. 
#since the update contains JSON from websub server, we can start transaction.
@app.route('/youtube-callback', methods=["GET", "POST"])
def youtube_callback():
    if request.method == "GET":
        hub = request.args.get("hub.challenge")
        if hub:
            return hub
        else:
            abort(400)
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/atom+xml':
            root = ET.fromstring(request.data)
            vd.value = yt.get_videoId(root)
            if yt.is_livestream(str(vd.value)):
                p = Process(target=db.process_livechat, args=(vd,))
                p.start()
                # Let the process run for a while; terminate it if needed
                p.join(timeout=60 * 60)  # Run for up to 1 hour
                if p.is_alive():
                    p.terminate()
                db.set_sql_file('./db/queries/summary.sql')
                db.summerize_db_data(db.get_sql_file())
            return '', 204
        else:
            abort(415)
    else:
        abort(405)

@app.route('/api/subscriptions', methods=['POST'])
def subscribe():
    if not request.json or 'youtuber' not in request.json:
        abort(400)
    youtuber = request.json['youtuber']
    id, status_code = yt.get_channelId(youtuber)
    status_code = websub.subscribe_to_channel(id)

    if(status_code==201):
        return jsonify({'message': f'{id} subscribed successfully'}), status_code
    else:
        return abort(403)

if __name__ == '__main__':
    freeze_support()
    manager = Manager()
    vd = manager.Value(str, "")
    websub = WebSub()
    # websub.subscribe_to_channel()
    db = Database()
    yt = YouTube()
    app.run(host='0.0.0.0', port=int(os.getenv("FLASK_RUN_PORT", 8000)))
