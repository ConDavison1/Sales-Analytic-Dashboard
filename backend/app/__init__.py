"""
Flask Application Package

This module serves as the entry point for the Flask application.
It implements the Application Factory pattern, which allows for:
  - Creating multiple instances of the app with different configurations
  - Easier testing
  - Cleaner initialization of extensions
  - Better separation of concerns
"""
from flask import Flask
from flask_cors import CORS
from .config import config
from .models.models import db


def create_app(config_name='default'):
    """
    Application Factory Function
    
    This function creates and configures a Flask application instance
    according to the specified configuration name.
    
    Args:
        config_name (str): The name of the configuration to use.
            Options: 'development', 'production', 'testing', 'default'
            Default is 'default' which maps to DevelopmentConfig.
    
    Returns:
        Flask: A configured Flask application instance ready to run
    """
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Load configuration from the config.py file
    # This sets up database connection, debug settings, and other app configs
    app.config.from_object(config[config_name])
    
    # Initialize Flask extensions
    
    # SQLAlchemy - Database ORM
    # This connects our models to the Flask app context
    db.init_app(app)
    
    # CORS - Cross-Origin Resource Sharing
    # This allows frontend applications from different domains to access the API
    CORS(app)
    
    # Register blueprints - Each blueprint handles a specific section of the API
    # Importing blueprints here avoids circular imports
    from .routes.auth import auth_bp             # Authentication endpoints
    # from .routes.clients import clients_bp       # Client management endpoints
    # from .routes.executives import executives_bp # Account executive management
    from .routes.pipeline import pipeline_bp     # Pipeline management endpoints
    from .routes.revenue import revenue_bp       # Revenue reporting endpoints  
    # from .routes.wins import wins_bp             # Sales wins tracking endpoints
    from .routes.signings import signings_bp     # Contract signing endpoints
    from .routes.landing import landing_bp       # Landing page endpoints
    from .routes.ai import ai_bp
    app.register_blueprint(ai_bp)  # This will expose /ai-insight

    # Add each blueprint to the application with its URL prefix
    # The URL prefixes are defined in each blueprint file
    app.register_blueprint(auth_bp)              # /api/auth/...
    # app.register_blueprint(clients_bp)           # /api/clients/...
    # app.register_blueprint(executives_bp)        # /api/executives/...
    app.register_blueprint(pipeline_bp)          # /api/pipeline/...
    app.register_blueprint(revenue_bp)           # /api/revenue/...
    # app.register_blueprint(wins_bp)              # /api/wins/...
    app.register_blueprint(signings_bp)          # /api/signings/...
    app.register_blueprint(landing_bp)           # /api/landing/...
    
    # Return the fully configured application
    return app