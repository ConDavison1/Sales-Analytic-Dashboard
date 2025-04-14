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
from ..auth_utils import token_required  # Adjust path if needed


# Create a Blueprint for clients routes
clients_bp = Blueprint('clients', __name__, url_prefix='/api/clients')

@clients_bp.route('/industry-treemap-chart', methods=['GET'])
@token_required
def get_industry_treemap_chart():
    try:
        username = request.args.get('username', type=str)
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        treemap_data = get_industry_distribution_data(user)

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
    
@clients_bp.route('/province-pie-chart', methods=['GET'])
@token_required
def get_province_pie_chart():
    try:
        username = request.args.get('username', type=str)
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        province_data = get_province_distribution_data(user)
        labels = [item["province_name"] for item in province_data]
        series = [item["client_count"] for item in province_data]

        return jsonify({
            "labels": labels,
            "series": series,
            "additional_data": province_data
        }), 200

    except Exception as e:
        print(f"Error in get_province_pie_chart: {str(e)}")
        return jsonify({"error": f"Failed to calculate province pie chart data: {str(e)}"}), 500


def get_province_distribution_data(user):
    """
    Get the distribution of clients by province with revenue and count data.
    
    For directors, includes clients managed by all account executives they manage.
    For account executives, includes only their clients.
    
    Args:
        user: The User object
    
    Returns:
        List of dictionaries with province code, name, client count, and revenue
    """
    try:
        # Start building the base query to get client counts and revenue by province
        query = db.session.query(
            Client.province,
            func.count(Client.client_id).label('client_count'),
            func.coalesce(func.sum(Revenue.amount), 0.0).label('revenue_amount')
        ).outerjoin(  # Use outer join to include clients with no revenue
            Revenue, Client.client_id == Revenue.client_id
        ).filter(
            Client.province != None,  # Ensure province is not null
            Client.province != ''     # Ensure province is not empty
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
        
        # Group by province and execute query
        query = query.group_by(Client.province)
        results = query.all()
        
        # Province code to full name mapping
        province_names = {
            'AB': 'Alberta',
            'BC': 'British Columbia',
            'MB': 'Manitoba',
            'NB': 'New Brunswick',
            'NL': 'Newfoundland and Labrador',
            'NS': 'Nova Scotia',
            'NT': 'Northwest Territories',
            'NU': 'Nunavut',
            'ON': 'Ontario',
            'PE': 'Prince Edward Island',
            'QC': 'Quebec',
            'SK': 'Saskatchewan',
            'YT': 'Yukon'
        }
        
        # Process results into list of dictionaries
        province_data = []
        for province, client_count, revenue_amount in results:
            # Convert to appropriate types
            client_count = int(client_count) if client_count is not None else 0
            revenue_amount = float(revenue_amount) if revenue_amount is not None else 0.0
            
            # Get full province name
            province_name = province_names.get(province, province)
            
            # Only include provinces with clients
            if client_count > 0:
                province_data.append({
                    "province": province,
                    "province_name": province_name,
                    "client_count": client_count,
                    "revenue": revenue_amount
                })
        
        # Sort by client count in descending order
        province_data.sort(key=lambda x: x["client_count"], reverse=True)
        
        return province_data
        
    except Exception as e:
        print(f"Error in get_province_distribution_data: {str(e)}")
        return []

@clients_bp.route('/clients', methods=['GET'])
@token_required
def get_clients():
    """
    Query clients data with flexible filtering

    This endpoint is now protected by JWT.
    """
    try:
        username = request.args.get('username', type=str)
        provinces_param = request.args.get('provinces', type=str)
        industries_param = request.args.get('industries', type=str)

        provinces = [p.strip().upper() for p in provinces_param.split(',')] if provinces_param else []
        industries = [i.strip() for i in industries_param.split(',')] if industries_param else []

        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        query, applied_filters = build_clients_query(user, provinces, industries)

        total_count = query.count()
        results = query.order_by(Client.client_name).limit(1000).all()
        clients_data = format_clients_results(results)

        return jsonify({
            "clients": clients_data,
            "total_count": total_count,
            "applied_filters": applied_filters
        }), 200

    except Exception as e:
        print(f"Error in get_clients: {str(e)}")
        return jsonify({"error": f"Failed to query clients: {str(e)}"}), 500



def build_clients_query(user, provinces=None, industries=None):
    """
    Build the query for clients based on user role and filters
    
    Args:
        user: The User object
        provinces: List of province codes to filter by (optional)
        industries: List of industries to filter by (optional)
    
    Returns:
        Tuple of (query, applied_filters)
    """
    # Start building the base query
    query = db.session.query(
        Client,
        User.first_name,
        User.last_name,
        User.user_id
    ).join(
        User, Client.account_executive_id == User.user_id
    )
    
    # Initialize applied filters dictionary
    applied_filters = {}
    
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
    
    # Apply province filter if provided
    if provinces:
        query = query.filter(Client.province.in_(provinces))
        applied_filters["provinces"] = provinces
    
    # Apply industry filter if provided (case-insensitive)
    if industries:
        # Create a list of case-insensitive conditions for each industry
        industry_conditions = []
        for industry in industries:
            industry_conditions.append(func.lower(Client.industry) == func.lower(industry))
        
        # Combine conditions with OR
        if industry_conditions:
            query = query.filter(or_(*industry_conditions))
        
        applied_filters["industries"] = industries
    
    return query, applied_filters


def format_clients_results(results):
    """
    Format the query results into the desired output structure
    
    Args:
        results: List of tuples from the query
    
    Returns:
        List of dictionaries with client data
    """
    clients_data = []
    
    for client, ae_first_name, ae_last_name, ae_id in results:
        # Format the account executive name
        account_executive = f"{ae_first_name} {ae_last_name}" if ae_first_name and ae_last_name else ""
        account_executive = account_executive.strip()
            
        clients_data.append({
            "client_id": client.client_id,
            "client_name": client.client_name,
            "industry": client.industry,
            "city": client.city,
            "province": client.province,
            "account_executive": account_executive,
            "account_executive_id": ae_id,
            "created_date": client.created_date.strftime('%Y-%m-%d') if client.created_date else None
        })
    
    return clients_data