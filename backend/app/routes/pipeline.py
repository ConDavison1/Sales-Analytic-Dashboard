"""
Pipeline Routes

This module defines API endpoints for the pipeline functionality,
particularly the opportunities filtering and querying.
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Opportunity, Client, User, Product,
    DirectorAccountExecutive
)
from datetime import datetime

# Create a Blueprint for pipeline routes
pipeline_bp = Blueprint('pipeline', __name__, url_prefix='/api/pipeline')

@pipeline_bp.route('/opportunities', methods=['GET'])
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