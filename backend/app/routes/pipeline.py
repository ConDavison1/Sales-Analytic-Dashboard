"""
Pipeline Routes

This module defines API endpoints for the pipeline functionality,
particularly the opportunities filtering and querying.
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Opportunity, Client, User, Product, YearlyTarget, QuarterlyTarget,
    DirectorAccountExecutive
)
from datetime import datetime
from ..auth_utils import token_required
# Create a Blueprint for pipeline routes
pipeline_bp = Blueprint('pipeline', __name__, url_prefix='/api/pipeline')

@pipeline_bp.route('/opportunities', methods=['GET'])
@token_required
def get_opportunities():
    """
    Get opportunities with flexible filtering
    
    Returns opportunities filtered by various criteria and based on user role.
    Directors can see opportunities for all account executives they manage.
    Account executives can only see opportunities for their clients.
    
    Query parameters:
    - username: Username of the current user (required)
    - sales_stages: Comma-separated list of sales stages to filter by (optional)
      Values: 'qualify', 'refine', 'tech-eval/soln-dev', 'proposal/negotiation', 'migrate'
    - forecast_categories: Comma-separated list of forecast categories to filter by (optional)
      Values: 'omit', 'pipeline', 'upside', 'commit', 'closed-won'
    - product_categories: Comma-separated list of product categories to filter by (optional)
      Values: 'gcp-core', 'data-analytics', 'cloud-security', 'mandiant', 'looker', 'apigee', 'maps', 'marketplace', 'vertex-ai-platform'
    - opportunity_name: Text to search in opportunity name (optional, case-insensitive partial match)
    - limit: Maximum number of results to return (optional, default: 100)
    
    Response format:
    {
        "opportunities": [
            {
                "opportunity_id": 1,
                "opportunity_name": "GCP Migration Project",
                "client_name": "Acme Corp",
                "product_name": "Compute Engine",
                "product_category": "gcp-core",
                "forecast_category": "pipeline",
                "sales_stage": "qualify",
                "close_date": "2024-06-30",
                "probability": 25.0,
                "amount": 50000.00,
                "created_date": "2024-01-15 10:30:45"
            },
            ...
        ],
        "total_count": 45,  // Total number of matching opportunities before applying limit
        "applied_filters": {
            // Only includes filters that were actually applied
            "sales_stages": ["qualify", "refine"],
            "forecast_categories": ["pipeline", "upside"],
            "product_categories": ["gcp-core"],
            "opportunity_name": "migration"
        }
    }
    
    Returns:
    - 200 OK with filtered opportunities as described above
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if query execution fails
    """
    try:
        # Get and validate basic parameters
        params = get_validated_params()
        if 'error' in params:
            return jsonify({"error": params['error']}), params['status_code']
            
        # Build the query with appropriate joins and filters
        query = build_opportunity_query(params)
        
        # Get total count and results
        total_count = query.count()
        results = query.order_by(Opportunity.opportunity_id).limit(params['limit']).all()
        
        # Format the results
        opportunities = format_opportunity_results(results)
        
        # Return formatted response
        return jsonify({
            'opportunities': opportunities,
            'total_count': total_count,
            'applied_filters': params['applied_filters']
        }), 200
        
    except Exception as e:
        print(f"Error in get_opportunities: {str(e)}")
        return jsonify({"error": f"Failed to retrieve opportunities: {str(e)}"}), 500


def get_validated_params():
    """Extract and validate request parameters"""
    params = {}
    
    # Get required parameters
    username = request.args.get('username', type=str)
    if not username:
        return {'error': 'Missing required parameter: username', 'status_code': 400}
    
    # Get user by username and validate
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'error': 'User not found', 'status_code': 404}
    
    params['username'] = username
    params['user'] = user
    params['limit'] = request.args.get('limit', 100, type=int)
    
    # Parse filter parameters
    params.update(parse_filter_params())
    
    return params


def parse_filter_params():
    """Parse and process the filter parameters from the request"""
    filters = {}
    applied_filters = {}
    
    # Get filter parameters
    sales_stages = request.args.get('sales_stages', type=str)
    forecast_categories = request.args.get('forecast_categories', type=str)
    product_categories = request.args.get('product_categories', type=str)
    opportunity_name = request.args.get('opportunity_name', type=str)
    
    # Convert comma-separated strings to lists
    if sales_stages:
        filters['sales_stages'] = sales_stages.split(',')
        applied_filters['sales_stages'] = filters['sales_stages']
    else:
        filters['sales_stages'] = []
        
    if forecast_categories:
        filters['forecast_categories'] = forecast_categories.split(',')
        applied_filters['forecast_categories'] = filters['forecast_categories']
    else:
        filters['forecast_categories'] = []
        
    if product_categories:
        filters['product_categories'] = product_categories.split(',')
        applied_filters['product_categories'] = filters['product_categories']
    else:
        filters['product_categories'] = []
    
    if opportunity_name:
        filters['opportunity_name'] = opportunity_name
        applied_filters['opportunity_name'] = opportunity_name
    else:
        filters['opportunity_name'] = None
    
    return {'filters': filters, 'applied_filters': applied_filters}


def build_opportunity_query(params):
    """Build the query with all necessary joins and filters"""
    # Extract parameters
    user = params['user']
    filters = params['filters']
    
    # Start building the query - core table joins
    query = db.session.query(
        Opportunity,
        Client.client_name,
        Product.product_name,
        Product.product_category
    ).join(
        Client, Opportunity.client_id == Client.client_id
    ).join(
        Product, Opportunity.product_id == Product.product_id
    )
    
    # Apply role-based access control
    query = apply_role_based_filter(query, user)
    
    # Apply all other filters
    query = apply_opportunity_filters(query, filters)
    
    return query


def apply_role_based_filter(query, user):
    """Apply filters based on user role"""
    if user.role == 'director':
        # For directors: Filter by account executives under them
        query = filter_by_director(query, user.user_id)
    elif user.role == 'account-executive':
        # For account executives: Filter by their clients
        query = query.filter(Client.account_executive_id == user.user_id)
    # For admins or other roles, no additional filtering
    
    return query


def filter_by_director(query, director_id):
    """Add filters to query to only show opportunities for account executives under the director"""
    # Get all account executives managed by this director
    ae_relations = DirectorAccountExecutive.query.filter_by(director_id=director_id).all()
    ae_ids = [relation.account_executive_id for relation in ae_relations]
    
    # Filter by clients managed by these account executives
    if ae_ids:
        query = query.filter(Client.account_executive_id.in_(ae_ids))
    else:
        # If no AEs found, return no results
        query = query.filter(False)
    
    return query


def apply_opportunity_filters(query, filters):
    """Apply all the opportunity filters to the query"""
    # Apply sales stage filter if provided
    if filters['sales_stages']:
        query = query.filter(Opportunity.sales_stage.in_(filters['sales_stages']))
    
    # Apply forecast category filter if provided
    if filters['forecast_categories']:
        query = query.filter(Opportunity.forecast_category.in_(filters['forecast_categories']))
    
    # Apply product category filter if provided
    if filters['product_categories']:
        query = query.filter(Product.product_category.in_(filters['product_categories']))
    
    # Apply opportunity name filter if provided
    if filters['opportunity_name']:
        query = query.filter(Opportunity.opportunity_name.ilike(f'%{filters["opportunity_name"]}%'))
    
    return query


def format_opportunity_results(results):
    """Format the query results into the desired output structure"""
    opportunities = []
    
    for opp, client_name, product_name, product_category in results:
        opportunities.append({
            'opportunity_id': opp.opportunity_id,
            'opportunity_name': opp.opportunity_name,
            'client_name': client_name,
            'product_name': product_name,
            'product_category': product_category,
            'forecast_category': opp.forecast_category,
            'sales_stage': opp.sales_stage,
            'close_date': opp.close_date.strftime('%Y-%m-%d') if opp.close_date else None,
            'probability': float(opp.probability) if opp.probability else None,
            'amount': float(opp.amount) if opp.amount else None,
            'created_date': opp.created_date.strftime('%Y-%m-%d %H:%M:%S') if opp.created_date else None
        })
    
    return opportunities

@pipeline_bp.route('/pipeline-quarterly-targets', methods=['GET'])
@token_required
def get_pipeline_quarterly_targets():
    """
    Get quarterly accumulated weighted pipeline values and target achievement percentages
    
    For each quarter, calculates the accumulated weighted opportunity values and the percentage
    of the quarterly target achieved. Only considers opportunities not in 'omit' or 'closed-won' categories.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
        "quarterly_targets": [
            {
                "quarter": 1,
                "accumulated_value": 12500.0,   // Accumulated weighted value through Q1
                "achievement_percentage": 50.0   // Percentage of Q1 target achieved
            },
            {
                "quarter": 2,
                "accumulated_value": 25000.0,   // Accumulated weighted value through Q2
                "achievement_percentage": 50.0   // Percentage of Q2 target achieved
            },
            {
                "quarter": 3,
                "accumulated_value": 37500.0,   // Accumulated weighted value through Q3
                "achievement_percentage": 50.0   // Percentage of Q3 target achieved
            },
            {
                "quarter": 4,
                "accumulated_value": 50000.0,   // Accumulated weighted value through Q4
                "achievement_percentage": 50.0   // Percentage of Q4 target achieved
            }
        ],
        "year": 2024,
        "quarterly_percentages": [25.0, 25.0, 25.0, 25.0]  // Target percentages by quarter
    }
    
    Returns:
    - 200 OK with quarterly target data
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
        
        # Get all relevant opportunities
        opportunities = get_user_opportunities(user, year)
        
        # Get the user's quarterly target percentages
        quarterly_percentages = get_user_targets(user.user_id, year)
        
        # Get the yearly target amount
        yearly_target_amount = get_yearly_target_amount(user, year)
        
        # Calculate the quarterly accumulated values
        quarterly_targets = calculate_quarterly_targets(opportunities, quarterly_percentages, yearly_target_amount)
        
        # Return response
        return jsonify({
            "quarterly_targets": quarterly_targets,
            "year": year,
            "quarterly_percentages": quarterly_percentages
        }), 200
        
    except Exception as e:
        print(f"Error in pipeline quarterly targets: {str(e)}")
        return jsonify({"error": f"Failed to calculate quarterly targets: {str(e)}"}), 500


