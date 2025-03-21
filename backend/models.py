from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Pipeline(db.Model):
    __tablename__ = 'pipeline'
    account_name = db.Column(db.String(255), nullable=False)
    opportunity_id = db.Column(db.Integer, primary_key=True)
    forecast_category = db.Column(db.String(50), nullable=False)
    opportunity_value = db.Column(db.Float, nullable=False)
    expected_close_date = db.Column(db.Date, nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    probability = db.Column(db.Float, nullable=False)

class Revenue(db.Model):
    __tablename__ = 'revenue'
    opportunity_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(255), nullable=False)
    revenue_type = db.Column(db.String(50), nullable=False)
    total_revenue = db.Column(db.Float, nullable=False)
    iacv = db.Column(db.Float, nullable=True)

class Win(db.Model):
    __tablename__ = 'wins'
    opportunity_id = db.Column(db.String, primary_key=True)  
    account_name = db.Column(db.String(255), nullable=False)
    win_date = db.Column(db.Date, nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    deal_value = db.Column(db.Float, nullable=False)
    forecast_category = db.Column(db.String(50), nullable=False)  
    is_win = db.Column(db.Boolean, nullable=False)  


class Signing(db.Model):
    __tablename__ = 'signings'
    account_name = db.Column(db.String(255), nullable=False)
    opportunity_id = db.Column(db.Integer, primary_key=True)
    months = db.Column(db.String(20), nullable=False)
    incremental_acv = db.Column(db.Float, nullable=False)
    forecast_category = db.Column(db.String(50), nullable=False)
    signing_date = db.Column(db.Date, nullable=False)




class AccountExecutive(db.Model):
    __tablename__ = 'account_executives'
    executive_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    assigned_accounts = db.Column(db.JSON, nullable=False, default=[])  # Updated to JSON
    performance_metrics = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True)
    executive_id = db.Column(db.Integer, db.ForeignKey('account_executives.executive_id'), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)