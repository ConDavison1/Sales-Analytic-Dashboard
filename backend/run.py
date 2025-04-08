"""
Application Entry Point

This script creates and runs the Flask application.
It serves as the entry point when running the application directly.
"""
from app import create_app
import os

# Create the Flask application with the appropriate configuration
# If FLASK_CONFIG environment variable is set, use that configuration
# Otherwise, use the default configuration (development)
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# This conditional ensures that the app only runs when this script is executed directly
# and not when imported by another module
if __name__ == '__main__':
    # Run the Flask development server
    # host='0.0.0.0' makes the server available externally
    # port=5000 is the default Flask port
    app.run(host='0.0.0.0', port=5000)