def get_yearly_target_amount(user, year):
    """
    Get the yearly target amount for a user.
    
    For directors, it's the sum of targets for account executives under them.
    For account executives, it's their own target amount.
    
    Args:
        user: The User object
        year: The fiscal year
    
    Returns:
        The yearly target amount as a float
    """
    if user.role == 'director':
        # Calculate yearly target as sum of AE targets
        yearly_amount = 0.0
        
        # Get all account executives managed by this director
        ae_relations = DirectorAccountExecutive.query.filter_by(director_id=user.user_id).all()
        ae_ids = [relation.account_executive_id for relation in ae_relations]
        
        # For each AE, get their yearly signing target and add to total
        if ae_ids:
            ae_targets = YearlyTarget.query.filter(
                YearlyTarget.user_id.in_(ae_ids),
                YearlyTarget.fiscal_year == year,
                YearlyTarget.target_type == 'signings'
            ).all()
            
            for target in ae_targets:
                if target.amount is not None:
                    yearly_amount += float(target.amount)
                    
        return yearly_amount
    else:
        # For account executives, get their own yearly target
        yearly_target = YearlyTarget.query.filter_by(
            user_id=user.user_id,
            fiscal_year=year,
            target_type='signings'
        ).first()
        
        if yearly_target and yearly_target.amount is not None:
            return float(yearly_target.amount)
        else:
            return 0.0
        

