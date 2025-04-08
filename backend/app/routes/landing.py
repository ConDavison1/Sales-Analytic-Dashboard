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

# Create a Blueprint for landing page routes
landing_bp = Blueprint('landing', __name__, url_prefix='/api/landing')


@landing_bp.route('/kpi-cards', methods=['GET'])
def get_kpi_cards():
    """
    Get Key Performance Indicators for the landing page cards
    
    Calculates four KPIs: Pipeline, Revenue, Signings, and Wins
    Based on user role (director or account executive), year, and quarter
    
    Query parameters:
        - user_id: ID of the current user (required)
        - year: Fiscal year (default: 2024)
        - quarter: Fiscal quarter (default: 4)
    
    Returns:
        - 200 OK with calculated KPI values
        - 400 Bad Request if missing required parameters
        - 404 Not Found if user doesn't exist
    """
    # Get query parameters
    user_id = request.args.get('user_id', type=int)
    year = request.args.get('year', 2024, type=int)
    quarter = request.args.get('quarter', 4, type=int)
    
    # Validate required parameters
    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400
    
    # Validate quarter
    if quarter not in [1, 2, 3, 4]:
        return jsonify({"error": "Quarter must be between 1 and 4"}), 400
    
    # Get user and validate
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Calculate KPIs based on user role
    if user.role == 'director':
        # For directors: Calculate KPIs for all account executives under them
        kpis = calculate_director_kpis(user_id, year, quarter)
    elif user.role == 'account-executive':
        # For account executives: Calculate KPIs for their clients only
        kpis = calculate_ae_kpis(user_id, year, quarter)
    else:
        # For any other role, return zeros
        kpis = {
            'pipeline': 0.0,
            'revenue': 0.0, 
            'signings': 0.0,
            'wins': 0.0
        }
    
    return jsonify(kpis), 200


def calculate_director_kpis(director_id, year, quarter):
    """Calculate KPIs for a director based on all AEs under them"""
    
    # Get all account executives managed by this director
    ae_relations = DirectorAccountExecutive.query.filter_by(director_id=director_id).all()
    ae_ids = [relation.account_executive_id for relation in ae_relations]
    
    # Get all clients managed by these account executives
    client_ids = []
    if ae_ids:
        clients = Client.query.filter(Client.account_executive_id.in_(ae_ids)).all()
        client_ids = [client.client_id for client in clients]
    
    # Calculate KPIs using these client IDs
    return calculate_kpis_for_clients(client_ids, year, quarter)


def calculate_ae_kpis(ae_id, year, quarter):
    """Calculate KPIs for an account executive based on their clients"""
    
    # Get all clients managed by this account executive
    clients = Client.query.filter_by(account_executive_id=ae_id).all()
    client_ids = [client.client_id for client in clients]
    
    # Calculate KPIs using these client IDs
    return calculate_kpis_for_clients(client_ids, year, quarter)


def calculate_kpis_for_clients(client_ids, year, quarter):
    """
    Calculate all four KPIs for the specified clients
    
    Args:
        client_ids: List of client IDs to filter by, or None for all clients
        year: The fiscal year to calculate for
        quarter: The fiscal quarter (up to which to calculate)
    
    Returns:
        Dictionary with calculated KPI values
    """
    # Get end date for the specified quarter
    quarter_end_dates = {
        1: f"{year}-03-31",
        2: f"{year}-06-30",
        3: f"{year}-09-30",
        4: f"{year}-12-31"
    }
    end_date = quarter_end_dates[quarter]
    
    # Initialize KPI results
    kpis = {
        'pipeline': 0.0,
        'revenue': 0.0, 
        'signings': 0.0,
        'wins': 0.0
    }
    
    # If client_ids is an empty list, return zeros
    if client_ids is not None and not client_ids:
        return kpis
    
    # 1. Pipeline KPI
    kpis['pipeline'] = calculate_pipeline_kpi(client_ids, year, end_date)
    
    # 2. Revenue KPI
    kpis['revenue'] = calculate_revenue_kpi(client_ids, year, quarter)
    
    # 3. Signings KPI
    kpis['signings'] = calculate_signings_kpi(client_ids, year, quarter)
    
    # 4. Wins KPI
    kpis['wins'] = calculate_wins_kpi(client_ids, year, quarter)
    
    return kpis


def calculate_pipeline_kpi(client_ids, year, end_date):
    """Calculate the pipeline KPI value"""
    pipeline_query = db.session.query(
        func.sum(
            case(
                [(Opportunity.forecast_category != 'omit', 
                  Opportunity.amount * Opportunity.probability / 100)],
                else_=0
            )
        )
    ).filter(
        extract('year', Opportunity.created_date) == year,
        Opportunity.created_date <= end_date
    )
    
    # Add client filter if needed
    if client_ids is not None:
        pipeline_query = pipeline_query.filter(Opportunity.client_id.in_(client_ids))
    
    pipeline_result = pipeline_query.scalar()
    return float(pipeline_result) if pipeline_result else 0.0


def calculate_revenue_kpi(client_ids, year, quarter):
    """Calculate the revenue KPI value"""
    revenue_query = db.session.query(
        func.sum(Revenue.amount)
    ).filter(
        Revenue.fiscal_year == year,
        Revenue.fiscal_quarter <= quarter
    )
    
    # Add client filter if needed
    if client_ids is not None:
        revenue_query = revenue_query.filter(Revenue.client_id.in_(client_ids))
    
    revenue_result = revenue_query.scalar()
    return float(revenue_result) if revenue_result else 0.0


def calculate_signings_kpi(client_ids, year, quarter):
    """Calculate the signings KPI value (annualized contract values)"""
    # This SQL expression calculates the precise contract duration in years
    # by finding the exact difference between dates and dividing by 365.25
    duration_expr = func.cast(
        func.extract('epoch', Signing.end_date) - func.extract('epoch', Signing.start_date),
        db.Float
    ) / (60 * 60 * 24 * 365.25)  # Convert seconds to years
    
    signings_query = db.session.query(
        func.sum(Signing.total_contract_value / func.greatest(duration_expr, 1.0))
    ).filter(
        Signing.fiscal_year == year,
        Signing.fiscal_quarter <= quarter
    )
    
    # Add client filter if needed
    if client_ids is not None:
        signings_query = signings_query.filter(Signing.client_id.in_(client_ids))
    
    signings_result = signings_query.scalar()
    return float(signings_result) if signings_result else 0.0


def calculate_wins_kpi(client_ids, year, quarter):
    """Calculate the wins KPI value (sum of win multipliers)"""
    wins_query = db.session.query(
        func.sum(Win.win_multiplier)
    ).filter(
        Win.fiscal_year == year,
        Win.fiscal_quarter <= quarter
    )
    
    # Add client filter if needed
    if client_ids is not None:
        wins_query = wins_query.filter(Win.client_id.in_(client_ids))
    
    wins_result = wins_query.scalar()
    return float(wins_result) if wins_result else 0.0