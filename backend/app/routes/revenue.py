"""
Revenue Routes

This module defines API endpoints for the revenue functionality,
particularly revenue reporting and analysis.
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Revenue, Client, User, Product,
    DirectorAccountExecutive
)
from datetime import datetime

# Create a Blueprint for revenue routes
revenue_bp = Blueprint('revenue', __name__, url_prefix='/api/revenue')

@revenue_bp.route('/revenue-product-distribution-chart', methods=['GET'])
def get_revenue_product_distribution_chart():
    """
    Get revenue distribution data for bubble chart visualization
    
    Returns data showing revenue amounts, client count, and product categories
    over quarters for the specified fiscal year.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
      "bubble_data": [
        {
          "product_category": "gcp-core",
          "data": [
            [1, 75000, 12],  // [quarter, revenue, client_count]
            [2, 85000, 14],
            [3, 110000, 18],
            [4, 125000, 20]
          ]
        },
        {
          "product_category": "data-analytics",
          "data": [
            [1, 45000, 8],
            [2, 55000, 10],
            [3, 60000, 11],
            [4, 70000, 13]
          ]
        },
        // other product categories...
      ],
      "year": 2024
    }
    
    Returns:
    - 200 OK with bubble chart data
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if calculation fails
    """
    try:
        # Get and validate parameters
        username = request.args.get('username', type=str)
        year = request.args.get('year', 2024, type=int)
        
        # Validate required parameters
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        # Get user by username and validate
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get bubble chart data based on user role and parameters
        bubble_data = get_revenue_distribution_data(user, year)
        
        # Return formatted response
        return jsonify({
            "bubble_data": bubble_data,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in get_revenue_product_distribution_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate revenue distribution data: {str(e)}"}), 500


def get_revenue_distribution_data(user, year):
    """
    Get the revenue distribution data for bubble chart visualization.
    
    For directors, includes revenue for all clients managed by account executives they manage.
    For account executives, includes only revenue for their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with product_category and data (list of lists with quarter, revenue, client_count)
    """
    try:
        # Define standard product categories
        standard_product_categories = ["gcp-core", "data-analytics", "cloud-security"]
        
        # Define the categories that make up "app-modernization"
        app_modernization_categories = ["mandiant", "looker", "apigee", "maps", "marketplace", "vertex-ai-platform"]
        
        # All product categories including the aggregate one
        all_product_categories = standard_product_categories + ["app-modernization"]
        
        # Start building the base query
        base_query = db.session.query(
            Product.product_category,
            Revenue.fiscal_quarter,
            func.sum(Revenue.amount).label('revenue'),
            func.count(func.distinct(Revenue.client_id)).label('client_count')
        ).join(
            Product, Revenue.product_id == Product.product_id
        ).join(
            Client, Revenue.client_id == Client.client_id
        ).filter(
            Revenue.fiscal_year == year
        )
        
        # Apply role-based filtering
        if user.role == 'director':
            # Get all account executives managed by this director
            ae_relations = DirectorAccountExecutive.query.filter_by(director_id=user.user_id).all()
            ae_ids = [relation.account_executive_id for relation in ae_relations]
            
            # Filter by clients managed by these account executives
            if ae_ids:
                base_query = base_query.filter(Client.account_executive_id.in_(ae_ids))
            else:
                # If no AEs found, return empty result
                return []
        elif user.role == 'account-executive':
            # Filter by this account executive's clients
            base_query = base_query.filter(Client.account_executive_id == user.user_id)
        
        # Complete the query with grouping and execute
        results = base_query.group_by(
            Product.product_category,
            Revenue.fiscal_quarter
        ).order_by(
            Product.product_category,
            Revenue.fiscal_quarter
        ).all()
        
        # Process results to create the bubble chart data
        # We'll track app-modernization categories separately and aggregate them
        product_data = {category: [] for category in all_product_categories}
        
        for product_category, quarter, revenue, client_count in results:
            # Convert revenue and client_count to appropriate types
            revenue = float(revenue) if revenue is not None else 0.0
            client_count = int(client_count) if client_count is not None else 0
            
            # Format the data point as [quarter, revenue, client_count]
            data_point = [quarter, revenue, client_count]
            
            # Check if this belongs to app-modernization
            if product_category in app_modernization_categories:
                # Add to app-modernization aggregate
                add_or_update_data_point(product_data["app-modernization"], quarter, revenue, client_count)
            # Or if it's one of our standard categories
            elif product_category in standard_product_categories:
                product_data[product_category].append(data_point)
        
        # Create the final bubble data structure
        bubble_data = []
        for category in all_product_categories:
            # Sort data points by quarter
            category_data = sorted(product_data[category], key=lambda x: x[0])
            
            # Only include categories with data
            if category_data:
                bubble_data.append({
                    "product_category": category,
                    "data": category_data
                })
        
        return bubble_data
        
    except Exception as e:
        print(f"Error in get_revenue_distribution_data: {str(e)}")
        return []


def add_or_update_data_point(data_points, quarter, revenue, client_count):
    """
    Helper function to add or update a data point in the list.
    
    If a data point with the same quarter already exists, add the revenue and update client count.
    Otherwise, add a new data point.
    
    Args:
        data_points: List of data points [quarter, revenue, client_count]
        quarter: The quarter value to add or update
        revenue: The revenue value to add
        client_count: The client count to incorporate
    """
    # Look for an existing data point with the same quarter
    for i, point in enumerate(data_points):
        if point[0] == quarter:
            # Update existing data point
            data_points[i][1] += revenue
            
            # For client count, we need to be careful not to double-count
            # Since we don't have the actual client IDs here, we'll take the max
            # This isn't perfect but avoids potential double-counting
            data_points[i][2] = max(data_points[i][2], client_count)
            return
            
    # If no matching quarter found, add a new data point
    data_points.append([quarter, revenue, client_count])