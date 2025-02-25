from typing import Counter
from flask import Flask, render_template, request, jsonify
from models import db, User, Pipeline, Revenue, Win, Signing, AccountExecutive, Client
from sqlalchemy.exc import IntegrityError
from config_module import Config
import uuid
import traceback
from flask_cors import CORS
from sqlalchemy import func



app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

#Login post method
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print(f"Username from request: {username}")
        print(f"Password from request: {password}")

        user = User.query.filter_by(username=username).first()

        if user:
            print(f"User from DB: {user.username}, Stored Password: {user.password}")
        else:
            print("User not found.")

        if user and user.password == password:
            token = str(uuid.uuid4())
            return jsonify({"message": "Login successful!", "token": token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": f"An error occurred: {e}"}), 500


@app.route('/chart-data', methods=['GET'])
def chart_data():
    try:
        pipeline_data = [p.opportunity_value for p in Pipeline.query.all()]
        revenue_data = [r.total_revenue for r in Revenue.query.all()]
        wins_data = [w.id for w in Win.query.filter_by(is_win=True).all()]
        signings_data = [s.incremental_acv for s in Signing.query.all()]

        return jsonify({
            "pipeline": pipeline_data,
            "revenue": revenue_data,
            "wins": wins_data,
            "signings": signings_data
        }), 200
    except Exception as e:
        print("Error in /chart-data:", traceback.format_exc())
        return jsonify({"message": f"An error occurred: {e}"}), 500

# Get Method for the signings chart being displayed on the landing page
@app.route('/sign-chart-data', methods=['GET'])
def sign_chart_data():
    try:
        results = db.session.query(Signing.forecast_category, db.func.count()).group_by(Signing.forecast_category).all()
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/revenue-client', methods=['GET'])
def get_revenue_clients():
    try:
        revenue_clients_data = [
            {
                "account_name": r.account_name,
                "revenue_type": r.revenue_type,
                "total_revenue": r.total_revenue,
                "iacv": r.iacv
            }
            for r in Revenue.query.all()
        ]
        return jsonify(revenue_clients_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500


# Get Account Exec Information
@app.route('/account_executives', methods=['GET'])
def account_executives():
    try:
        executives = []
        for row in AccountExecutive.query.all():
            assigned_accounts = eval(row.assigned_accounts) if isinstance(row.assigned_accounts, str) else row.assigned_accounts
            performance_metrics = eval(row.performance_metrics) if isinstance(row.performance_metrics, str) else row.performance_metrics
            number_of_clients = len(assigned_accounts)
            sales = performance_metrics.get('sales', 0)
            targets = performance_metrics.get('targets', 0)
            performance_percentage = targets if targets > 0 else 0

            executives.append({
                "name": f"{row.first_name} {row.last_name}",
                "clients": number_of_clients,
                "performance": {
                    "value": f"${sales}",
                    "percentage": performance_percentage,
                    "color": "green" if performance_percentage >= 70 else ("#ffc107" if performance_percentage >= 40 else "red")
                },
                "status": {
                    "value": row.status,
                    "percentage": 100,
                    "color": "green" if row.status == "Active" else "red"
                }
            })
        return jsonify(executives), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

# Get Method for the revenue chart being displayed on the landing page
@app.route('/revenue-chart-data', methods=['GET'])
def revenue_chart_data():
    try:
        results = db.session.query(Revenue.revenue_type, db.func.count()).group_by(Revenue.revenue_type).all()
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

#Revenue Card get method
@app.route('/revenue-sum', methods=['GET'])
def revenue_sum():
    try:
        total = db.session.query(db.func.sum(Revenue.total_revenue)).scalar()
        return jsonify({"revenue_sum": total}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

#Pipeline Card get method
@app.route('/pipeline-count', methods=['GET'])
def pipeline_count():
    try:
        total = db.session.query(db.func.sum(Pipeline.opportunity_value)).scalar()
        return jsonify({"pipeline_count": total}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

#Signings Card get method
@app.route('/signings-count', methods=['GET'])
def signings_count():
    try:
        total = db.session.query(db.func.sum(Signing.incremental_acv)).scalar()
        return jsonify({"signings_count": total}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

#Wins Card get method    
@app.route('/wins-count', methods=['GET'])
def wins_count():
    try:
        total = db.session.query(db.func.count(Win.id)).filter(Win.is_win == True).scalar()
        return jsonify({"wins_count": total}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/clients', methods=['GET'])
def clients():
    try:
        clients = []
        for row in Client.query.all():
            clients.append({
                "client_id": row.client_id,
                "executive_id": row.executive_id,
                "company_name": row.company_name,
                "industry": row.industry,
                "email": row.email,
                "location": row.location
            })
        return jsonify(clients), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

#Signings Estimates table get method
@app.route('/signings-data', methods=['GET'])
def signingschart():
    try:
        signings = []
        for row in Signing.query.all():
            signings.append({
                "account_name": row.account_name,
                "opportunity_id": row.opportunity_id,
                "incremental_acv": row.incremental_acv,
                "forecast_category": row.forecast_category,
                "signing_date": row.signing_date

            })
        return jsonify(signings), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

from sqlalchemy import func

@app.route('/signingsChart', methods=['GET'])
def signingsChart():
    try:
        results = db.session.query(Signing.forecast_category, func.count()).group_by(Signing.forecast_category).all()
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    

# ------------------------------------
# Count-to-win endpoints

@app.route('/wins-industry/<string:industry_name>', methods=['GET'])
def get_wins_by_industry(industry_name):
    """
    Endpoint to retrieve all wins for a given industry.
    
    :param industry_name: Name of the industry to filter wins by.
    :return: JSON response containing a list of wins related to the specified industry.    
    """
    try:
        # Query the database for all wins where the industry matches the provided name
        wins = Win.query.filter_by(industry=industry_name).all()
        
        # Convert the list of Win objects into a list of dictionaries
        result = [
            {
                "id": win.id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime('%Y-%m-%d'),  # Convert date to string format
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "stage": win.stage,
                "is_win": win.is_win
            } 
            for win in wins
        ]
        
        # Return the JSON response with the wins data
        return jsonify({"wins_industry": result}), 200

    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
@app.route('/wins-account-type/<string:account_type>', methods=['GET'])
def get_wins_by_account_type(account_type):
    """
    Endpoint to retrieve all wins for a given account type.
    
    :param account_type: Type of the account to filter wins by.
    :return: JSON response containing a list of wins related to the specified account type.    
    """
    try:
        # Query the database for all wins where the account type matches the provided name
        wins = Win.query.filter_by(account_type=account_type).all()
        
        # Convert the list of Win objects into a list of dictionaries
        result = [
            {
                "id": win.id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime('%Y-%m-%d'),  # Convert date to string format
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "stage": win.stage,
                "is_win": win.is_win
            } 
            for win in wins
        ]
        
        # Return the JSON response with the wins data
        return jsonify({"wins_account_type": result}), 200

    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route('/wins-account-name/<string:account_name>', methods=['GET'])
def get_wins_by_account_name(account_name):
    """
    Endpoint to retrieve all wins for a given account name.
    
    :param account_name: Name of the account to filter wins by.
    :return: JSON response containing a list of wins related to the specified account name.    
    """
    try:
        wins = Win.query.filter_by(account_name=account_name).all()
        result = [
            {
                "id": win.id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime('%Y-%m-%d'),
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "stage": win.stage,
                "is_win": win.is_win
            }
            for win in wins
        ]
        return jsonify({"wins_account_name": result}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
@app.route('/wins-stage/<string:stage>', methods=['GET'])
def get_wins_by_stage(stage):
    """
    Endpoint to retrieve all wins for a given stage.
    
    :param stage: The stage of the win to filter by.
    :return: JSON response containing a list of wins related to the specified stage.
    """
    try:
        wins = Win.query.filter_by(stage=stage).all()
        result = [
            {
                "id": win.id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime('%Y-%m-%d'),
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "stage": win.stage,
                "is_win": win.is_win
            }
            for win in wins
        ]
        return jsonify({"wins_stage": result}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
@app.route('/wins-deal-range', methods=['GET'])
def get_wins_deal_range():
    """
    Endpoint to retrieve all wins within a specified deal value range.
    
    Query Parameters:
    - lower_bound: Minimum deal value (optional, defaults to 0)
    - upper_bound: Maximum deal value (optional, defaults to a high number)
    
    :return: JSON response containing a list of wins within the specified deal value range.
    """
    try:
        lower_bound = float(request.args.get('lower_bound', 0))
        upper_bound = float(request.args.get('upper_bound', float('inf')))
        
        # Query the database for wins within the deal value range
        wins = Win.query.filter(Win.deal_value.between(lower_bound, upper_bound)).all()
        
        result = [
            {
                "id": win.id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime('%Y-%m-%d'),
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "stage": win.stage,
                "is_win": win.is_win
            }
            for win in wins
        ]
        
        return jsonify({"wins_deal_range": result}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
@app.route('/wins-date-range', methods=['GET'])
def get_wins_date_range():
    """
    Endpoint to retrieve all wins within a specified date range.
    
    Query Parameters:
    - start_date: Start date in YYYY-MM-DD format (optional)
    - end_date: End date in YYYY-MM-DD format (optional)
    
    :return: JSON response containing a list of wins within the specified date range.
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        date_format = "%Y-%m-%d"

        # Validate and parse dates
        if start_date:
            start_date = datetime.strptime(start_date, date_format).date()
        if end_date:
            end_date = datetime.strptime(end_date, date_format).date()

        # Query construction
        query = Win.query
        if start_date and end_date:
            query = query.filter(Win.win_date.between(start_date, end_date))
        elif start_date:
            query = query.filter(Win.win_date >= start_date)
        elif end_date:
            query = query.filter(Win.win_date <= end_date)

        # Execute query
        wins = query.all()

        result = [
            {
                "id": win.id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime('%Y-%m-%d'),
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "stage": win.stage,
                "is_win": win.is_win
            }
            for win in wins
        ]

        return jsonify({"wins_date_range": result}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Count-to-win endpoints    
# ------------------------------------



@app.route('/test', methods=['GET'])
def test():
    return "Flask is running!"


if __name__ == '__main__':
    app.run(debug=True)
