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

@revenue_bp.route('/industry-revenue-area-chart', methods=['GET'])
def get_industry_revenue_area_chart():
    """
    Get revenue data by industry for area chart visualization
    
    Returns data showing revenue trends for the top 4 industries across quarters
    for the specified fiscal year. This is designed for stacked area chart visualization.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
      "industry_data": [
        {
          "industry": "Financial Services",
          "data": [25000, 35000, 40000, 50000]  // Revenue for quarters 1-4
        },
        {
          "industry": "Healthcare",
          "data": [20000, 25000, 30000, 35000]
        },
        {
          "industry": "Manufacturing",
          "data": [15000, 20000, 25000, 30000]
        },
        {
          "industry": "Retail",
          "data": [10000, 15000, 18000, 22000]
        }
      ],
      "quarters": [1, 2, 3, 4],
      "year": 2024
    }
    
    Returns:
    - 200 OK with industry revenue data
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
        
        # Get area chart data by industry
        industry_data = get_industry_revenue_data(user, year)
        
        # Return formatted response
        return jsonify({
            "industry_data": industry_data,
            "quarters": [1, 2, 3, 4],
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in get_industry_revenue_area_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate industry revenue data: {str(e)}"}), 500


def get_industry_revenue_data(user, year):
    """
    Get quarterly revenue data for the top 4 industries.
    
    For directors, includes revenue for all clients managed by account executives they manage.
    For account executives, includes only revenue for their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with industry and quarterly revenue data
    """
    try:
        # First, identify the top 4 industries by total revenue
        top_industries_query = db.session.query(
            Client.industry,
            func.sum(Revenue.amount).label('total_revenue')
        ).join(
            Revenue, Client.client_id == Revenue.client_id
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
                top_industries_query = top_industries_query.filter(Client.account_executive_id.in_(ae_ids))
            else:
                # If no AEs found, return empty result
                return []
        elif user.role == 'account-executive':
            # Filter by this account executive's clients
            top_industries_query = top_industries_query.filter(Client.account_executive_id == user.user_id)
        
        # Complete the query with grouping and get top 4 by revenue
        top_industries_query = top_industries_query.group_by(
            Client.industry
        ).order_by(
            func.sum(Revenue.amount).desc()
        ).limit(4)
        
        top_industries_result = top_industries_query.all()
        
        # Extract just the industry names
        top_industries = [industry for industry, _ in top_industries_result if industry]
        
        # If we have fewer than 4 industries, or some are None, this is ok
        if len(top_industries) == 0:
            return []
        
        # Now get quarterly revenue data for each of these top industries
        industry_data = []
        
        for industry in top_industries:
            # Query revenue by quarter for this industry
            quarterly_revenue_query = db.session.query(
                Revenue.fiscal_quarter,
                func.sum(Revenue.amount).label('quarterly_revenue')
            ).join(
                Client, Revenue.client_id == Client.client_id
            ).filter(
                Revenue.fiscal_year == year,
                Client.industry == industry
            )
            
            # Apply the same role-based filtering
            if user.role == 'director':
                if ae_ids:
                    quarterly_revenue_query = quarterly_revenue_query.filter(Client.account_executive_id.in_(ae_ids))
                else:
                    continue  # Skip this industry if no AEs found
            elif user.role == 'account-executive':
                quarterly_revenue_query = quarterly_revenue_query.filter(Client.account_executive_id == user.user_id)
            
            # Complete the query with grouping
            quarterly_revenue_query = quarterly_revenue_query.group_by(
                Revenue.fiscal_quarter
            ).order_by(
                Revenue.fiscal_quarter
            )
            
            quarterly_results = quarterly_revenue_query.all()
            
            # Initialize array with zeros for all 4 quarters
            quarterly_data = [0.0, 0.0, 0.0, 0.0]
            
            # Fill in actual values from query results
            for quarter, revenue in quarterly_results:
                if 1 <= quarter <= 4:  # Ensure quarter is valid
                    quarterly_data[quarter - 1] = float(revenue) if revenue is not None else 0.0
            
            # Add to industry data
            industry_data.append({
                "industry": industry,
                "data": quarterly_data
            })
        
        return industry_data
        
    except Exception as e:
        print(f"Error in get_industry_revenue_data: {str(e)}")
        return []

@revenue_bp.route('/revenue', methods=['GET'])
def get_revenue():
    """
    Query revenue data with flexible filtering
    
    Returns revenue entries filtered by various criteria and based on user role.
    Directors can see revenue for all account executives they manage.
    Account executives can only see revenue for their clients.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    - quarters: Comma-separated list of quarters to filter by (optional)
      Example: quarters=1,2,3
    - product_categories: Comma-separated list of product categories to filter by (optional)
      Values: 'gcp-core', 'data-analytics', 'cloud-security', 'app-modernization'
      Example: product_categories=gcp-core,data-analytics
      Note: 'app-modernization' includes: mandiant, looker, apigee, maps, marketplace, vertex-ai-platform
    
    Response format:
    {
        "revenue": [
            {
                "revenue_id": 1,
                "client_name": "Acme Corp",
                "client_industry": "Financial Services",
                "account_executive": "John Smith",
                "account_executive_id": 5,
                "product_name": "Compute Engine",
                "product_category": "gcp-core",
                "fiscal_year": 2024,
                "fiscal_quarter": 1,
                "month": 2,
                "amount": 12500.00
            },
            ...
        ],
        "total_count": 42,
        "total_amount": 850000.00,
        "applied_filters": {
            "year": 2024,
            "quarters": [1, 2],
            "product_categories": ["gcp-core", "data-analytics"]
        }
    }
    
    Returns:
    - 200 OK with filtered revenue data
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if query execution fails
    """
    try:
        # Get and validate parameters
        username = request.args.get('username', type=str)
        year = request.args.get('year', 2024, type=int)
        quarters_param = request.args.get('quarters', type=str)
        product_categories_param = request.args.get('product_categories', type=str)
        
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
        
        # Parse comma-separated product categories
        product_categories = []
        valid_product_categories = ['gcp-core', 'data-analytics', 'cloud-security', 'app-modernization']
        if product_categories_param:
            product_categories = [p.strip() for p in product_categories_param.split(',') if p.strip()]
            # Validate all product categories are valid
            invalid_categories = [p for p in product_categories if p not in valid_product_categories]
            if invalid_categories:
                return jsonify({"error": f"Invalid product categories: {', '.join(invalid_categories)}. Valid values are: {', '.join(valid_product_categories)}"}), 400
        
        # Validate required parameters
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        # Get user by username and validate
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Build the query based on user role and filters
        query, applied_filters = build_revenue_query(user, year, quarters, product_categories)
        
        # Get total count for metadata
        total_count = query.count()
        
        # Calculate total amount as a separate query
        amount_query = query.with_entities(func.sum(Revenue.amount))
        total_amount = amount_query.scalar() or 0.0
        
        # Execute query and get results with pagination
        # Limit to 1000 records for performance
        results = query.order_by(
            Revenue.fiscal_year, 
            Revenue.fiscal_quarter, 
            Revenue.month
        ).limit(1000).all()
        
        # Format the results
        revenue_data = format_revenue_results(results)
        
        # Return formatted response
        return jsonify({
            "revenue": revenue_data,
            "total_count": total_count,
            "total_amount": float(total_amount),
            "applied_filters": applied_filters
        }), 200
        
    except Exception as e:
        print(f"Error in get_revenue: {str(e)}")
        return jsonify({"error": f"Failed to query revenue: {str(e)}"}), 500


def build_revenue_query(user, year, quarters, product_categories):
    """
    Build the query for revenue based on user role and filters
    
    Args:
        user: The User object
        year: The fiscal year to filter by
        quarters: List of fiscal quarters to filter by (optional)
        product_categories: List of product categories to filter by (optional)
    
    Returns:
        Tuple of (query, applied_filters)
    """
    # Start building the base query
    query = db.session.query(
        Revenue,
        Client.client_name,
        Client.industry,
        User.first_name,
        User.last_name,
        User.user_id,
        Product.product_name,
        Product.product_category
    ).join(
        Client, Revenue.client_id == Client.client_id
    ).join(
        User, Client.account_executive_id == User.user_id
    ).join(
        Product, Revenue.product_id == Product.product_id
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
    query = query.filter(Revenue.fiscal_year == year)
    
    # Apply quarters filter if provided
    if quarters:
        query = query.filter(Revenue.fiscal_quarter.in_(quarters))
        applied_filters["quarters"] = quarters
    
    # Apply product categories filter if provided
    if product_categories:
        # Prepare all product categories we need to filter by, including app-modernization subcategories
        db_product_categories = []
        for category in product_categories:
            if category == 'app-modernization':
                # Include all app-modernization subcategories
                db_product_categories.extend([
                    'looker', 'apigee', 'maps', 'marketplace', 
                    'vertex-ai-platform', 'mandiant'
                ])
            else:
                db_product_categories.append(category)
        
        # Filter by the expanded list of categories
        query = query.filter(Product.product_category.in_(db_product_categories))
        applied_filters["product_categories"] = product_categories
    
    return query, applied_filters


def format_revenue_results(results):
    """
    Format the query results into the desired output structure
    
    Args:
        results: List of tuples from the query
    
    Returns:
        List of dictionaries with revenue data
    """
    revenue_data = []
    
    for revenue, client_name, industry, ae_first_name, ae_last_name, ae_id, product_name, product_category in results:
        # For app-modernization categories, standardize the category name for display
        if product_category in ['looker', 'apigee', 'maps', 'marketplace', 'vertex-ai-platform', 'mandiant']:
            display_category = 'app-modernization'
        else:
            display_category = product_category
            
        # Format the account executive name
        account_executive = f"{ae_first_name} {ae_last_name}" if ae_first_name and ae_last_name else ""
        account_executive = account_executive.strip()
            
        revenue_data.append({
            "revenue_id": revenue.revenue_id,
            "client_name": client_name,
            "client_industry": industry,
            "account_executive": account_executive,
            "account_executive_id": ae_id,
            "product_name": product_name,
            "product_category": display_category,
            "fiscal_year": revenue.fiscal_year,
            "fiscal_quarter": revenue.fiscal_quarter,
            "month": revenue.month,
            "amount": float(revenue.amount) if revenue.amount else 0.0
        })
    
    return revenue_data