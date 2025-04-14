from flask import Blueprint, request, jsonify
from ..models.models import db, User
import jwt
import datetime
from flask import current_app


# Create a Blueprint for authentication routes
# The url_prefix means all routes will be prefixed with /api/auth
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or user.hashed_password != data['password']:
        return jsonify({"error": "Invalid username or password"}), 401
    
    # ✅ Generate JWT
    token = jwt.encode({
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
    }), 200