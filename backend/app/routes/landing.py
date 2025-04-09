"""
Landing Page Routes

This module defines API endpoints specific to the landing page functionality,
particularly the Key Performance Indicators (KPIs) dashboard.
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func, case, and_, or_, text
from ..models.models import (
    db, Opportunity, Revenue, Signing, Win, Client, User,
    DirectorAccountExecutive
)
from datetime import datetime
import logging


# Create a Blueprint for landing page routes
landing_bp = Blueprint('landing', __name__, url_prefix='/api/landing')

@landing_bp.route('/revenue-chart-data', methods=['GET'])
def get_revenue_chart_data():
    """
        Get Revenue Chart Data for histogram visualization

        Returns the distribution of revenue across the 12 months
        for the specified fiscal year, to be displayed as a histogram chart.

        Query parameters:
        - username: Username of the current user (required)
        - year: Fiscal year (default: 2024)

        Returns:
        - 200 OK with monthly revenue distribution data in format:
        {
            "revenue_chart_data": [
                {"month": 1, "revenue": 5000.0},
                {"month": 2, "revenue": 6200.0},
                ...
                {"month": 12, "revenue": 4500.0}
            ],
            "year": 2024
        }
        - 400 Bad Request if missing required parameters
        - 404 Not Found if user doesn't exist
   """
    # Get query parameters
    username = request.args.get('username', type=str)
    year = request.args.get('year', 2024, type=int)
    
    # Validate required parameters
    if not username:
        return jsonify({"error": "Missing required parameter: username"}), 400
    
    # Get user by username and validate
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Calculate revenue chart data based on user role
    if user.role == 'director':
        # For directors: Calculate revenue chart data for all account executives under them
        monthly_data = calculate_director_revenue_chart_data(user.user_id, year)
    elif user.role == 'account-executive':
        # For account executives: Calculate revenue chart data for their clients only
        monthly_data = calculate_ae_revenue_chart_data(user.user_id, year)
    else:
        # For any other role, return zeros for all months
        monthly_data = [
            {"month": 1, "revenue": 0.0},
            {"month": 2, "revenue": 0.0},
            {"month": 3, "revenue": 0.0},
            {"month": 4, "revenue": 0.0},
            {"month": 5, "revenue": 0.0},
            {"month": 6, "revenue": 0.0},
            {"month": 7, "revenue": 0.0},
            {"month": 8, "revenue": 0.0},
            {"month": 9, "revenue": 0.0},
            {"month": 10, "revenue": 0.0},
            {"month": 11, "revenue": 0.0},
            {"month": 12, "revenue": 0.0}
        ]
    
    return jsonify({
        "revenue_chart_data": monthly_data,
        "year": year
    }), 200
    

def calculate_director_revenue_chart_data(director_id, year):
    """Calculate monthly revenue chart data for a director based on all AEs under them"""
    
    # Get all account executives managed by this director
    ae_relations = DirectorAccountExecutive.query.filter_by(director_id=director_id).all()
    ae_ids = [relation.account_executive_id for relation in ae_relations]
    
    # Get all clients managed by these account executives
    client_ids = []
    if ae_ids:
        clients = Client.query.filter(Client.account_executive_id.in_(ae_ids)).all()
        client_ids = [client.client_id for client in clients]
    
    # Calculate revenue chart data using these client IDs
    return calculate_revenue_chart_data_for_clients(client_ids, year)


def calculate_ae_revenue_chart_data(ae_id, year):
    """Calculate monthly revenue chart data for an account executive based on their clients"""
    
    # Get all clients managed by this account executive
    clients = Client.query.filter_by(account_executive_id=ae_id).all()
    client_ids = [client.client_id for client in clients]
    
    # Calculate revenue chart data using these client IDs
    return calculate_revenue_chart_data_for_clients(client_ids, year)


def calculate_revenue_chart_data_for_clients(client_ids, year):
    """
    Calculate monthly revenue chart data for the specified clients
    
    Args:
        client_ids: List of client IDs to filter by, or None for all clients
        year: The fiscal year to calculate for
    
    Returns:
        List of dictionaries with month and revenue values
    """
    # If client_ids is an empty list, return zeros for all months
    if client_ids is not None and not client_ids:
        return [
            {"month": month, "revenue": 0.0}
            for month in range(1, 13)
        ]
    
    # Query to calculate sum of revenue grouped by month
    revenue_query = db.session.query(
        Revenue.month,
        func.sum(Revenue.amount).label('revenue')
    ).filter(
        Revenue.fiscal_year == year
    )
    
    # Add client filter if needed
    if client_ids is not None:
        revenue_query = revenue_query.filter(Revenue.client_id.in_(client_ids))
    
    # Group by month and order by month
    revenue_query = revenue_query.group_by(Revenue.month).order_by(Revenue.month)
    
    # Execute query
    monthly_results = revenue_query.all()
    
    # Initialize results with zeros for all months
    monthly_data = {month: 0.0 for month in range(1, 13)}
    
    # Update with actual values from query
    for month, revenue in monthly_results:
        monthly_data[month] = float(revenue)
    
    # Format into list of dictionaries for the response
    return [
        {"month": month, "revenue": revenue}
        for month, revenue in monthly_data.items()
    ]

@landing_bp.route('/win-chart-data', methods=['GET'])
def get_win_chart_data():
    """
        Get Win Chart Data for histogram visualization

        Returns the distribution of win counts (sum of win multipliers) by quarter
        for the specified fiscal year, to be displayed as a histogram chart.

        Query parameters:
        - username: Username of the current user (required)
        - year: Fiscal year (default: 2024)

        Returns:
        - 200 OK with quarterly win distribution data in format:
        {
            "win_chart_data": [
                {"quarter": 1, "win_count": 1.5},
                {"quarter": 2, "win_count": 2.0},
                {"quarter": 3, "win_count": 0.5}, 
                {"quarter": 4, "win_count": 1.0}
            ],
            "year": 2024
        }
        - 400 Bad Request if missing required parameters
        - 404 Not Found if user doesn't exist
    """
    # Get query parameters
    username = request.args.get('username', type=str)
    year = request.args.get('year', 2024, type=int)
    
    # Validate required parameters
    if not username:
        return jsonify({"error": "Missing required parameter: username"}), 400
    
    # Get user by username and validate
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Calculate win chart data based on user role
    if user.role == 'director':
        # For directors: Calculate win chart data for all account executives under them
        quarterly_data = calculate_director_win_chart_data(user.user_id, year)
    elif user.role == 'account-executive':
        # For account executives: Calculate win chart data for their clients only
        quarterly_data = calculate_ae_win_chart_data(user.user_id, year)
    else:
        # For any other role, return zeros for all quarters
        quarterly_data = [
            {"quarter": 1, "win_count": 0.0},
            {"quarter": 2, "win_count": 0.0},
            {"quarter": 3, "win_count": 0.0},
            {"quarter": 4, "win_count": 0.0}
        ]
    
    return jsonify({
        "win_chart_data": quarterly_data,
        "year": year
    }), 200

def calculate_director_win_chart_data(director_id, year):
    """Calculate quarterly win chart data for a director based on all AEs under them"""
    
    # Get all account executives managed by this director
    ae_relations = DirectorAccountExecutive.query.filter_by(director_id=director_id).all()
    ae_ids = [relation.account_executive_id for relation in ae_relations]
    
    # Get all clients managed by these account executives
    client_ids = []
    if ae_ids:
        clients = Client.query.filter(Client.account_executive_id.in_(ae_ids)).all()
        client_ids = [client.client_id for client in clients]
    
    # Calculate win chart data using these client IDs
    return calculate_win_chart_data_for_clients(client_ids, year)


def calculate_ae_win_chart_data(ae_id, year):
    """Calculate quarterly win chart data for an account executive based on their clients"""
    
    # Get all clients managed by this account executive
    clients = Client.query.filter_by(account_executive_id=ae_id).all()
    client_ids = [client.client_id for client in clients]
    
    # Calculate win chart data using these client IDs
    return calculate_win_chart_data_for_clients(client_ids, year)


def calculate_win_chart_data_for_clients(client_ids, year):
    """
    Calculate quarterly win chart data (sum of win multipliers by quarter) for the specified clients
    
    Args:
        client_ids: List of client IDs to filter by, or None for all clients
        year: The fiscal year to calculate for
    
    Returns:
        List of dictionaries with quarter and win_count values
    """
    # If client_ids is an empty list, return zeros for all quarters
    if client_ids is not None and not client_ids:
        return [
            {"quarter": 1, "win_count": 0.0},
            {"quarter": 2, "win_count": 0.0},
            {"quarter": 3, "win_count": 0.0},
            {"quarter": 4, "win_count": 0.0}
        ]
    
    # Query to calculate sum of win multipliers grouped by quarter
    wins_query = db.session.query(
        Win.fiscal_quarter,
        func.sum(Win.win_multiplier).label('win_count')
    ).filter(
        Win.fiscal_year == year
    )
    
    # Add client filter if needed
    if client_ids is not None:
        wins_query = wins_query.filter(Win.client_id.in_(client_ids))
    
    # Group by quarter and order by quarter
    wins_query = wins_query.group_by(Win.fiscal_quarter).order_by(Win.fiscal_quarter)
    
    # Execute query
    quarterly_results = wins_query.all()
    
    # Initialize results with zeros for all quarters
    quarterly_data = {
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0
    }
    
    # Update with actual values from query
    for quarter, win_count in quarterly_results:
        quarterly_data[quarter] = float(win_count)
    
    # Format into list of dictionaries for the response
    return [
        {"quarter": quarter, "win_count": count}
        for quarter, count in quarterly_data.items()
    ]


@landing_bp.route('/kpi-cards', methods=['GET'])
def get_kpi_cards():
    """
        Get Key Performance Indicators for the landing page cards

        Calculates four KPIs: Pipeline, Revenue, Signings, and Wins
        Based on user role (director or account executive) and year

        Query parameters:
        - username: Username of the current user (required)
        - year: Fiscal year (default: 2024)

        Returns:
        - 200 OK with calculated KPI values in format:
        {
            "pipeline": 125000.0,
            "revenue": 75000.0,
            "signings": 50000.0,
            "wins": 3.5
        }
        - 400 Bad Request if missing required parameters
        - 404 Not Found if user doesn't exist
        - 500 Internal Server Error with error details if calculation fails
    """
    try:
        # Get query parameters with defaults
        username = request.args.get('username', type=str)
        year = request.args.get('year', 2024, type=int)
        
        # Validate required parameters
        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        # Get user by username and validate
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Initialize default KPIs
        kpis = {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }
        
        # Calculate KPIs based on user role
        if user.role == 'director':
            # For directors: Calculate KPIs for all account executives under them
            kpis = calculate_director_kpis(user.user_id, year)
        elif user.role == 'account-executive':
            # For account executives: Calculate KPIs for their clients only
            kpis = calculate_ae_kpis(user.user_id, year)
        
        return jsonify(kpis), 200
        
    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error in KPI cards calculation: {str(e)}")
        return jsonify({"error": f"Failed to calculate KPIs: {str(e)}"}), 500


def calculate_director_kpis(director_id, year):
    """Calculate KPIs for a director based on all AEs under them"""
    try:
        # Initialize default KPIs
        kpis = {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }
        
        # Get all account executives managed by this director
        ae_relations = DirectorAccountExecutive.query.filter_by(director_id=director_id).all()
        
        # If no AEs are found, return zeros
        if not ae_relations:
            return kpis
            
        ae_ids = [relation.account_executive_id for relation in ae_relations]
        
        # Get all clients managed by these account executives
        client_ids = []
        clients = Client.query.filter(Client.account_executive_id.in_(ae_ids)).all()
        
        # If no clients are found, return zeros
        if not clients:
            return kpis
            
        client_ids = [client.client_id for client in clients]
        
        # Calculate KPIs using these client IDs
        return calculate_kpis_for_clients(client_ids, year)
        
    except Exception as e:
        logging.error(f"Error calculating director KPIs: {str(e)}")
        # Return zeros instead of raising the exception
        return {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }


def calculate_ae_kpis(ae_id, year):
    """Calculate KPIs for an account executive based on their clients"""
    try:
        # Initialize default KPIs
        kpis = {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }
        
        # Get all clients managed by this account executive
        clients = Client.query.filter_by(account_executive_id=ae_id).all()
        
        # If no clients are found, return zeros
        if not clients:
            return kpis
            
        client_ids = [client.client_id for client in clients]
        
        # Calculate KPIs using these client IDs
        return calculate_kpis_for_clients(client_ids, year)
        
    except Exception as e:
        logging.error(f"Error calculating AE KPIs: {str(e)}")
        # Return zeros instead of raising the exception
        return {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }


def calculate_kpis_for_clients(client_ids, year):
    """
    Calculate all four KPIs for the specified clients for the entire year
    
    Args:
        client_ids: List of client IDs to filter by
        year: The fiscal year to calculate for
    
    Returns:
        Dictionary with calculated KPI values
    """
    try:
        # Initialize KPI results
        kpis = {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }
        
        # If client_ids is an empty list, return zeros
        if not client_ids:
            return kpis
            
        # Calculate each KPI individually and catch exceptions for each
        try:
            kpis['pipeline'] = calculate_pipeline_kpi(client_ids, year)
        except Exception as e:
            logging.error(f"Error calculating pipeline KPI: {str(e)}")
            kpis['pipeline'] = 0.0
            
        try:
            kpis['revenue'] = calculate_revenue_kpi(client_ids, year)
        except Exception as e:
            logging.error(f"Error calculating revenue KPI: {str(e)}")
            kpis['revenue'] = 0.0
            
        try:
            kpis['signings'] = calculate_signings_kpi(client_ids, year)
        except Exception as e:
            logging.error(f"Error calculating signings KPI: {str(e)}")
            kpis['signings'] = 0.0
            
        try:
            kpis['wins'] = calculate_wins_kpi(client_ids, year)
        except Exception as e:
            logging.error(f"Error calculating wins KPI: {str(e)}")
            kpis['wins'] = 0.0
        
        return kpis
        
    except Exception as e:
        logging.error(f"Error in calculate_kpis_for_clients: {str(e)}")
        return {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }


def calculate_pipeline_kpi(client_ids, year):
    """Calculate the pipeline KPI value"""
    try:
        # Use date range filtering instead of extract function to handle timestamps properly
        start_date = f"{year}-01-01 00:00:00"
        end_date = f"{year}-12-31 23:59:59"
        
        # Create a query to calculate weighted pipeline value using the correct case syntax
        # The error shows we need to use positional elements for case statements
        pipeline_query = db.session.query(
            func.sum(
                case(
                    (Opportunity.forecast_category != 'omit', 
                     Opportunity.amount * Opportunity.probability / 100.0),
                    else_=0.0
                )
            )
        ).filter(
            Opportunity.client_id.in_(client_ids),
            Opportunity.created_date >= start_date,
            Opportunity.created_date <= end_date
        )
        
        pipeline_result = pipeline_query.scalar()
        
        # Return the result, default to 0.0 if None
        return float(pipeline_result) if pipeline_result is not None else 0.0
        
    except Exception as e:
        # Print the full exception for easier debugging
        print(f"Error in pipeline calculation: {str(e)}")
        return 0.0

def calculate_revenue_kpi(client_ids, year):
    """Calculate the revenue KPI value for the entire year"""
    try:
        # Simplify the query and use coalesce to handle nulls
        revenue_query = db.session.query(
            func.coalesce(
                func.sum(Revenue.amount),
                0.0  # Default to 0.0 if no rows match
            )
        ).filter(
            Revenue.client_id.in_(client_ids),
            Revenue.fiscal_year == year
        )
        
        # Execute query
        revenue_result = revenue_query.scalar()
        
        # Return the result, default to 0.0 if None
        return float(revenue_result) if revenue_result is not None else 0.0
        
    except Exception as e:
        logging.error(f"Error in revenue calculation: {str(e)}")
        return 0.0


def calculate_signings_kpi(client_ids, year):
    """Calculate the signings KPI value (annualized contract values) for the entire year"""
    try:
        # Simplify the date calculation to reduce errors
        # Instead of complex date math, use a simpler approach
        signings_query = db.session.query(
            func.coalesce(
                func.sum(
                    Signing.total_contract_value / 
                    func.greatest(
                        # Calculate the duration in years using a simpler approach
                        # Subtract the years directly and add 1 for partial years
                        (extract('year', Signing.end_date) - extract('year', Signing.start_date) + 1),
                        1.0  # Ensure we don't divide by zero
                    )
                ),
                0.0  # Default to 0.0 if no rows match
            )
        ).filter(
            Signing.client_id.in_(client_ids),
            Signing.fiscal_year == year
        )
        
        # Execute query
        signings_result = signings_query.scalar()
        
        # Return the result, default to 0.0 if None
        return float(signings_result) if signings_result is not None else 0.0
        
    except Exception as e:
        logging.error(f"Error in signings calculation: {str(e)}")
        return 0.0


def calculate_wins_kpi(client_ids, year):
    """Calculate the wins KPI value (sum of win multipliers) for the entire year"""
    try:
        # Use coalesce to handle nulls
        wins_query = db.session.query(
            func.coalesce(
                func.sum(Win.win_multiplier),
                0.0  # Default to 0.0 if no rows match
            )
        ).filter(
            Win.client_id.in_(client_ids),
            Win.fiscal_year == year
        )
        
        # Execute query
        wins_result = wins_query.scalar()
        
        # Return the result, default to 0.0 if None
        return float(wins_result) if wins_result is not None else 0.0
        
    except Exception as e:
        logging.error(f"Error in wins calculation: {str(e)}")
        return 0.0