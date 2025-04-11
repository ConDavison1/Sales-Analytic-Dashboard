"""
Wins Routes

This module defines API endpoints for the wins functionality,
particularly tracking technical wins (GCP and Data Analytics).
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Win, Client, User, Product,
    DirectorAccountExecutive
)
from datetime import datetime

# Create a Blueprint for wins routes
wins_bp = Blueprint('wins', __name__, url_prefix='/api/wins')

@wins_bp.route('/win-quarterly-evolution-chart', methods=['GET'])
def get_win_quarterly_evolution_chart():
    """
    Get win count evolution by quarter for line chart visualization
    
    Returns data showing the number of wins achieved in each quarter
    for the specified fiscal year. This is designed for a line chart showing
    win progression over time.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
      "win_evolution": [
        {"quarter": 1, "win_count": 4.5},
        {"quarter": 2, "win_count": 7.0},
        {"quarter": 3, "win_count": 9.5},
        {"quarter": 4, "win_count": 12.0}
      ],
      "categories": ["Q1", "Q2", "Q3", "Q4"],
      "year": 2024
    }
    
    Returns:
    - 200 OK with quarterly win evolution data
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
        
        # Get win evolution data based on user role
        win_evolution = get_wins_evolution_data(user, year)
        
        # Create array of quarter labels for the chart
        categories = [f"Q{q}" for q in range(1, 5)]
        
        # Return formatted response
        return jsonify({
            "win_evolution": win_evolution,
            "categories": categories,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in get_win_quarterly_evolution_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate wins evolution data: {str(e)}"}), 500


def get_wins_evolution_data(user, year):
    """
    Get the wins evolution data by quarter.
    
    For directors, includes wins for all clients managed by account executives they manage.
    For account executives, includes only wins for their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with quarter and win_count values
    """
    try:
        # Start building the base query to get quarterly win counts
        query = db.session.query(
            Win.fiscal_quarter,
            func.sum(Win.win_multiplier).label('win_count')
        ).join(
            Client, Win.client_id == Client.client_id
        ).filter(
            Win.fiscal_year == year
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
                # If no AEs found, return empty result
                return []
        elif user.role == 'account-executive':
            # Filter by this account executive's clients
            query = query.filter(Client.account_executive_id == user.user_id)
        
        # Complete the query with grouping and ordering
        query = query.group_by(
            Win.fiscal_quarter
        ).order_by(
            Win.fiscal_quarter
        )
        
        # Execute query
        results = query.all()
        
        # Initialize with zeros for all quarters
        win_data = {q: 0.0 for q in range(1, 5)}
        
        # Fill in actual values from query results
        for quarter, win_count in results:
            win_data[quarter] = float(win_count) if win_count is not None else 0.0
        
        # Format into list of dictionaries
        win_evolution = [
            {"quarter": quarter, "win_count": win_count}
            for quarter, win_count in win_data.items()
        ]
        
        return win_evolution
        
    except Exception as e:
        print(f"Error in get_wins_evolution_data: {str(e)}")
        return []
    
@wins_bp.route('/win-category-quarterly-chart', methods=['GET'])
def get_win_category_quarterly_chart():
    """
    Get win counts by category and quarter for stacked bar chart visualization
    
    Returns data showing the distribution of wins across categories (GCP and DA)
    for each quarter in the specified fiscal year. This is designed for a stacked 
    bar chart visualization.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
      "win_categories": ["gcp", "da"],
      "quarters": ["Q1", "Q2", "Q3", "Q4"],
      "series": [
        {
          "name": "gcp",
          "data": [1.5, 2.0, 2.5, 3.0]  // GCP wins by quarter
        },
        {
          "name": "da",
          "data": [1.0, 1.5, 2.0, 2.5]  // DA wins by quarter
        }
      ],
      "year": 2024
    }
    
    Returns:
    - 200 OK with win category data by quarter
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
        
        # Get win category data based on user role
        series_data = get_win_category_data(user, year)
        
        # Create array of quarter labels for the chart
        quarters = [f"Q{q}" for q in range(1, 5)]
        
        # Define win categories
        win_categories = ["gcp", "da"]
        
        # Return formatted response
        return jsonify({
            "win_categories": win_categories,
            "quarters": quarters,
            "series": series_data,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in get_win_category_quarterly_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate win category data: {str(e)}"}), 500


def get_win_category_data(user, year):
    """
    Get the wins data by category and quarter.
    
    For directors, includes wins for all clients managed by account executives they manage.
    For account executives, includes only wins for their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with name and data (win counts by quarter)
    """
    try:
        # Define win categories we want to track
        win_categories = ["gcp", "da"]
        
        # Start building the base query to get wins by category and quarter
        query = db.session.query(
            Win.win_category,
            Win.fiscal_quarter,
            func.sum(Win.win_multiplier).label('win_count')
        ).join(
            Client, Win.client_id == Client.client_id
        ).filter(
            Win.fiscal_year == year,
            Win.win_category.in_(win_categories)
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
                # If no AEs found, return empty result
                return []
        elif user.role == 'account-executive':
            # Filter by this account executive's clients
            query = query.filter(Client.account_executive_id == user.user_id)
        
        # Complete the query with grouping and ordering
        query = query.group_by(
            Win.win_category,
            Win.fiscal_quarter
        ).order_by(
            Win.win_category,
            Win.fiscal_quarter
        )
        
        # Execute query
        results = query.all()
        
        # Initialize a nested dictionary to store win counts by category and quarter
        win_data = {category: {q: 0.0 for q in range(1, 5)} for category in win_categories}
        
        # Fill in actual values from query results
        for category, quarter, win_count in results:
            win_data[category][quarter] = float(win_count) if win_count is not None else 0.0
        
        # Format into list of dictionaries for the chart series
        series_data = []
        for category in win_categories:
            # Get win counts for all quarters for this category
            quarter_data = [win_data[category][q] for q in range(1, 5)]
            
            series_data.append({
                "name": category,
                "data": quarter_data
            })
        
        return series_data
        
    except Exception as e:
        print(f"Error in get_win_category_data: {str(e)}")
        return []

@wins_bp.route('/wins', methods=['GET'])
def get_wins():
    """
    Query wins data with flexible filtering
    
    Returns wins entries filtered by various criteria and based on user role.
    Directors can see wins for all account executives they manage.
    Account executives can only see wins for their clients.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    - quarters: Comma-separated list of quarters to filter by (optional)
      Example: quarters=1,2,3
    - multipliers: Comma-separated list of win multipliers to filter by (optional)
      Values: 'half', 'full'
      Example: multipliers=half,full
    - categories: Comma-separated list of win categories to filter by (optional)
      Values: 'gcp', 'da'
      Example: categories=gcp,da
    
    Response format:
    {
        "wins": [
            {
                "win_id": 1,
                "client_name": "Acme Corp",
                "client_industry": "Financial Services",
                "account_executive": "John Smith",
                "account_executive_id": 5,
                "win_category": "gcp",
                "win_level": 2,
                "win_multiplier": 1.0,
                "fiscal_year": 2024,
                "fiscal_quarter": 1
            },
            ...
        ],
        "total_count": 24,
        "total_win_count": 18.5,
        "applied_filters": {
            "year": 2024,
            "quarters": [1, 2],
            "multipliers": ["half", "full"],
            "categories": ["gcp", "da"]
        }
    }
    
    Returns:
    - 200 OK with filtered wins data
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if query execution fails
    """
    try:
        # Get and validate parameters
        username = request.args.get('username', type=str)
        year = request.args.get('year', 2024, type=int)
        quarters_param = request.args.get('quarters', type=str)
        multipliers_param = request.args.get('multipliers', type=str)
        categories_param = request.args.get('categories', type=str)
        
        # Parse comma-separated quarters
        quarters = []
        if quarters_param:
            try:
                quarters = [int(q.strip()) for q in quarters_param.split(',') if q.strip()]
                # Validate all quarters are between 1 and 4
                if not all(1 <= q <= 4 for q in quarters):
                    return jsonify({"error": "All quarters must be between 1 and 4"}), 400
            except ValueError:
                return jsonify({"error": "Invalid quarters format. Must be comma-separated integers."}), 400
        
        # Parse comma-separated multipliers
        multipliers = []
        valid_multipliers = ['half', 'full']
        if multipliers_param:
            multipliers = [m.strip().lower() for m in multipliers_param.split(',') if m.strip()]
            # Validate all multipliers are valid
            invalid_multipliers = [m for m in multipliers if m not in valid_multipliers]
            if invalid_multipliers:
                return jsonify({"error": f"Invalid multipliers: {', '.join(invalid_multipliers)}. Valid values are: {', '.join(valid_multipliers)}"}), 400
        
        # Parse comma-separated categories
        categories = []
        valid_categories = ['gcp', 'da']
        if categories_param:
            categories = [c.strip().lower() for c in categories_param.split(',') if c.strip()]
            # Validate all categories are valid
            invalid_categories = [c for c in categories if c not in valid_categories]
            if invalid_categories:
                return jsonify({"error": f"Invalid categories: {', '.join(invalid_categories)}. Valid values are: {', '.join(valid_categories)}"}), 400
        
        # Validate required parameters
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        # Get user by username and validate
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Build the query based on user role and filters
        query, applied_filters = build_wins_query(user, year, quarters, multipliers, categories)
        
        # Get total count for metadata
        total_count = query.count()
        
        # Calculate total win count (sum of win multipliers) as a separate query
        win_count_query = query.with_entities(func.sum(Win.win_multiplier))
        total_win_count = win_count_query.scalar() or 0.0
        
        # Execute query and get results with pagination
        # Limit to 1000 records for performance
        results = query.order_by(
            Win.fiscal_year, 
            Win.fiscal_quarter,
            Win.win_category,
            Win.win_level
        ).limit(1000).all()
        
        # Format the results
        wins_data = format_wins_results(results)
        
        # Return formatted response
        return jsonify({
            "wins": wins_data,
            "total_count": total_count,
            "total_win_count": float(total_win_count),
            "applied_filters": applied_filters
        }), 200
        
    except Exception as e:
        print(f"Error in get_wins: {str(e)}")
        return jsonify({"error": f"Failed to query wins: {str(e)}"}), 500


def build_wins_query(user, year, quarters, multipliers, categories):
    """
    Build the query for wins based on user role and filters
    
    Args:
        user: The User object
        year: The fiscal year to filter by
        quarters: List of fiscal quarters to filter by (optional)
        multipliers: List of win multipliers to filter by (optional)
        categories: List of win categories to filter by (optional)
    
    Returns:
        Tuple of (query, applied_filters)
    """
    # Start building the base query
    query = db.session.query(
        Win,
        Client.client_name,
        Client.industry,
        User.first_name,
        User.last_name,
        User.user_id
    ).join(
        Client, Win.client_id == Client.client_id
    ).join(
        User, Client.account_executive_id == User.user_id
    )
    
    # Initialize applied filters dictionary
    applied_filters = {"year": year}
    
    # Apply role-based filtering
    if user.role == 'director':
        # Get all account executives managed by this director
        ae_relations = DirectorAccountExecutive.query.filter_by(director_id=user.user_id).all()
        ae_ids = [relation.account_executive_id for relation in ae_relations]
        
        # Filter by clients managed by these account executives
        if ae_ids:
            query = query.filter(Client.account_executive_id.in_(ae_ids))
        else:
            # If no AEs found, return no results
            query = query.filter(False)
    elif user.role == 'account-executive':
        # Filter by this account executive's clients
        query = query.filter(Client.account_executive_id == user.user_id)
    
    # Apply year filter
    query = query.filter(Win.fiscal_year == year)
    
    # Apply quarters filter if provided
    if quarters:
        query = query.filter(Win.fiscal_quarter.in_(quarters))
        applied_filters["quarters"] = quarters
    
    # Apply multipliers filter if provided
    if multipliers:
        # Convert text multipliers to numeric values
        numeric_multipliers = []
        for multiplier in multipliers:
            if multiplier == 'half':
                numeric_multipliers.append(0.5)
            elif multiplier == 'full':
                numeric_multipliers.append(1.0)
        
        query = query.filter(Win.win_multiplier.in_(numeric_multipliers))
        applied_filters["multipliers"] = multipliers
    
    # Apply categories filter if provided
    if categories:
        query = query.filter(Win.win_category.in_(categories))
        applied_filters["categories"] = categories
    
    return query, applied_filters


def format_wins_results(results):
    """
    Format the query results into the desired output structure
    
    Args:
        results: List of tuples from the query
    
    Returns:
        List of dictionaries with wins data
    """
    wins_data = []
    
    for win, client_name, industry, ae_first_name, ae_last_name, ae_id in results:
        # Format the account executive name
        account_executive = f"{ae_first_name} {ae_last_name}" if ae_first_name and ae_last_name else ""
        account_executive = account_executive.strip()
        
        # Format multiplier label
        multiplier_label = "full" if win.win_multiplier == 1.0 else "half"
            
        wins_data.append({
            "win_id": win.win_id,
            "client_name": client_name,
            "client_industry": industry,
            "account_executive": account_executive,
            "account_executive_id": ae_id,
            "win_category": win.win_category,
            "win_level": win.win_level,
            "win_multiplier": float(win.win_multiplier) if win.win_multiplier else 0.0,
            "multiplier_type": multiplier_label,
            "fiscal_year": win.fiscal_year,
            "fiscal_quarter": win.fiscal_quarter
        })
    
    return wins_data