def get_user_opportunities(user, year):
    """
    Get all relevant opportunities for a user in the specified year,
    excluding those in the 'omit' and 'closed-won' forecast categories.
    
    For directors, gets opportunities from all account executives they manage.
    For account executives, gets only their opportunities.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with opportunity data
    """
    # Start building the query to get opportunities
    query = db.session.query(
        Opportunity
    ).join(
        Client, Opportunity.client_id == Client.client_id
    ).filter(
        Opportunity.forecast_category != 'omit',
        Opportunity.forecast_category != 'closed-won',
        extract('year', Opportunity.created_date) == year
    )
    
    # Apply role-based filtering
    if user.role == 'director':
        # Get all account executives under this director
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
    
    # Execute query
    results = query.all()
    
    # Process results into list of dictionaries
    opportunities = []
    for opp in results:
        # Calculate duration in years (assume 1 year if no close date or close date is same as created date)
        duration_years = 1.0
        if opp.close_date and opp.created_date:
            # Calculate difference in days and convert to years
            delta = opp.close_date - opp.created_date.date()
            days = delta.days
            if days > 0:
                duration_years = days / 365.25  # Account for leap years
        
        # Convert Decimal values to float to avoid type errors
        amount = float(opp.amount) if opp.amount is not None else 0.0
        probability = float(opp.probability) if opp.probability is not None else 0.0
        
        # Calculate weighted value (amount * probability / 100)
        weighted_value = (amount * probability / 100.0)
        
        # Calculate annual weighted value
        annual_weighted_value = weighted_value / max(duration_years, 1.0)
        
        opportunities.append({
            'opportunity_id': opp.opportunity_id,
            'annual_weighted_value': annual_weighted_value
        })
    
    return opportunities


