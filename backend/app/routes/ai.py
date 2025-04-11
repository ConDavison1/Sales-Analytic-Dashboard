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

    client(client_id, client_name, account_executive_id, city, province, industry, created_date)  
    directoraccountexecutive(account_executive_id, director_id)  
    opportunity(opportunity_id, opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)  
    opportunityupdatelog(log_id, change_batch_id, field_name, old_value, new_value)  
    product(product_id, product_name, product_category)  
    quarterlytarget(quarterly_target_id, target_id, fiscal_quarter, user_id, percentage)  
    revenue(revenue_id, opportunity_id, client_id, signing_id, fiscal_year, fiscal_quarter, month, amount, product_id)  
    signing(signing_id, opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)  
    updateevent(change_batch_id, opportunity_id, change_date)  
    user(user_id, username, email, first_name, last_name, role, hashed_password)  
    win(win_id, client_id, win_category, win_level, win_multiplier, fiscal_year, fiscal_quarter, opportunity_id, product_id)  
    yearlytarget(target_id, user_id, fiscal_year, target_type, amount)

    Relationships:
    - Each client is managed by a user (account executive) via client.account_executive_id = user.user_id  
    - Each opportunity belongs to a client and a product  
    - Revenue is tied to opportunities, clients, and products  
    - Signings and wins are tied to opportunities, clients, and products  
    - Quarterly and yearly targets are tied to users via user_id  
    - Use user.email and CONCAT(first_name, ' ', last_name) for readable names

    Instructions:
    - Understand natural, vague, or conversational questions (e.g., “biggest deals”, “top customer last month”, “who crushed Q1”)  
    - Translate synonyms into schema terms (e.g., “deal” = opportunity, “customer” = client, “rep” = user)  
    - When referencing performance or ranking, use SUM(amount) or COUNT(*) depending on context  
    - Join relevant tables for readable values (client_name, product_name, full name, email)  
    - Use safe, read-only SQL (SELECT only). Never use INSERT, UPDATE, DELETE, DROP, or DDL statements  
    - Use lowercase, unquoted column and table names  
    - Do not format results as Markdown or code blocks  

    Date/time handling:
    - “Q1”, “Q2”, etc. → fiscal_quarter 1–4  
    - “This year” → current fiscal_year  
    - “Last year” → fiscal_year - 1  
    - “Last quarter” → fiscal_quarter - 1 (adjust for rollover)  
    - Always include fiscal_year and fiscal_quarter in WHERE clauses when quarters are referenced

    Multiple query parts:
    - If a question asks multiple things (e.g., "Top deal and who sold it?"), include JOINs across opportunity, client, and user

    Example:
    Q: Which clients brought the most revenue in Q1 this year?  
    A: SELECT client.client_name, SUM(revenue.amount) AS total_revenue  
       FROM revenue  
       JOIN client ON revenue.client_id = client.client_id  
       WHERE fiscal_quarter = 1 AND fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)  
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
