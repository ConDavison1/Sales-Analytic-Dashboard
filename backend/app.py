from datetime import timedelta
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
        return jsonify({"wins_count": total}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

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

    
@app.route('/test', methods=['GET'])
def test():
    return "Flask is running!"


if __name__ == '__main__':
    app.run(debug=True)