def get_user_targets(user_id, year):
    """
    Get a user's quarterly target percentages.
    
    For directors, uses fixed percentages [10.0, 20.0, 25.0, 45.0].
    For account executives, retrieves from database or uses defaults.
    
    Args:
        user_id: The user's ID
        year: The fiscal year
    
    Returns:
        List of percentages for each quarter [q1_percentage, q2_percentage, q3_percentage, q4_percentage]
    """
    # Get the user to check their role
    user = User.query.filter_by(user_id=user_id).first()
    
    # For directors: use fixed percentages
    if user and user.role == 'director':
        return [10.0, 20.0, 25.0, 45.0]
    
    # For account executives and other roles:
    # Initialize with default values
    quarterly_percentages = [10.0, 20.0, 25.0, 45.0]
    
    # Try to get quarterly targets from database
    for quarter in range(1, 5):
        quarterly_target = QuarterlyTarget.query.filter_by(
            user_id=user_id,
            fiscal_quarter=quarter
        ).first()
        
        if quarterly_target and quarterly_target.percentage is not None:
            # Convert from Decimal to float
            quarterly_percentages[quarter - 1] = float(quarterly_target.percentage)
    
    return quarterly_percentages



def calculate_quarterly_targets(opportunities, quarterly_percentages, yearly_target_amount):
    """
    Calculate quarterly accumulated values and achievement percentages.
    
    Args:
        opportunities: List of dictionaries with opportunity data
        quarterly_percentages: List of percentages for each quarter
        yearly_target_amount: The yearly signing target amount for the user
    
    Returns:
        List of dictionaries with quarter, accumulated_value, and achievement_percentage
    """
    # Calculate total annual weighted value from all opportunities
    total_accumulated_value = sum(opp['annual_weighted_value'] for opp in opportunities)
    
    # Calculate quarterly targets
    quarterly_targets = []
    
    for quarter in range(1, 5):
        # Calculate accumulated value for this quarter based on proportion of year
        accumulated_value = total_accumulated_value * (quarter / 4.0)
        
        # Get the quarterly target percentage for this quarter
        quarter_percentage = quarterly_percentages[quarter-1]
        
        # Calculate the absolute target for this quarter from the yearly target amount
        absolute_target = yearly_target_amount * (quarter_percentage / 100.0)
        
        # Calculate achievement percentage (avoid division by zero)
        achievement_percentage = 0.0
        if absolute_target > 0:
            achievement_percentage = (accumulated_value / absolute_target) * 100.0
        
        quarterly_targets.append({
            "quarter": quarter,
            "accumulated_value": round(accumulated_value, 2),
            "achievement_percentage": round(achievement_percentage, 1)
        })
    
    return quarterly_targets

