from flask import Flask, request, jsonify
from flask_cors import CORS 
import psycopg2 
import uuid  

# Initialize Flask app and enable CORS
app = Flask(__name__) 
CORS(app)  

# Database connection function
def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using psycopg2.
    Connects to the Neon hosted database and returns the connection object.
    """
    connection = psycopg2.connect(
        host="ep-nameless-queen-a53rjqqq.us-east-2.aws.neon.tech",  
        database="neondb",                                        
        user="neondb_owner",                                       
        password="faAnkog7FQ8j",                                   
        sslmode="require"                                         
    )
    return connection

# Define the login route
@app.route('/login', methods=['POST'])
def login():
    
    # Handles login by checking username and password against the database.
    # Returns a token if successful, or an error message otherwise.
    
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[2]  
            if password == stored_password:
                token = str(uuid.uuid4()) 
                return jsonify({"message": "Login successful!", "token": token}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        else:
            return jsonify({"message": "User not found"}), 404

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

import traceback  # Add this for debugging

@app.route('/chart-data', methods=['GET'])
def chart_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query Pipeline
        cursor.execute("""
            SELECT forecast_category, COUNT(*) AS count
            FROM pipeline  
            GROUP BY forecast_category
            ORDER BY forecast_category
        """)
        pipeline_data = [row[1] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT months, SUM(total_revenue)
            FROM revenue  
            GROUP BY months
            ORDER BY months;
        """)

        revenue_data = [row[1] for row in cursor.fetchall()]

        # Query Wins
        cursor.execute("""
            SELECT months, COUNT(*) 
            FROM wins 
            WHERE is_win = TRUE            
            GROUP BY months
            ORDER BY months
        """)
        wins_data = [row[1] for row in cursor.fetchall()]

        # Query Signings
        cursor.execute("""
            SELECT months, SUM(incremental_acv)
            FROM signings 
            GROUP BY months
            ORDER BY months
        """)
        signings_data = [row[1] for row in cursor.fetchall()]

        return jsonify({
            "pipeline": pipeline_data,
            "revenue": revenue_data,
            "wins": wins_data,
            "signings": signings_data
        }), 200

    except Exception as e:
        print("Error in /chart-data:", traceback.format_exc())  # Logs the full error
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()





# Define the signings chart data route
@app.route('/sign-chart-data', methods=['GET'])
def sign_chart_data():
    
    # Retrieves the number of signings clients in each category (Omit, Upside, Pipeline, Commit)
    # and returns the data as JSON for the frontend.
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        cursor.execute("""
                    SELECT forecast_category, COUNT(*) AS count
                    FROM signings  
                    GROUP BY forecast_category
                    ORDER BY forecast_category
                    """)

        results = cursor.fetchall()

        
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

            
@app.route('/revenue-client', methods=['GET'])
def get_revenue_clients():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve data from the database and order by opportunity_id
        cursor.execute("""
        SELECT account_name, revenue_type, total_revenue, iacv
        FROM revenue
        ORDER BY opportunity_id
        """)

        # Fetch all results
        revenue_clients = cursor.fetchall()

        # Process the results into a list of dictionaries
        revenue_clients_data = [
            {
                "account_name": client[0],
                "revenue_type": client[1],
                "total_revenue": client[2],
                "iacv": client[3]
            }
            for client in revenue_clients
        ]
        
        return jsonify(revenue_clients_data), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/account_executives', methods=['GET'])
def account_executives():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT first_name, last_name, assigned_accounts, performance_metrics, status 
            FROM account_executives
        """)
        
        data = cursor.fetchall()
        executives = []

        for row in data:
            first_name, last_name, assigned_accounts, performance_metrics, status = row

            # Convert assigned_accounts from string format to list (assumes it's a valid list in string form)
            assigned_accounts = eval(assigned_accounts) if isinstance(assigned_accounts, str) else assigned_accounts
            number_of_clients = len(assigned_accounts)  # Count the number of clients assigned

            # Parse performance_metrics as JSON
            try:
                performance_metrics = eval(performance_metrics) if isinstance(performance_metrics, str) else performance_metrics
                sales = performance_metrics.get('sales', 0)
                targets = performance_metrics.get('targets', 0)
            except (ValueError, TypeError):
                sales = 0
                targets = 0

            # Calculate the performance percentage
            performance_percentage = targets if targets > 0 else 0

            executives.append({
                "name": f"{first_name} {last_name}",
                "clients": number_of_clients,
                "performance": {
                    "value": f"${sales}",
                    "percentage": performance_percentage,
                    "color": "green" if performance_percentage >= 70 else ("#ffc107" if performance_percentage >= 40 else "red")
                },
                "status": {
                    "value": status,
                    "percentage": 100,
                    "color": "green" if status == "Active" else "red"
                }
            })
        return jsonify(executives), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# Define the Wins table data route
@app.route('/wins-chart-data', methods=['GET'])
def wins_chart_data():
    
    # Retrieves the count of wins in each stage and returns the data as JSON for the frontend.
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        cursor.execute("""
            SELECT stage, COUNT(*) AS count
            FROM wins
            GROUP BY stage
            ORDER BY stage
        """)

        results = cursor.fetchall()

       
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/revenue-chart-data', methods=['GET'])
def revenue_chart_data():
    
    # Retrieves the count of each revenue_type (GCP, Workspace, Other) and returns the data as JSON for the frontend.
   
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN revenue_type IN ('GCP', 'Workspace') THEN revenue_type
                    ELSE 'Other'
                END AS revenue_type,
                COUNT(*) AS count
            FROM revenue
            GROUP BY revenue_type
            ORDER BY revenue_type
        """)

        results = cursor.fetchall()

        
        chart_data = [{"category": row[0], "count": row[1]} for row in results]
        return jsonify(chart_data), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Sum of revenue_amount in the revenue table
@app.route('/revenue-sum', methods=['GET'])
def revenue_sum():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(total_revenue) FROM revenue
        """)
        result = cursor.fetchone()
        return jsonify({"revenue_sum": result[0]}), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Sum of counts in the pipeline table
@app.route('/pipeline-count', methods=['GET'])
def pipeline_count():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(opportunity_value) FROM pipeline
        """)
        result = cursor.fetchone()
        return jsonify({"pipeline_count": result[0]}), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Sum of signings in the signings table
@app.route('/signings-count', methods=['GET'])
def signings_count():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(incremental_acv) FROM signings
        """)
        result = cursor.fetchone()
        return jsonify({"signings_count": result[0]}), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Sum of wins in the wins table
@app.route('/wins-count', methods=['GET'])
def wins_count():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM wins WHERE is_win = TRUE
        """)
        result = cursor.fetchone()
        return jsonify({"wins_count": result[0]}), 200

    except psycopg2.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  
