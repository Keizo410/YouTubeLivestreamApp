from flask import Flask
from dotenv import load_dotenv
import os
from multiprocessing import freeze_support
from flask_cors import CORS
import sys 

from routes.channels import channels_bp
from routes.emails import emails_bp
from routes.livestreams import livestreams_bp
from routes.subscriptions import subscriptions_bp
from routes.view import views_bp
from routes.youtube import youtube_bp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

app = Flask(__name__, template_folder='templates')

CORS(app)

app.register_blueprint(channels_bp)
app.register_blueprint(emails_bp)
app.register_blueprint(livestreams_bp)
app.register_blueprint(subscriptions_bp)
app.register_blueprint(views_bp)
app.register_blueprint(youtube_bp)

if __name__ == '__main__':
    freeze_support()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("FLASK_RUN_PORT", 8000)))
