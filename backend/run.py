"""
Application Entry Point

This script creates and runs the Flask application.
It serves as the entry point when running the application directly.
"""
from app import create_app
import os

# Create the Flask application with the appropriate configuration
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # Use port 8080 for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
