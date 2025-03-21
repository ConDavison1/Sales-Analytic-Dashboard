from datetime import datetime
from models import db, User, Client, Pipeline, Signing, Revenue, Win, AccountExecutive
from sqlalchemy.exc import IntegrityError
from config_module import Config
import traceback
from flask_cors import CORS
from sqlalchemy import func
from werkzeug.security import check_password_hash
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config.from_object(Config) 
jwt = JWTManager(app)
CORS(app, supports_credentials=True)
db.init_app(app)


load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

            clients_data = []
            if user.role == 'Account Executive':
                clients = Client.query.filter_by(executive_id=user.id).all()
                clients_data = [{"id": client.client_id, "name": client.company_name} for client in clients]
            elif user.role == 'Director':
                clients = Client.query.all()
                clients_data = [{"id": client.client_id, "name": client.company_name} for client in clients]

            print(f"User Role: {user.role}")
            print(f"Generated Token: {access_token}")  

            return jsonify({
                "message": "Login successful!",
                "token": access_token,
                "role": user.role,
                "clients": clients_data
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": f"An error occurred: {e}"}), 500



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message="Access granted", user=current_user), 200



@app.route('/chart-data', methods=['GET'])
def chart_data():
    try:
        pipeline_data = [p.opportunity_value for p in Pipeline.query.all()]
        revenue_data = [r.total_revenue for r in Revenue.query.all()]
        wins_count = db.session.query(db.func.count(Win.opportunity_id)).filter(Win.is_win == True).scalar()

        signings_data = [s.incremental_acv for s in Signing.query.all()]

        return jsonify({
            "pipeline": pipeline_data,
            "revenue": revenue_data,
            "wins": [wins_count],  
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
        for row in AccountExecutive.query.order_by(AccountExecutive.executive_id).all():
            assigned_accounts = eval(row.assigned_accounts) if isinstance(row.assigned_accounts, str) else row.assigned_accounts
            performance_metrics = eval(row.performance_metrics) if isinstance(row.performance_metrics, str) else row.performance_metrics
            number_of_clients = len(assigned_accounts)
            sales = performance_metrics.get('sales', 0)
            targets = performance_metrics.get('targets', 0)
            performance_percentage = targets if targets > 0 else 0

            executives.append({
                "name": f"{row.first_name} {row.last_name}",
                "executive_id": row.executive_id,
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
        total = db.session.query(db.func.count(Win.opportunity_id)).filter(Win.is_win == True).scalar()
        total = db.session.query(db.func.count(Win.opportunity_id)).filter(Win.is_win == True).scalar()
        return jsonify({"wins_count": total}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

#Clients table get method
#Clients table get method
@app.route('/clients', methods=['GET'])
@jwt_required()
def clients():
    try:
        print("Incoming request headers:")
        for key, value in request.headers.items():
            print(f"{key}: {value}")

        user_id = get_jwt_identity()  
        claims = get_jwt() 
        user_role = claims.get("role") 

        print(f"Authenticated User: ID={user_id}, Role={user_role}")

        if not user_role:
            return jsonify({"message": "Invalid user role"}), 400

        if user_role == "Director":
            clients = Client.query.all()
        elif user_role == "Account Executive":
            clients = Client.query.filter_by(executive_id=int(user_id)).all()
        else:
            return jsonify({"message": "Access denied"}), 403

        clients_data = [
            {
                "client_id": client.client_id,
                "executive_id": client.executive_id,
                "company_name": client.company_name,
                "industry": client.industry,
                "email": client.email,
                "location": client.location
            }
            for client in clients
        ]

        print("Sending clients data:", clients_data)
        return jsonify(clients_data), 200


    except Exception as e:
        print(f"Error in /clients endpoint: {e}")
        return jsonify({"message": f"An error occurred: {e}"}), 500
    
# @app.route('/clients/<int:client_id>', methods=['DELETE'])
# def delete_client(client_id):
#     try:
#         client = db.session.get(Client, client_id)
#         if not client:
#             return jsonify({"message": "Client not found"}), 404

#         executive_id = client.executive_id

#         executive = db.session.get(AccountExecutive, executive_id)
#         if executive and executive.assigned_accounts:
#             if client_id in executive.assigned_accounts:
#                 executive.assigned_accounts.remove(client_id)

#                 db.session.execute(
#                     AccountExecutive.__table__.update().
#                     where(AccountExecutive.executive_id == executive.executive_id).
#                     values(assigned_accounts=executive.assigned_accounts)
#                 )
#                 db.session.commit()

#         db.session.delete(client)
#         db.session.commit()

#         return jsonify({"message": "Client deleted successfully"}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": f"An error occurred: {e}"}), 500

    
# @app.route('/clients', methods=['POST'])
# def add_client():
#     try:
#         data = request.get_json()

#         if not data:
#             return jsonify({"message": "Invalid JSON payload"}), 400

#         client = Client(
#             executive_id=data.get('executive_id'),
#             company_name=data.get('company_name'),
#             industry=data.get('industry'),
#             email=data.get('email'),
#             location=data.get('location')
#         )

       

       
#         db.session.add(client)
#         db.session.commit() 

#         executive = db.session.get(AccountExecutive, client.executive_id)
#         if executive:
#             print(f"Before update (executive {executive.executive_id}): {executive.assigned_accounts}") 

#             if not executive.assigned_accounts:
#                 executive.assigned_accounts = [] 

#             executive.assigned_accounts.append(client.client_id)
            
#             print(f"After update (executive {executive.executive_id}): {executive.assigned_accounts}")  

#             db.session.execute(
#                 AccountExecutive.__table__.update().
#                 where(AccountExecutive.executive_id == executive.executive_id).
#                 values(assigned_accounts=executive.assigned_accounts)
#             )

#             db.session.commit()

#         return jsonify({"message": "Client added successfully", "client_id": client.client_id}), 201

#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({"message": "Client already exists"}), 400
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": f"An error occurred: {e}"}), 500

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




@app.route('/signingsChart', methods=['GET'])
def signingsChart():
    try:
        results = db.session.query(Signing.forecast_category, func.count()).group_by(Signing.forecast_category).all()
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/pipeline-table-data', methods=['GET'])
def pipeline_table_data():
    try:
        pipeline_data = []
        for row in Pipeline.query.all():
            pipeline_data.append({
                "opportunity_id": row.opportunity_id,
                "account_name": row.account_name,
                "opportunity_value": row.opportunity_value,
                "forecast_category": row.forecast_category,
                "probability": row.probability,
                "close_date": row.expected_close_date,
                "stage": row.stage
            })
        return jsonify(pipeline_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    
@app.route('/pipeline-chart-data', methods=['GET'])
def pipeline_chart_data():
    try:
        results = db.session.query(Pipeline.probability, func.count()).group_by(Pipeline.probability).all()
        chart_data = [{"probability": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

# -----------------------------
# Count-to-wins API endpoints

@app.route('/wins-rows', methods=['GET'])
def get_wins():
    try:
        # Validate win_status parameter
        win_status = request.args.get('win_status', type=str)
        if win_status and win_status.lower() not in ["true", "false", "all"]:
            return jsonify({"error": "win_status must be 'true', 'false', or 'all'"}), 400

        # Validate date parameters
        start_date = request.args.get('start_date', type=str)
        end_date = request.args.get('end_date', type=str)
        
        # Parse and validate dates
        start_date_obj = None
        end_date_obj = None
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
                
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        
        # Ensure start_date <= end_date if both are provided
        if start_date_obj and end_date_obj and start_date_obj > end_date_obj:
            return jsonify({"error": "start_date cannot be after end_date"}), 400
        
        # Validate numeric parameters
        lower_bound = request.args.get('lower_bound', type=float)
        upper_bound = request.args.get('upper_bound', type=float)
        
        if lower_bound is not None and lower_bound < 0:
            return jsonify({"error": "lower_bound cannot be negative"}), 400
            
        if upper_bound is not None and upper_bound < 0:
            return jsonify({"error": "upper_bound cannot be negative"}), 400
            
        if lower_bound is not None and upper_bound is not None and lower_bound > upper_bound:
            return jsonify({"error": "lower_bound cannot be greater than upper_bound"}), 400
        
        # Get other parameters with proper typing
        account_name = request.args.get('account_name', type=str)
        industry = request.args.get('industry', type=str)
        account_type = request.args.get('account_type', type=str)
        forecast_category = request.args.get('forecast_category', type=str)
        account_executive = request.args.get('account_executive', type=int)
        
        # Validate forecast_category against allowed values (case-insensitive)
        valid_forecast_categories = ["commit", "omit", "upside", "pipeline"]
        if forecast_category and forecast_category.lower() not in valid_forecast_categories:
            return jsonify({"error": f"forecast_category must be one of: Commit, Omit, Upside, Pipeline"}), 400
        
        # Start building the query
        query = Win.query
        
        # Apply filters safely (note the use of parameter binding for LIKE queries)
        if account_name:
            # Use parameter binding for safety against SQL injection
            query = query.filter(Win.account_name.ilike("%" + account_name + "%"))
        
        if win_status and win_status.lower() != "all":
            query = query.filter(Win.is_win == (win_status.lower() == "true"))
        
        if start_date_obj:
            query = query.filter(Win.win_date >= start_date_obj)
            
        if end_date_obj:
            query = query.filter(Win.win_date <= end_date_obj)
            
        if industry:
            # Use parameter binding for safety against SQL injection
            query = query.filter(Win.industry.ilike("%" + industry + "%"))
            
        if account_type:
            # Use parameter binding for safety against SQL injection
            query = query.filter(Win.account_type.ilike("%" + account_type + "%"))
            
        if lower_bound is not None:
            query = query.filter(Win.deal_value >= lower_bound)
            
        if upper_bound is not None:
            query = query.filter(Win.deal_value <= upper_bound)
            
        if forecast_category:
            # Case-insensitive comparison for forecast_category
            query = query.filter(func.lower(Win.forecast_category) == forecast_category.lower())
            
        if account_executive:
            query = query.filter(Win.account_executive == account_executive)
        
        # Execute the query
        wins = query.all()
        
        # Convert to JSON-serializable format
        win_list = []
        for win in wins:
            win_list.append({
                "opportunity_id": win.opportunity_id,
                "account_name": win.account_name,
                "win_date": win.win_date.strftime("%Y-%m-%d"),
                "industry": win.industry,
                "account_type": win.account_type,
                "deal_value": win.deal_value,
                "forecast_category": win.forecast_category,
                "is_win": win.is_win
            })
        
        return jsonify(win_list), 200
        
    except Exception as e:
        # Log the error for debugging
        import traceback
        traceback.print_exc()
        
        # Return a generic error message to the client
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/wins-average-deal-size', methods=['GET'])
def get_average_deal_size():
    try:
        # Query to sum the deal values where is_win is True
        total_deal_value = db.session.query(db.func.sum(Win.deal_value)).filter(Win.is_win == True).scalar()

        # Query to count the number of wins (where is_win is True)
        total_wins = db.session.query(db.func.count(Win.opportunity_id)).filter(Win.is_win == True).scalar()

        # Calculate Average Deal Size (avoid division by zero)
        average_deal_size = total_deal_value / total_wins if total_wins > 0 else 0

        # Return the result
        return jsonify({
            "average_deal_size": round(average_deal_size, 2),  # Round to 2 decimal places
            "total_deal_value": total_deal_value,
            "total_wins": total_wins
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors
    
@app.route('/wins-win-rate', methods=['GET'])
def get_win_rate():
    try:
        # Query to count the total number of wins (where is_win is True)
        total_wins = db.session.query(db.func.count(Win.opportunity_id)).filter(Win.is_win == True).scalar()

        # Query to count the total number of opportunities (all rows in the wins table)
        total_opportunities = db.session.query(db.func.count(Win.opportunity_id)).scalar()

        # Calculate Win Rate (avoid division by zero)
        win_rate = (total_wins / total_opportunities) * 100 if total_opportunities > 0 else 0

        # Return the result
        return jsonify({
            "win_rate": round(win_rate, 2),  # Percentage rounded to 2 decimal places
            "total_wins": total_wins,
            "total_opportunities": total_opportunities
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

@app.route('/wins-open-opportunities', methods=['GET'])
@jwt_required()
def get_open_opportunities():
    try:
        # Query to count the total number of open opportunities (where is_win is False)
        total_open_opportunities = db.session.query(db.func.count(Win.opportunity_id)).filter(Win.is_win == False).scalar()

        # Return the result
        return jsonify({
            "open_opportunities": total_open_opportunities
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors


@app.route('/wins-opportunities-by-industry', methods=['GET'])
def get_wins_opportunities_by_industry():
    try:
        # Query to count wins (is_win == True) grouped by industry
        wins_by_industry = (
            db.session.query(Win.industry, db.func.count().label("win_count"))
            .filter(Win.is_win == True)
            .group_by(Win.industry)
            .all()
        )

        # Query to count open opportunities (is_win == False) grouped by industry
        opportunities_by_industry = (
            db.session.query(Win.industry, db.func.count().label("opportunity_count"))
            .filter(Win.is_win == False)
            .group_by(Win.industry)
            .all()
        )

        # Convert query results to dictionaries
        wins_dict = {industry: count for industry, count in wins_by_industry}
        opportunities_dict = {industry: count for industry, count in opportunities_by_industry}

        # Get all industries from both queries
        all_industries = set(wins_dict.keys()).union(set(opportunities_dict.keys()))

        # Construct the response
        industry_data = [
            {
                "industry": industry,
                "wins": wins_dict.get(industry, 0),  # Default to 0 if no wins
                "opportunities": opportunities_dict.get(industry, 0)  # Default to 0 if no opportunities
            }
            for industry in all_industries
        ]

        return jsonify(industry_data), 200  # Return JSON data

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

@app.route('/wins-over-time', methods=['GET'])
def get_wins_over_time():
    try:
        # Get the year parameter from the request (default to the current year if not provided)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Query to count confirmed wins (is_win == True) grouped by month
        confirmed_wins = (
            db.session.query(
                db.func.extract('month', Win.win_date).label("month"),
                db.func.count().label("confirmed_wins")
            )
            .filter(db.func.extract('year', Win.win_date) == year, Win.is_win == True)
            .group_by(db.func.extract('month', Win.win_date))
            .all()
        )

        # Query to count potential wins (is_win == False) grouped by month
        potential_wins = (
            db.session.query(
                db.func.extract('month', Win.win_date).label("month"),
                db.func.count().label("potential_wins")
            )
            .filter(db.func.extract('year', Win.win_date) == year, Win.is_win == False)
            .group_by(db.func.extract('month', Win.win_date))
            .all()
        )

        # Convert query results to dictionaries
        confirmed_wins_dict = {int(month): count for month, count in confirmed_wins}
        potential_wins_dict = {int(month): count for month, count in potential_wins}

        # Ensure all months (1-12) are included, even if no data exists
        monthly_data = [
            {
                "month": month,
                "confirmed_wins": confirmed_wins_dict.get(month, 0),  # Default to 0 if no wins
                "potential_wins": potential_wins_dict.get(month, 0)  # Default to 0 if no opportunities
            }
            for month in range(1, 13)  # Ensure all months from January (1) to December (12) are present
        ]

        return jsonify(monthly_data), 200  # Return JSON data

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors


@app.route('/wins-distribution-by-forecast-category', methods=['GET'])
def get_wins_distribution_by_forecast_category():
    try:
        # Get the year parameter from the request (default to the current year if not provided)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Ensure all forecast categories (commit, omit, upside, pipeline) are included
        valid_categories = ["Commit", "Omit", "Upside", "Pipeline"]

        # Query to count wins grouped by forecast category for the given year
        wins_by_forecast_category = (
            db.session.query(
                db.func.coalesce(Win.forecast_category, 'Unknown').label("forecast_category"),
                db.func.count().label("win_count")
            )
            .filter(
                db.func.extract('year', Win.win_date) == year,
                Win.is_win == True,
                Win.forecast_category.in_(valid_categories)  # Ensure only valid categories are included
            )
            .group_by(Win.forecast_category)
            .all()
        )

        # Convert query results to a dictionary
        forecast_category_dict = {category: 0 for category in valid_categories}  # Initialize all categories with 0

        for forecast_category, count in wins_by_forecast_category:
            forecast_category_dict[forecast_category] = count  # Assign counted values

        # Convert to list format for JSON response
        forecast_category_data = [
            {
                "forecast_category": category,
                "win_count": forecast_category_dict[category]
            }
            for category in valid_categories
        ]

        return jsonify(forecast_category_data), 200  # Return JSON data

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors
# -----------------------------

# -----------------------------
# Performance metrics endpoints

@app.route('/quarterly-revenue-performance-ae', methods=['GET'])
def get_quarterly_revenue_performance_ae():
    try:
        # Extract query parameters
        quarter = request.args.get('quarter', type=int)
        executive_id = request.args.get('id', type=int)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Validate inputs
        if not all([quarter, executive_id]):
            return jsonify({"message": "Missing required parameters"}), 400

        if quarter not in [1, 2, 3, 4]:
            return jsonify({"message": "Invalid quarter. Must be 1, 2, 3, or 4"}), 400

        if executive_id <= 0:
            return jsonify({"message": "Invalid account executive ID. Must be a positive integer"}), 400

        # Define date ranges for each quarter
        quarter_end_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        start_date = datetime(year, 1, 1).date()
        end_date = quarter_end_dates[quarter]

        print(f"Querying revenue from {start_date} to {end_date} for executive ID: {executive_id}")

        # Step 1: Find all client accounts assigned to the specified account executive
        client_accounts = db.session.query(Client.client_id).filter_by(executive_id=executive_id).all()
        client_ids = [account[0] for account in client_accounts]

        if not client_ids:
            # No clients assigned to this account executive
            return jsonify({
                "metric": "revenue",
                "quarter": quarter,
                "year": year,
                "amount": 0,
                "percentage": 0
            }), 200

        print(f"Found client IDs: {client_ids}")

        # Step 2: Calculate total revenue from these clients within the date range
        total_revenue = db.session.query(db.func.sum(Revenue.total_revenue)).\
            filter(Revenue.opportunity_id.in_(client_ids)).\
            filter(Revenue.revenue_date >= start_date).\
            filter(Revenue.revenue_date <= end_date).\
            scalar() or 0

        print(f"Total Revenue Query Result: {total_revenue}")

        # Step 3: Calculate percentage of target achieved
        # Determine annual target for this executive
        if executive_id == 1:
            annual_target = 20000000
        elif executive_id == 2:
            annual_target = 27000000
        elif 3 <= executive_id <= 7:
            annual_target = 2500000
        else:
            # For other executives, use a default value or return an error
            return jsonify({"message": "Invalid account executive ID"}), 400
        
        # Define quarterly target percentages
        quarter_percentages = {1: 0.1, 2: 0.2, 3: 0.25, 4: 0.45}
        
        # Calculate quarterly target amount
        quarterly_target = annual_target * quarter_percentages[quarter]
        
        # Calculate percentage achieved (avoid division by zero)
        percentage_achieved = (total_revenue / quarterly_target * 100) if quarterly_target > 0 else 0
        
        # Return the performance data
        return jsonify({
            "metric": "revenue",
            "quarter": quarter,
            "year": year,
            "amount": round(total_revenue, 2),
            "percentage": round(percentage_achieved, 2)
        }), 200

    except Exception as e:
        print(f"Error in /quarterly-revenue-performance-ae endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({"message": f"An error occurred: {e}"}), 500
    

@app.route('/quarterly-revenue-performance-dir', methods=['GET'])
def get_quarterly_revenue_performance_dir():
    try:
        # Extract query parameters
        quarter = request.args.get('quarter', type=int)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Validate inputs
        if not quarter:
            return jsonify({"message": "Missing required quarter parameter"}), 400

        if quarter not in [1, 2, 3, 4]:
            return jsonify({"message": "Invalid quarter. Must be 1, 2, 3, or 4"}), 400

        # Define date ranges for each quarter
        quarter_end_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        start_date = datetime(year, 1, 1).date()
        end_date = quarter_end_dates[quarter]

        print(f"Querying revenue from {start_date} to {end_date}")

        # Calculate total revenue across all accounts within the date range
        # using parameterized queries
        total_revenue = db.session.query(db.func.sum(Revenue.total_revenue)).\
            filter(Revenue.revenue_date >= start_date).\
            filter(Revenue.revenue_date <= end_date).\
            scalar() or 0
        
        print(f"Total Revenue Query Result: {total_revenue}")

        # Define director's annual target
        annual_target = 59500000  # 59.5M

        # Define quarterly target percentages
        quarter_percentages = {1: 0.1, 2: 0.2, 3: 0.25, 4: 0.45}
        
        # Calculate quarterly target amount
        quarterly_target = annual_target * quarter_percentages[quarter]
        
        # Calculate percentage achieved (avoid division by zero)
        percentage_achieved = (total_revenue / quarterly_target * 100) if quarterly_target > 0 else 0
        
        # Return the performance data
        return jsonify({
            "metric": "revenue",
            "quarter": quarter,
            "year": year,
            "amount": round(total_revenue, 2),
            "percentage": round(percentage_achieved, 2)
        }), 200

    except Exception as e:
        print(f"Error in /quarterly-revenue-performance-dir endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({"message": f"An error occurred: {e}"}), 500


@app.route('/quarterly-signings-performance-ae', methods=['GET'])
def get_quarterly_signings_performance_ae():
    try:
        # Extract query parameters
        quarter = request.args.get('quarter', type=int)
        executive_id = request.args.get('id', type=int)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Validate inputs
        if not all([quarter, executive_id]):
            return jsonify({"message": "Missing required parameters"}), 400

        if quarter not in [1, 2, 3, 4]:
            return jsonify({"message": "Invalid quarter. Must be 1, 2, 3, or 4"}), 400

        if executive_id <= 0:
            return jsonify({"message": "Invalid account executive ID. Must be a positive integer"}), 400

        # Define date ranges for each quarter
        quarter_end_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        start_date = datetime(year, 1, 1).date()
        end_date = quarter_end_dates[quarter]

        print(f"Querying signings from {start_date} to {end_date} for executive ID: {executive_id}")

        # Step 1: Find all client accounts assigned to the specified account executive
        client_accounts = db.session.query(Client.client_id).filter_by(executive_id=executive_id).all()
        client_ids = [account[0] for account in client_accounts]

        if not client_ids:
            # No clients assigned to this account executive
            return jsonify({
                "metric": "signings",
                "quarter": quarter,
                "year": year,
                "amount": 0,
                "percentage": 0
            }), 200

        print(f"Found client IDs: {client_ids}")

        # Step 2: Calculate total signings from these clients within the date range
        total_signings = db.session.query(db.func.sum(Signing.incremental_acv)).\
            filter(Signing.opportunity_id.in_(client_ids)).\
            filter(Signing.signing_date >= start_date).\
            filter(Signing.signing_date <= end_date).\
            scalar() or 0

        print(f"Total Signings Query Result: {total_signings}")

        # Step 3: Calculate percentage of target achieved
        # Determine annual target for this executive
        if executive_id == 1 or executive_id == 2:
            annual_target = 5000000  # 5M
        elif 3 <= executive_id <= 7:
            annual_target = 1000000  # 1M
        else:
            # For other executives, use a default value or return an error
            return jsonify({"message": "Invalid account executive ID"}), 400
        
        # Define quarterly target percentages
        quarter_percentages = {1: 0.1, 2: 0.2, 3: 0.25, 4: 0.45}
        
        # Calculate quarterly target amount
        quarterly_target = annual_target * quarter_percentages[quarter]
        
        # Calculate percentage achieved (avoid division by zero)
        percentage_achieved = (total_signings / quarterly_target * 100) if quarterly_target > 0 else 0
        
        # Return the performance data
        return jsonify({
            "metric": "signings",
            "quarter": quarter,
            "year": year,
            "amount": round(total_signings, 2),
            "percentage": round(percentage_achieved, 2)
        }), 200

    except Exception as e:
        print(f"Error in /quarterly-signings-performance-ae endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({"message": f"An error occurred: {e}"}), 500        
            
    
@app.route('/quarterly-signings-performance-dir', methods=['GET'])
def get_quarterly_signings_performance_dir():
    try:
        # Extract query parameters
        quarter = request.args.get('quarter', type=int)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Validate inputs
        if not quarter:
            return jsonify({"message": "Missing required quarter parameter"}), 400

        if quarter not in [1, 2, 3, 4]:
            return jsonify({"message": "Invalid quarter. Must be 1, 2, 3, or 4"}), 400

        # Define date ranges for each quarter
        quarter_end_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        start_date = datetime(year, 1, 1).date()
        end_date = quarter_end_dates[quarter]

        print(f"Querying signings from {start_date} to {end_date}")

        # Calculate total incremental ACV across all signings within the date range
        total_signings = db.session.query(db.func.sum(Signing.incremental_acv)).\
            filter(Signing.signing_date >= start_date).\
            filter(Signing.signing_date <= end_date).\
            scalar() or 0
        
        print(f"Total Signings Query Result: {total_signings}")

        # Define director's annual target for signings
        annual_target = 15000000  # 15M

        # Define quarterly target percentages
        quarter_percentages = {1: 0.1, 2: 0.2, 3: 0.25, 4: 0.45}
        
        # Calculate quarterly target amount
        quarterly_target = annual_target * quarter_percentages[quarter]
        
        # Calculate percentage achieved (avoid division by zero)
        percentage_achieved = (total_signings / quarterly_target * 100) if quarterly_target > 0 else 0
        
        # Return the performance data
        return jsonify({
            "metric": "signings",
            "quarter": quarter,
            "year": year,
            "amount": round(total_signings, 2),
            "percentage": round(percentage_achieved, 2)
        }), 200

    except Exception as e:
        print(f"Error in /quarterly-signings-performance-dir endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({"message": f"An error occurred: {e}"}), 500
    

@app.route('/quarterly-cows-performance-ae', methods=['GET'])
def get_quarterly_cows_performance_ae():
    try:
        # Extract query parameters
        quarter = request.args.get('quarter', type=int)
        executive_id = request.args.get('id', type=int)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Validate inputs
        if not all([quarter, executive_id]):
            return jsonify({"message": "Missing required parameters"}), 400

        if quarter not in [1, 2, 3, 4]:
            return jsonify({"message": "Invalid quarter. Must be 1, 2, 3, or 4"}), 400

        if executive_id <= 0:
            return jsonify({"message": "Invalid account executive ID. Must be a positive integer"}), 400
            
        if year <= 0:
            return jsonify({"message": "Invalid year. Must be a positive integer"}), 400

        # Define date ranges for each quarter
        quarter_end_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        start_date = datetime(year, 1, 1).date()
        end_date = quarter_end_dates[quarter]

        print(f"Querying wins from {start_date} to {end_date} for executive ID: {executive_id}")

        # Step 1: Find all client accounts assigned to the specified account executive
        client_accounts = db.session.query(Client.client_id).filter_by(executive_id=executive_id).all()
        client_ids = [str(account[0]) for account in client_accounts]  # Convert to strings to match opportunity_id

        if not client_ids:
            # No clients assigned to this account executive
            return jsonify({
                "metric": "wins",
                "quarter": quarter,
                "year": year,
                "amount": 0,
                "percentage": 0
            }), 200

        print(f"Found client IDs: {client_ids}")

        # Step 2: Count wins from these clients within the date range where is_win = True
        win_count = db.session.query(db.func.count(Win.opportunity_id)).\
            filter(Win.opportunity_id.in_(client_ids)).\
            filter(Win.is_win == True).\
            filter(Win.win_date >= start_date).\
            filter(Win.win_date <= end_date).\
            scalar() or 0

        print(f"Win Count Query Result: {win_count}")

        # Step 3: Calculate percentage of target achieved
        # Determine annual target for this executive
        if executive_id == 1 or executive_id == 2:
            annual_target = 0  # No target for executives 1 and 2
            percentage_achieved = 0  # Can't calculate percentage if target is 0
        elif 3 <= executive_id <= 7:
            annual_target = 10  # Target of 10 wins for executives 3-7
            
            # Define quarterly target percentages
            quarter_percentages = {1: 0.1, 2: 0.2, 3: 0.25, 4: 0.45}
            
            # Calculate quarterly target amount
            quarterly_target = annual_target * quarter_percentages[quarter]
            
            # Calculate percentage achieved (avoid division by zero)
            percentage_achieved = (win_count / quarterly_target * 100) if quarterly_target > 0 else 0
        else:
            # For other executives, use a default value or return an error
            return jsonify({"message": "Invalid account executive ID"}), 400
        
        # Return the performance data
        return jsonify({
            "metric": "wins",
            "quarter": quarter,
            "year": year,
            "amount": win_count,
            "percentage": round(percentage_achieved, 2)
        }), 200

    except Exception as e:
        print(f"Error in /quarterly-cows-performance-ae endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/quarterly-cows-performance-dir', methods=['GET'])
def get_quarterly_cows_performance_dir():
    try:
        # Extract query parameters
        quarter = request.args.get('quarter', type=int)
        year = request.args.get('year', type=int, default=datetime.now().year)

        # Validate inputs
        if not quarter:
            return jsonify({"message": "Missing required quarter parameter"}), 400

        if quarter not in [1, 2, 3, 4]:
            return jsonify({"message": "Invalid quarter. Must be 1, 2, 3, or 4"}), 400
            
        if year <= 0:
            return jsonify({"message": "Invalid year. Must be a positive integer"}), 400

        # Define date ranges for each quarter
        quarter_end_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        start_date = datetime(year, 1, 1).date()
        end_date = quarter_end_dates[quarter]

        print(f"Querying wins from {start_date} to {end_date} for director")

        # Count all wins within the date range where is_win = True
        win_count = db.session.query(db.func.count(Win.opportunity_id)).\
            filter(Win.is_win == True).\
            filter(Win.win_date >= start_date).\
            filter(Win.win_date <= end_date).\
            scalar() or 0

        print(f"Win Count Query Result: {win_count}")

        # Calculate percentage of target achieved
        # Define director's annual target
        annual_target = 50  # 50 wins per year
        
        # Define quarterly target percentages
        quarter_percentages = {1: 0.1, 2: 0.2, 3: 0.25, 4: 0.45}
        
        # Calculate quarterly target amount
        quarterly_target = annual_target * quarter_percentages[quarter]
        
        # Calculate percentage achieved (avoid division by zero)
        percentage_achieved = (win_count / quarterly_target * 100) if quarterly_target > 0 else 0
        
        # Return the performance data
        return jsonify({
            "metric": "wins",
            "quarter": quarter,
            "year": year,
            "amount": win_count,
            "percentage": round(percentage_achieved, 2)
        }), 200

    except Exception as e:
        print(f"Error in /quarterly-cows-performance-dir endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({"message": f"An error occurred: {e}"}), 500        
    
# ----------------------


if __name__ == '__main__':
    app.run(debug=True)