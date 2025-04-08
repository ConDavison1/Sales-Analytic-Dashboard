from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import config
from .models.models import db


def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.clients import clients_bp
    from .routes.executives import executives_bp
    from .routes.pipeline import pipeline_bp
    from .routes.revenue import revenue_bp
    from .routes.count_to_wins import count_to_wins_bp
    from .routes.signings import signings_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(executives_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(revenue_bp)
    app.register_blueprint(count_to_wins_bp)
    app.register_blueprint(signings_bp)
    
    return app