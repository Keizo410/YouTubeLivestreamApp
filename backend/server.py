# from flask import Flask
# from dotenv import load_dotenv
# import os
# from multiprocessing import freeze_support
# from flask_cors import CORS
# import sys 
# from routes.channels import channels_bp
# from routes.emails import emails_bp
# from routes.livestreams import livestreams_bp
# from routes.subscriptions import subscriptions_bp
# from routes.view import views_bp
# from routes.youtube import youtube_bp

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# load_dotenv()

# app = Flask(__name__, template_folder='templates')

# if os.getenv("FLASK_ENV")=="production":
#     CORS(app, origins="https://keizo-youtube-livestream-frontend.expo.app")
# else:
#     CORS(app)

# app.register_blueprint(channels_bp)
# app.register_blueprint(emails_bp)
# app.register_blueprint(livestreams_bp)
# app.register_blueprint(subscriptions_bp)
# app.register_blueprint(views_bp)
# app.register_blueprint(youtube_bp)

# if __name__ == '__main__':
#     freeze_support()
#     if os.getenv("FLASK_ENV")=="production":
#             app.run(debug=True, host='0.0.0.0', port=int(os.getenv("FLASK_RUN_PORT", 8000)))
#     else: 
#         app.run(debug=True, host='0.0.0.0', port=int(os.getenv("FLASK_RUN_PORT", 8000)))
from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
from routes.channels import channels_bp
from routes.emails import emails_bp
from routes.livestreams import livestreams_bp
from routes.subscriptions import subscriptions_bp
from routes.view import views_bp
from routes.youtube import youtube_bp

def load_environment_variables():
    """Load environment variables from .env file."""
    load_dotenv()

def configure_app(app):
    """Set app configurations."""
    app.config.from_mapping(
        TEMPLATE_FOLDER='templates',  
    )

def configure_cors(app):
    """Setup CORS for the app."""
    cors_origins = os.getenv("CORS_ORIGINS", "*") #add to .env
    if os.getenv("FLASK_ENV") == "production":
        CORS(app, origins=cors_origins)
    else:
        CORS(app)

def register_blueprints(app):
    """Register all blueprints for the app."""
    blueprints = [channels_bp, emails_bp, livestreams_bp, subscriptions_bp, views_bp, youtube_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, template_folder='templates')
    load_environment_variables()
    configure_app(app)
    configure_cors(app)
    register_blueprints(app)
    return app

if __name__ == '__main__':
    #(Windows-specific issue)
    from multiprocessing import freeze_support
    freeze_support()

    app = create_app()

    app_env = os.getenv("FLASK_ENV", "development")
    app_port = int(os.getenv("FLASK_RUN_PORT", 8000))

    if app_env == "production":
        app.run(debug=False, host='0.0.0.0', port=app_port)
    else:
        app.run(debug=True, host='0.0.0.0', port=app_port)
