from flask import Blueprint, request, jsonify
from ..models.models import db, User

# Create a Blueprint for authentication routes
# The url_prefix means all routes will be prefixed with /api/auth
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint - authenticates a user with username and password
    
    This is a simplified authentication without password hashing or JWT tokens
    Currently only checks if the password matches exactly what's stored in database
    
    Request body should be JSON with:
        - username: string
        - password: string
    
    Returns:
        - 200 OK with user data if authentication successful
        - 400 Bad Request if missing required fields
        - 401 Unauthorized if credentials are invalid
    """
    # Get the JSON data from the request
    data = request.get_json()
    
    # Validate that both username and password are provided
    if not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "Missing username or password"}), 400
    
    # Find the user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Simple password check without hashing - Will be updated later with proper hashing
    if not user or user.hashed_password != data['password']:
        return jsonify({"error": "Invalid username or password"}), 401
    
    # If authentication successful, return user information
    return jsonify({
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
    }), 200