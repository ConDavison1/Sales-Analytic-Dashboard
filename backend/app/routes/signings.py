from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, and_, or_
from ..models.models import (
    db, Signing, Client, User, Product,
    DirectorAccountExecutive, YearlyTarget, QuarterlyTarget
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


@signings_bp.route('/industry-acv-chart-data', methods=['GET'])
def get_industry_acv_chart_data():
    """
    Get industry ACV histogram data
    
    Returns data for a histogram showing the distribution of the sum of incremental ACV
    values for the top 4 industries with signings.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Year of the signing date (optional, default: 2024)
    
    Response format:
    {
        "industry_acv_data": [
            {"industry": "Financial Services", "incremental_acv": 750000.0},
            {"industry": "Healthcare", "incremental_acv": 500000.0},
            {"industry": "Manufacturing", "incremental_acv": 350000.0},
            {"industry": "Retail", "incremental_acv": 250000.0}
        ],
        "year": 2024
    }
    
    Returns:
    - 200 OK with industry ACV histogram data
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if query execution fails
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
        
        # Get industry ACV data based on user role
        industry_acv_data = get_industry_acv_data(user, year)
        
        # Return formatted response
        return jsonify({
            "industry_acv_data": industry_acv_data,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in get_industry_acv_histogram: {str(e)}")
        return jsonify({"error": f"Failed to calculate industry ACV histogram data: {str(e)}"}), 500


def get_industry_acv_data(user, year):
    """
    Get industry ACV data for the top 4 industries.
    
    For directors, includes signings for all clients managed by account executives they manage.
    For account executives, includes only signings for their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with industry and incremental_acv values for top 4 industries
    """
    # Start building the base query to get sum of incremental_acv by industry
    query = db.session.query(
        Client.industry,
        func.sum(Signing.incremental_acv).label('incremental_acv')
    ).join(
        Signing, Client.client_id == Signing.client_id
    ).filter(
        Signing.fiscal_year == year
    ).group_by(
        Client.industry
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
    
    # Order by incremental_acv in descending order and limit to top 4
    query = query.order_by(func.sum(Signing.incremental_acv).desc()).limit(4)
    
    # Execute query
    results = query.all()
    
    # Format the results
    industry_acv_data = []
    for industry, incremental_acv in results:
        # Skip if industry is None or empty
        if not industry:
            continue
            
        industry_acv_data.append({
            "industry": industry,
            "incremental_acv": float(incremental_acv) if incremental_acv is not None else 0.0
        })
    
    # Ensure we have exactly 4 industries (or fewer if not enough data)
    while len(industry_acv_data) < 4:
        # Add placeholder dummy data if we have fewer than 4 industries
        # This is just to maintain the expected format, can be removed if not needed
        industry_acv_data.append({
            "industry": f"Other {len(industry_acv_data) + 1}",
            "incremental_acv": 0.0
        })
    
    return industry_acv_data

@signings_bp.route('/provincial-distribution-chart', methods=['GET'])
def get_provincial_distribution_chart():
    """
    Get the distribution of contracts and average values by province
    
    Returns data for a polar area chart showing the number of contracts signed
    and average contract value for each province.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Year of the signing date (optional, default: 2024)
    
    Response format:
    {
        "provincial_data": [
            {"province": "ON", "count": 23, "avg_value": 75000.0},
            {"province": "QC", "count": 17, "avg_value": 92000.0},
            {"province": "BC", "count": 12, "avg_value": 110000.0},
            ...
        ],
        "year": 2024
    }
    
    Returns:
    - 200 OK with provincial distribution data
    - 400 Bad Request if missing required parameters
    - 404 Not Found if user doesn't exist
    - 500 Internal Server Error if query execution fails
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
        
        # Get provincial distribution data based on user role
        provincial_data = get_provincial_distribution_data(user, year)
        
        # Return formatted response
        return jsonify({
            "provincial_data": provincial_data,
            "year": year
        }), 200
        
    except Exception as e:
        print(f"Error in get_provincial_distribution_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate provincial distribution data: {str(e)}"}), 500


