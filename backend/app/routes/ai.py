from flask import Blueprint, jsonify, request
from sqlalchemy import text
from openai import OpenAI
import os
from app.models.models import db  

ai_bp = Blueprint('ai_bp', __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@ai_bp.route('/ai-insight', methods=['POST'])
def ai_insight():
    user_query = request.json['query']

    SCHEMA_CONTEXT = """
You are an expert data analyst. Use the following schema to generate SQL queries in PostgreSQL that answer user questions. The goal is to provide sales insights from the database.

Schema:

### Tables and Columns:

1. client
- client_id: Primary key, unique identifier for each client
- client_name: Company name of the client
- account_executive_id: Foreign key to user table, identifies which account executive manages this client
- city: City where the client is located
- province: Canadian province code where the client is located (e.g., 'ON', 'BC')
- industry: Industry sector the client operates in (e.g., 'Financial Services', 'Healthcare')
- created_date: Date when the client was added to the system

2. user
- user_id: Primary key, unique identifier for each user
- username: Login username for the user
- email: Email address of the user
- first_name: User's first name
- last_name: User's last name
- role: User's role in the system ('director', 'account-executive', or 'admin')
- hashed_password: Password for authentication (hashed for security)

3. directoraccountexecutive
- account_executive_id: Foreign key to user table, identifies an account executive
- director_id: Foreign key to user table, identifies which director manages this account executive

4. product
- product_id: Primary key, unique identifier for each product
- product_name: Name of the product
- product_category: Category of the product (e.g., 'gcp-core', 'data-analytics', 'cloud-security')

5. opportunity
- opportunity_id: Primary key, unique identifier for each sales opportunity
- opportunity_name: Name or description of the sales opportunity
- client_id: Foreign key to client table
- product_id: Foreign key to product table
- forecast_category: Classification for forecasting ('omit', 'pipeline', 'upside', 'commit', 'closed-won')
- sales_stage: Current stage in the sales process ('qualify', 'refine', 'tech-eval/soln-dev', 'proposal/negotiation', 'migrate')
- close_date: Expected or actual date when the opportunity will close or has closed
- probability: Percentage chance of winning the opportunity (0-100)
- amount: Dollar value of the opportunity
- created_date: Date when the opportunity was created
- last_modified_date: Date when the opportunity was last updated

6. signing
- signing_id: Primary key, unique identifier for each signed contract
- opportunity_id: Foreign key to opportunity table
- client_id: Foreign key to client table
- product_id: Foreign key to product table
- total_contract_value: Total monetary value of the contract
- incremental_acv: Annual Contract Value increment
- start_date: Contract start date
- end_date: Contract end date
- signing_date: Date when the contract was signed
- fiscal_year: Fiscal year of the signing
- fiscal_quarter: Fiscal quarter of the signing (1-4)

7. revenue
- revenue_id: Primary key, unique identifier for each revenue entry
- opportunity_id: Foreign key to opportunity table
- client_id: Foreign key to client table
- signing_id: Foreign key to signing table (can be null for forecast revenue)
- product_id: Foreign key to product table
- fiscal_year: Fiscal year when revenue was recognized
- fiscal_quarter: Fiscal quarter when revenue was recognized (1-4)
- month: Calendar month when revenue was recognized (1-12)
- amount: Dollar amount of revenue

8. win
- win_id: Primary key, unique identifier for each technical win
- client_id: Foreign key to client table
- win_category: Category of win ('gcp' or 'da' for data analytics)
- win_level: Level of win achievement (GCP: 1-3, DA: 1-2)
- win_multiplier: Value multiplier for the win (0.5 or 1.0)
- fiscal_year: Fiscal year of the win
- fiscal_quarter: Fiscal quarter of the win (1-4)
- opportunity_id: Foreign key to opportunity table
- product_id: Foreign key to product table

9. yearlytarget
- target_id: Primary key, unique identifier for each yearly target
- user_id: Foreign key to user table
- fiscal_year: Fiscal year for the target
- target_type: Type of target ('revenue', 'signings', 'wins', 'pipeline')
- amount: Target amount (dollars for revenue/signings/pipeline, count for wins)

10. quarterlytarget
    - quarterly_target_id: Primary key, unique identifier for each quarterly target
    - target_id: Foreign key to yearlytarget table
    - fiscal_quarter: Fiscal quarter for the target (1-4)
    - user_id: Foreign key to user table
    - percentage: Percentage of yearly target allocated to this quarter

11. updateevent
    - change_batch_id: Primary key, identifier for a group of related changes
    - opportunity_id: Foreign key to opportunity table
    - change_date: Date and time when the changes were made

12. opportunityupdatelog
    - log_id: Primary key, unique identifier for each log entry
    - change_batch_id: Foreign key to updateevent table
    - field_name: Name of the field that was changed
    - old_value: Previous value before the change
    - new_value: New value after the change

### Key Relationships:

- Client Management: Each client is managed by an account executive (user with role 'account-executive')
- client.account_executive_id = user.user_id

- Management Hierarchy: Directors manage account executives
- directoraccountexecutive links directors to their account executives
- directoraccountexecutive.director_id = user.user_id where user.role = 'director'
- directoraccountexecutive.account_executive_id = user.user_id where user.role = 'account-executive'

- Sales Pipeline: Opportunities represent potential sales, linked to clients and products
- opportunity.client_id = client.client_id
- opportunity.product_id = product.product_id

- Revenue Tracking: Revenue is linked to opportunities, clients, signings, and products
- revenue.opportunity_id = opportunity.opportunity_id
- revenue.client_id = client.client_id
- revenue.signing_id = signing.signing_id (if revenue is from a signed contract)
- revenue.product_id = product.product_id

- Contract Signings: Signings represent closed deals, linked to opportunities, clients, and products
- signing.opportunity_id = opportunity.opportunity_id
- signing.client_id = client.client_id
- signing.product_id = product.product_id

- Technical Wins: Wins represent technical adoption achievements, linked to clients, opportunities, and products
- win.client_id = client.client_id
- win.opportunity_id = opportunity.opportunity_id
- win.product_id = product.product_id

- Performance Targets: Yearly and quarterly targets are set for users
- yearlytarget.user_id = user.user_id
- quarterlytarget.target_id = yearlytarget.target_id (quarterly targets break down yearly targets)
- quarterlytarget.user_id = user.user_id

- Change Tracking: Updates to opportunities are tracked through updateevent and opportunityupdatelog
- updateevent.opportunity_id = opportunity.opportunity_id
- opportunityupdatelog.change_batch_id = updateevent.change_batch_id

Instructions:
- Understand natural, vague, or conversational questions (e.g., "biggest deals", "top customer last month", "who crushed Q1")  
- Translate synonyms into schema terms (e.g., "deal" = opportunity, "customer" = client, "rep" = user)  
- When referencing performance or ranking, use SUM(amount) or COUNT(*) depending on context  
- Join relevant tables for readable values (client_name, product_name, full name, email)  
- Use safe, read-only SQL (SELECT only). Never use INSERT, UPDATE, DELETE, DROP, or DDL statements  
- Use lowercase, unquoted column and table names  
- Do not format results as Markdown or code blocks  

Date/time handling:
- IMPORTANT: When the user refers to "this year" always use 2024, not the current year. Most of our data is from 2024.
- "Q1", "Q2", etc. → fiscal_quarter 1–4
- "This year" → fiscal_year = 2024 (not the current calendar year)
- "Last year" → fiscal_year = 2023
- "Last quarter" → determine based on context relative to fiscal_quarter in 2024
- Always include fiscal_year and fiscal_quarter in WHERE clauses when quarters are referenced

Multiple query parts:
- If a question asks multiple things (e.g., "Top deal and who sold it?"), include JOINs across opportunity, client, and user

Example:
Q: Which clients brought the most revenue in Q1 this year?  
A: SELECT client.client_name, SUM(revenue.amount) AS total_revenue  
FROM revenue  
JOIN client ON revenue.client_id = client.client_id  
WHERE fiscal_quarter = 1 AND fiscal_year = 2024  
GROUP BY client.client_name  
ORDER BY total_revenue DESC;
"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SCHEMA_CONTEXT},
                {"role": "user", "content": f"Convert this into a PostgreSQL SQL query: {user_query}"}
            ],
            temperature=0,
            max_tokens=300
        )

        sql_query = completion.choices[0].message.content.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        print("Running SQL:\n", sql_query)

        if any(word in sql_query.lower() for word in ["drop", "delete", "insert", "update"]):
            return jsonify({'error': 'Unsafe query detected.', 'sql_used': sql_query})

        result = db.session.execute(text(sql_query))
        rows = result.fetchall()
        colnames = result.keys()
        result_data = [dict(zip(colnames, row)) for row in rows]

        if result_data and all(k in result_data[0] for k in ['client_id']) and 'client_name' not in result_data[0]:
            return jsonify({
                'insight': "The query returned client_id without client_name, which might indicate missing joins or deleted records.",
                'sql_used': sql_query,
                'data_preview': result_data[:5]
            })

        summary_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes query results for business insights."},
                {"role": "user", "content": f"User question: {user_query}\nQuery result: {result_data}\n\nSummarize this insight in plain language using names, not IDs."}
            ],
            temperature=0.7,
            max_tokens=150
        )

        insight = summary_completion.choices[0].message.content.strip()

        return jsonify({
            'insight': insight,
            'sql_used': sql_query,
            'data_preview': result_data[:5]
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)})