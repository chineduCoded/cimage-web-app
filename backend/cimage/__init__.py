from flask import Flask, request
from flask_session import Session
from flask_cors import CORS
from config import Config
from cimage.models.engine.redis_session import RedisClient
from cimage.common.logger import configure_logger


cors = CORS()

def create_app():
    """Create app"""
    app = Flask(__name__)

    # Load configuration settings from Config class
    app.config.from_object(Config)

    # Initialize extensions
    cors = CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:3000",
        }
    })
    Session(app)

    # Configure the logger to log to a file
    configure_logger(app)

    redis_client = RedisClient(app)

    with app.app_context():
        from cimage.api.v1.views import cimage_views
        from cimage.api.v1.views import api_bp

        # Pass the redis_client object to your blueprints
        cimage_views.redis_client = redis_client
        api_bp.redis_client = redis_client

    
    # Register API blueprints
    app.register_blueprint(cimage_views)
    app.register_blueprint(api_bp)
    

    return app