def get_provincial_distribution_data(user, year):
    """
    Get the distribution of contracts and average values by province.
    
    For directors, includes signings for all clients managed by account executives they manage.
    For account executives, includes only signings for their clients.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with province, count, and avg_value
    """
    try:
        # Define the list of valid provinces to include
        valid_provinces = ['ON', 'QC', 'NS', 'NB', 'MB', 'BC', 'PE', 'SK', 'AB', 'NL']
        
        # Start building the base query to get count and average value by province
        query = db.session.query(
            Client.province,
            func.count(Signing.signing_id).label('count'),
            func.avg(Signing.total_contract_value).label('avg_value')
        ).join(
            Signing, Client.client_id == Signing.client_id
        ).filter(
            Signing.fiscal_year == year,
            Client.province.in_(valid_provinces)  # Only include valid provinces
        ).group_by(
            Client.province
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
        
        # Order by count in descending order
        query = query.order_by(func.count(Signing.signing_id).desc())
        
        # Execute query
        results = query.all()
        
        # Format the results
        provincial_data = []
        for province, count, avg_value in results:
            provincial_data.append({
                "province": province,
                "count": count,
                "avg_value": float(avg_value) if avg_value is not None else 0.0
            })
        
        # Get provinces with no signings but in our valid list
        provinces_with_data = {item["province"] for item in provincial_data}
        missing_provinces = [p for p in valid_provinces if p not in provinces_with_data]
        
        # Add missing provinces with zero values
        for province in missing_provinces:
            provincial_data.append({
                "province": province,
                "count": 0,
                "avg_value": 0.0
            })
        
        # Re-sort the final list by count (ensures proper order after adding zeros)
        provincial_data.sort(key=lambda x: x["count"], reverse=True)
        
        return provincial_data
        
    except Exception as e:
        print(f"Error in get_provincial_distribution_data: {str(e)}")
        return []
    
@signings_bp.route('/signings-quarterly-targets', methods=['GET'])
def get_signings_quarterly_targets():
    """
    Get quarterly accumulated signing values and target achievement percentages
    
    For each quarter, calculates the accumulated signing annual contract values and the percentage
    of the quarterly target achieved. Accumulated values represent the total from Q1 through the specified quarter.
    
    Query parameters:
    - username: Username of the current user (required)
    - year: Fiscal year (optional, default: 2024)
    
    Response format:
    {
        "quarterly_targets": [
            {
                "quarter": 1,
                "accumulated_value": 12500.0,   // Accumulated value through Q1
                "achievement_percentage": 50.0   // Percentage of Q1 target achieved
            },
            {
                "quarter": 2,
                "accumulated_value": 25000.0,   // Accumulated value through Q2
                "achievement_percentage": 50.0   // Percentage of Q2 target achieved
            },
            {
                "quarter": 3,
                "accumulated_value": 37500.0,   // Accumulated value through Q3
                "achievement_percentage": 50.0   // Percentage of Q3 target achieved
            },
            {
                "quarter": 4,
                "accumulated_value": 50000.0,   // Accumulated value through Q4
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
        
        # Get all relevant signings
        signings_data = get_user_signings(user, year)
        
        # Get the user's quarterly target percentages
        quarterly_percentages = get_user_signing_targets(user.user_id, year)
        
        # Get the yearly target amount
        yearly_target_amount = get_yearly_signing_target_amount(user, year)
        
        # Calculate the quarterly accumulated values and achievement percentages
        quarterly_targets = calculate_quarterly_signing_targets(signings_data, quarterly_percentages, yearly_target_amount)
        
        # Return response
        return jsonify({
            "quarterly_targets": quarterly_targets,
            "year": year,
            "quarterly_percentages": quarterly_percentages
        }), 200
        
    except Exception as e:
        print(f"Error in signings quarterly targets: {str(e)}")
        return jsonify({"error": f"Failed to calculate quarterly targets: {str(e)}"}), 500


def get_yearly_signing_target_amount(user, year):
    """
    Get the yearly signing target amount for a user.
    
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


def get_user_signings(user, year):
    """
    Get all relevant signings data for a user in the specified year.
    
    For directors, gets signings from all account executives they manage.
    For account executives, gets only their signings.
    
    Args:
        user: The User object
        year: The fiscal year to filter by
    
    Returns:
        List of dictionaries with signing data
    """
    # Start building the query to get signings
    query = db.session.query(
        Signing,
        Client
    ).join(
        Client, Signing.client_id == Client.client_id
    ).filter(
        Signing.fiscal_year == year
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
    signings_data = []
    for signing, client in results:
        # Calculate annual contract value (total value divided by duration in years)
        annual_contract_value = 0.0
        if signing.total_contract_value is not None and signing.start_date and signing.end_date:
            # Calculate duration in years
            days = (signing.end_date - signing.start_date).days
            years = max(days / 365.25, 1.0)  # Ensure at least 1 year
            
            # Calculate annual contract value
            annual_contract_value = float(signing.total_contract_value) / years
        
        signings_data.append({
            'signing_id': signing.signing_id,
            'quarter': signing.fiscal_quarter,
            'annual_contract_value': annual_contract_value,
            'account_executive_id': client.account_executive_id
        })
    
    return signings_data


def get_user_signing_targets(user_id, year):
    """
    Get a user's quarterly target percentages for signings.
    
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
    quarterly_percentages = [25.0, 25.0, 25.0, 25.0]
    
    # Try to get the user's yearly target for signings
    yearly_target = YearlyTarget.query.filter_by(
        user_id=user_id,
        fiscal_year=year,
        target_type='signings'
    ).first()
    
    if yearly_target:
        # Try to get quarterly targets from database
        for quarter in range(1, 5):
            quarterly_target = QuarterlyTarget.query.filter_by(
                target_id=yearly_target.target_id,
                fiscal_quarter=quarter
            ).first()
            
            if quarterly_target and quarterly_target.percentage is not None:
                # Convert from Decimal to float
                quarterly_percentages[quarter - 1] = float(quarterly_target.percentage)
    
    return quarterly_percentages


def calculate_quarterly_signing_targets(signings_data, quarterly_percentages, yearly_target_amount):
    """
    Calculate quarterly accumulated values and achievement percentages for signings.
    
    Args:
        signings_data: List of dictionaries with signing data
        quarterly_percentages: List of percentages for each quarter
        yearly_target_amount: The yearly signing target amount for the user
    
    Returns:
        List of dictionaries with quarter, accumulated_value, and achievement_percentage
    """
    # Initialize accumulated values for each quarter
    accumulated_values = [0.0, 0.0, 0.0, 0.0]
    
    # Calculate accumulated value for each quarter
    for signing in signings_data:
        quarter = signing['quarter']
        value = signing['annual_contract_value']
        
        # Add this signing's value to all quarters from its quarter through Q4
        for q in range(quarter - 1, 4):
            accumulated_values[q] += value
    
    # Calculate quarterly targets
    quarterly_targets = []
    
    for quarter in range(1, 5):
        # Get the accumulated value for this quarter
        accumulated_value = accumulated_values[quarter - 1]
        
        # Get the quarterly target percentage for this quarter
        quarter_percentage = quarterly_percentages[quarter - 1]
        
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