@pipeline_bp.route('/stage-funnel-chart-data', methods=['GET'])
@token_required
def get_stage_funnel_chart_data():
    """
    Get opportunity count by sales stage for funnel chart visualization
    
    Returns the count of opportunities at each sales stage for the specified year.
    Only includes opportunities that are not in the 'omit' forecast category.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
        "stage_funnel_data": [
            {"stage": "qualify", "count": 25},
            {"stage": "refine", "count": 18},
            {"stage": "tech-eval/soln-dev", "count": 12},
            {"stage": "proposal/negotiation", "count": 8},
            {"stage": "migrate", "count": 4}
        ],
        "year": 2024
    }
    
    Returns:
    - 200 OK with stage funnel data
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
        
        # Get stage funnel data based on user role
        stage_funnel_data = get_stage_funnel_data(user, year)
        
        # Return response
        return jsonify({
            "stage_funnel_data": stage_funnel_data,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in stage funnel chart data: {str(e)}")
        return jsonify({"error": f"Failed to calculate stage funnel data: {str(e)}"}), 500


def get_stage_funnel_data(user, year):
    """
    Get the count of opportunities at each sales stage.
    
    For directors, counts opportunities for all clients managed by account executives they manage.
    For account executives, counts opportunities for only their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with stage and count
    """
    # Define the stages in the correct order for the funnel
    stages = [
        "qualify", 
        "refine", 
        "tech-eval/soln-dev", 
        "proposal/negotiation", 
        "migrate"
    ]
    
    # Start building the base query to count opportunities by stage
    base_query = db.session.query(
        Opportunity.sales_stage,
        func.count(Opportunity.opportunity_id).label('count')
    ).join(
        Client, Opportunity.client_id == Client.client_id
    ).filter(
        Opportunity.forecast_category != 'omit',
        extract('year', Opportunity.created_date) == year
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
            # If no AEs found, return empty result with zero counts
            return [{"stage": stage, "count": 0} for stage in stages]
    elif user.role == 'account-executive':
        # Filter by this account executive's clients
        base_query = base_query.filter(Client.account_executive_id == user.user_id)
    
    # Complete the query with grouping and execute
    results = base_query.group_by(Opportunity.sales_stage).all()
    
    # Convert results to a dictionary for easier lookup
    stage_counts = {stage: 0 for stage in stages}
    for stage, count in results:
        if stage in stage_counts:  # Only include valid stages
            stage_counts[stage] = count
    
    # Format into the expected response structure, maintaining stage order
    stage_funnel_data = [
        {"stage": stage, "count": count}
        for stage, count in stage_counts.items()
    ]
    
    return stage_funnel_data

@pipeline_bp.route('/product-forecast-heatmap-chart-data', methods=['GET'])
@token_required
def get_product_forecast_heatmap_data():
    """
    Get weighted opportunity values across product categories and forecast categories
    
    Returns data for a heatmap visualization showing the weighted opportunity values
    (amount × probability/100) for each combination of product category and forecast category.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
        "heatmap_data": [
            {"product_category": "gcp-core", "forecast_category": "pipeline", "value": 250000.0, "count": 12},
            {"product_category": "gcp-core", "forecast_category": "upside", "value": 180000.0, "count": 8},
            {"product_category": "data-analytics", "forecast_category": "commit", "value": 300000.0, "count": 5},
            ...
        ],
        "year": 2024
    }
    
    Returns:
    - 200 OK with heatmap data
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
        
        # Get heatmap data based on user role
        heatmap_data = get_product_forecast_heatmap_data(user, year)
        
        # Return response
        return jsonify({
            "heatmap_data": heatmap_data,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in product forecast heatmap data: {str(e)}")
        return jsonify({"error": f"Failed to calculate product forecast heatmap data: {str(e)}"}), 500


def get_product_forecast_heatmap_data(user, year):
    """
    Get weighted opportunity values for each combination of product category and forecast category.
    
    For directors, includes opportunities for all clients managed by account executives they manage.
    For account executives, includes only opportunities for their clients.
    
    App-modernization is an aggregate category that includes:
    mandiant, looker, apigee, maps, marketplace, and vertex-ai-platform.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with product_category, forecast_category, value, and count
    """
    # Define the product categories we want to track
    # Note: app-modernization is an aggregate category handled separately
    standard_product_categories = [
        "gcp-core", 
        "data-analytics", 
        "cloud-security"
    ]
    
    # Define the categories that make up "app-modernization"
    app_modernization_categories = [
        "mandiant", 
        "looker", 
        "apigee", 
        "maps", 
        "marketplace", 
        "vertex-ai-platform"
    ]
    
    # Define the forecast categories
    forecast_categories = [
        "pipeline", 
        "upside", 
        "commit", 
        "closed-won"
    ]
    
    # Start building the base query
    base_query = db.session.query(
        Product.product_category,
        Opportunity.forecast_category,
        func.sum(Opportunity.amount * Opportunity.probability / 100.0).label('weighted_value'),
        func.count(Opportunity.opportunity_id).label('count')
    ).join(
        Product, Opportunity.product_id == Product.product_id
    ).join(
        Client, Opportunity.client_id == Client.client_id
    ).filter(
        Opportunity.forecast_category.in_(forecast_categories),
        extract('year', Opportunity.created_date) == year
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
        Opportunity.forecast_category
    ).all()
    
    # Process results to create the heatmap data
    # We'll track totals for app-modernization while processing standard categories
    heatmap_data = []
    app_modernization_totals = {fc: {'value': 0.0, 'count': 0} for fc in forecast_categories}
    
    for product_category, forecast_category, weighted_value, count in results:
        # Convert from potentially Decimal to float
        weighted_value = float(weighted_value) if weighted_value is not None else 0.0
        count = int(count) if count is not None else 0
        
        # Check if this belongs to app-modernization
        if product_category in app_modernization_categories:
            app_modernization_totals[forecast_category]['value'] += weighted_value
            app_modernization_totals[forecast_category]['count'] += count
        # Or if it's one of our standard categories
        elif product_category in standard_product_categories:
            heatmap_data.append({
                'product_category': product_category,
                'forecast_category': forecast_category,
                'value': round(weighted_value, 2),
                'count': count
            })
    
    # Add app-modernization data
    for forecast_category, totals in app_modernization_totals.items():
        if totals['value'] > 0 or totals['count'] > 0:
            heatmap_data.append({
                'product_category': 'app-modernization',
                'forecast_category': forecast_category,
                'value': round(totals['value'], 2),
                'count': totals['count']
            })
    
    # Add zero entries for any missing combinations
    all_product_categories = standard_product_categories + ['app-modernization']
    existing_combinations = {
        (item['product_category'], item['forecast_category']) 
        for item in heatmap_data
    }
    
    for product_category in all_product_categories:
        for forecast_category in forecast_categories:
            if (product_category, forecast_category) not in existing_combinations:
                heatmap_data.append({
                    'product_category': product_category,
                    'forecast_category': forecast_category,
                    'value': 0.0,
                    'count': 0
                })
    
    # Sort by product category and forecast category for consistency
    heatmap_data.sort(key=lambda x: (
        all_product_categories.index(x['product_category']),
        forecast_categories.index(x['forecast_category'])
    ))
    
    return heatmap_data