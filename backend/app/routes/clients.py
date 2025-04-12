"""
Clients Routes

This module defines API endpoints for the clients functionality,
particularly client management and data visualization.
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Client, User, Revenue, 
    DirectorAccountExecutive
)
from datetime import datetime

# Create a Blueprint for clients routes
clients_bp = Blueprint('clients', __name__, url_prefix='/api/clients')

@clients_bp.route('/industry-treemap-chart', methods=['GET'])
def get_industry_treemap_chart():
    """
    Get client distribution by industry for treemap chart visualization
    
    Returns data showing the number of clients and revenue for the top 10 industries by revenue,
    formatted for a treemap chart visualization. Rectangles are sized by client count.
    
    Query parameters:
    - username: Username of the current user (required)
    
    Response format:
    {
      "treemap_data": [
        {
          "x": "Financial Services",  // Industry name (used as rectangle label)
          "y": 25,                    // Client count (determines rectangle size)
          "revenue": 1250000.0,       // Total revenue for the industry (can be used for color intensity)
          "client_count": 25          // Same as y-value, included for clarity in tooltips
        },
        ...
      ]
    }
    
    Chart visualization details:
    - Each rectangle represents an industry
    - Rectangle size is proportional to the client count (y-value)
    - Revenue can be used for color intensity (higher revenue = darker color)
    - Industry name (x-value) is displayed as the rectangle label
    - Tooltips can show both client count and revenue for each industry
    - Only the top 10 industries by revenue are included
    
    Returns:
    - 200 OK with treemap chart data
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if calculation fails
    """
    try:
        # Get and validate parameters
        username = request.args.get('username', type=str)
        
        # Validate required parameters
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        # Get user by username and validate
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get client industry distribution data based on user role
        treemap_data = get_industry_distribution_data(user)
        
        # Return formatted response
        return jsonify({
            "treemap_data": treemap_data
        }), 200
        
    except Exception as e:
        print(f"Error in get_industry_treemap_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate industry distribution data: {str(e)}"}), 500


def get_industry_distribution_data(user):
    """
    Get the distribution of clients by industry with revenue and count data,
    returning only the top 10 industries by revenue.
    
    For directors, includes clients managed by all account executives they manage.
    For account executives, includes only their clients.
    
    Args:
        user: The User object
    
    Returns:
        List of dictionaries with industry, y-value, revenue, and client_count
        for the top 10 industries by revenue
    """
    try:
        # Start building the base query to get client counts and revenue by industry
        query = db.session.query(
            Client.industry,
            func.count(Client.client_id).label('client_count'),
            func.coalesce(func.sum(Revenue.amount), 0.0).label('revenue_amount')
        ).outerjoin(  # Use outer join to include clients with no revenue
            Revenue, Client.client_id == Revenue.client_id
        ).filter(
            Client.industry != None,  # Ensure industry is not null
            Client.industry != ''     # Ensure industry is not empty
        )
        
        # Apply role-based filtering
        if user.role == 'director':
            # Get all account executives managed by this director
            ae_relations = DirectorAccountExecutive.query.filter_by(director_id=user.user_id).all()
            ae_ids = [relation.account_executive_id for relation in ae_relations]
            
            # Filter by clients managed by these account executives
            if ae_ids:
                query = query.filter(Client.account_executive_id.in_(ae_ids))
            else:
                # If no AEs found, return empty list
                return []
        elif user.role == 'account-executive':
            # Filter by this account executive's clients
            query = query.filter(Client.account_executive_id == user.user_id)
        
        # Group by industry, order by revenue (descending), and limit to top 10
        query = query.group_by(Client.industry)
        query = query.order_by(func.coalesce(func.sum(Revenue.amount), 0.0).desc())
        query = query.limit(10)
        
        results = query.all()
        
        # Process results into list of dictionaries
        treemap_data = []
        for industry, client_count, revenue_amount in results:
            # Convert to appropriate types
            client_count = int(client_count) if client_count is not None else 0
            revenue_amount = float(revenue_amount) if revenue_amount is not None else 0.0
            
            treemap_data.append({
                "x": industry,
                "y": client_count,
                "revenue": revenue_amount,
                "client_count": client_count
            })
        
        return treemap_data
        
    except Exception as e:
        print(f"Error in get_industry_distribution_data: {str(e)}")
        return []