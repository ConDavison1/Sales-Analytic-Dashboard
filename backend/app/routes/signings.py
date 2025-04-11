from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Signing, Client, User, Product,
    DirectorAccountExecutive
)
from datetime import datetime

# Create a Blueprint for signings routes
signings_bp = Blueprint('signings', __name__, url_prefix='/api/signings')

@signings_bp.route('/signings', methods=['GET'])
def get_signings():
    """
    Query signings with flexible filtering
    
    Returns signings filtered by various criteria and based on user role.
    Directors can see signings for all account executives they manage.
    Account executives can only see signings for their clients.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Year of the signing date (optional, default: 2024)
    - quarters: Comma-separated list of quarters of the signing date (optional)
      Example: quarters=1,2,3
    - product_categories: Comma-separated list of product categories to filter by (optional)
      Values: 'gcp-core', 'data-analytics', 'cloud-security', 'app-modernization'
      Example: product_categories=gcp-core,data-analytics
      Note: 'app-modernization' includes: looker, apigee, maps, marketplace, vertex-ai-platform, mandiant
    
    Response format:
    {
        "signings": [
            {
                "signing_id": 1,
                "client_name": "Acme Corp",
                "product_name": "Compute Engine",
                "product_category": "gcp-core",
                "total_contract_value": 150000.00,
                "incremental_acv": 50000.00,
                "start_date": "2024-01-01",
                "end_date": "2026-12-31",
                "signing_date": "2024-01-15",
                "fiscal_year": 2024,
                "fiscal_quarter": 1
            },
            ...
        ],
        "total_count": 12,
        "applied_filters": {
            "year": 2024,
            "quarters": [1, 2],
            "product_categories": ["gcp-core", "data-analytics"]
        }
    }
    
    Returns:
    - 200 OK with filtered signings
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
        
        # Parse comma-separated values
        quarters = []
        if quarters_param:
            try:
                quarters = [int(q.strip()) for q in quarters_param.split(',') if q.strip()]
                # Validate all quarters are between 1 and 4
                if not all(1 <= q <= 4 for q in quarters):
                    return jsonify({"error": "All quarters must be between 1 and 4"}), 400
            except ValueError:
                return jsonify({"error": "Invalid quarters format. Must be comma-separated integers."}), 400
        
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
        query, applied_filters = build_signings_query(user, year, quarters, product_categories)
        
        # Get total count for metadata
        total_count = query.count()
        
        # Execute query and get results
        results = query.order_by(Signing.signing_date.desc()).all()
        
        # Format the results
        signings = format_signings_results(results)
        
        # Return formatted response
        return jsonify({
            "signings": signings,
            "total_count": total_count,
            "applied_filters": applied_filters
        }), 200
        
    except Exception as e:
        print(f"Error in get_signings: {str(e)}")
        return jsonify({"error": f"Failed to query signings: {str(e)}"}), 500


def build_signings_query(user, year, quarters, product_categories):
    """
    Build the query for signings based on user role and filters
    
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
        Signing,
        Client.client_name,
        Product.product_name,
        Product.product_category
    ).join(
        Client, Signing.client_id == Client.client_id
    ).join(
        Product, Signing.product_id == Product.product_id
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
    query = query.filter(Signing.fiscal_year == year)
    
    # Apply quarters filter if provided
    if quarters:
        query = query.filter(Signing.fiscal_quarter.in_(quarters))
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


def format_signings_results(results):
    """
    Format the query results into the desired output structure
    
    Args:
        results: List of tuples from the query
    
    Returns:
        List of dictionaries with signing data
    """
    signings = []
    
    for signing, client_name, product_name, product_category in results:
        # For app-modernization categories, standardize the category name
        if product_category in ['looker', 'apigee', 'maps', 'marketplace', 'vertex-ai-platform', 'mandiant']:
            display_category = 'app-modernization'
        else:
            display_category = product_category
            
        signings.append({
            "signing_id": signing.signing_id,
            "client_name": client_name,
            "product_name": product_name,
            "product_category": display_category,
            "total_contract_value": float(signing.total_contract_value) if signing.total_contract_value else None,
            "incremental_acv": float(signing.incremental_acv) if signing.incremental_acv else None,
            "start_date": signing.start_date.strftime('%Y-%m-%d') if signing.start_date else None,
            "end_date": signing.end_date.strftime('%Y-%m-%d') if signing.end_date else None,
            "signing_date": signing.signing_date.strftime('%Y-%m-%d') if signing.signing_date else None,
            "fiscal_year": signing.fiscal_year,
            "fiscal_quarter": signing.fiscal_quarter
        })
    
    return signings