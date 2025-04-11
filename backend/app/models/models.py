"""
Database Models Module

This module defines all the database models for the application using SQLAlchemy ORM.
Each class represents a table in the database and includes column definitions,
relationships, and helper methods like to_dict() for serialization.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()


class User(db.Model):
    """
    User Model
    
    Represents users of the system with different roles (director, account-executive, admin).
    Used for authentication and authorization.
    """
    __tablename__ = 'user'  # Table name in the database

    # Primary columns
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(20), nullable=False)  # Values: 'director', 'account-executive', 'admin'
    hashed_password = db.Column(db.String(100), nullable=False)  # Not actually hashed for now

    # Relationships
    # Currently commented out to simplify the initial implementation
    # account_executives = db.relationship('DirectorAccountExecutive', 
    #                                      foreign_keys='DirectorAccountExecutive.director_id',
    #                                      backref='director', lazy='dynamic')
    # clients = db.relationship('Client', backref='account_executive', lazy='dynamic')
    # yearly_targets = db.relationship('YearlyTarget', backref='user', lazy='dynamic')
    # quarterly_targets = db.relationship('QuarterlyTarget', backref='user', lazy='dynamic')
    
    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role
        }


class DirectorAccountExecutive(db.Model):
    """
    Director-Account Executive Relationship Model
    
    Maps which account executives report to which directors.
    This model supports the hierarchical management structure.
    """
    __tablename__ = 'directoraccountexecutive'

    # Primary key is the account executive's ID, creating a one-to-one mapping to a director
    account_executive_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    def to_dict(self):
        """Convert relationship to dictionary for API responses"""
        return {
            'account_executive_id': self.account_executive_id,
            'director_id': self.director_id
        }


class Client(db.Model):
    """
    Client Model
    
    Represents client organizations that account executives manage.
    Contains basic information about the client and their location.
    """
    __tablename__ = 'client'

    # Primary columns
    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    account_executive_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    city = db.Column(db.String(50))
    province = db.Column(db.String(2))  # Canadian province code (2 letters)
    industry = db.Column(db.String(50))
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Relationships
    # Currently commented out to simplify the initial implementation
    # opportunities = db.relationship('Opportunity', backref='client', lazy='dynamic')
    # signings = db.relationship('Signing', backref='client', lazy='dynamic')
    # revenue = db.relationship('Revenue', backref='client', lazy='dynamic')
    # wins = db.relationship('Win', backref='client', lazy='dynamic')
    
    def to_dict(self):
        """Convert client object to dictionary for API responses"""
        return {
            'client_id': self.client_id,
            'client_name': self.client_name,
            'account_executive_id': self.account_executive_id,
            'city': self.city,
            'province': self.province,
            'industry': self.industry,
            'created_date': self.created_date.strftime('%Y-%m-%d') if self.created_date else None
        }


class Product(db.Model):
    """
    Product Model
    
    Represents Google Cloud products that can be sold to clients.
    Products are categorized (e.g., gcp-core, data-analytics, etc.).
    """
    __tablename__ = 'product'

    # Primary columns
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    product_category = db.Column(db.String(50), nullable=False)  # Values defined in DB constraints

    # Relationships
    # Currently commented out to simplify the initial implementation
    # opportunities = db.relationship('Opportunity', backref='product', lazy='dynamic')
    # signings = db.relationship('Signing', backref='product', lazy='dynamic')
    # revenue = db.relationship('Revenue', backref='product', lazy='dynamic')
    # wins = db.relationship('Win', backref='product', lazy='dynamic')
    
    def to_dict(self):
        """Convert product object to dictionary for API responses"""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_category': self.product_category
        }


class Opportunity(db.Model):
    """
    Opportunity Model
    
    Represents sales opportunities with clients.
    Includes forecast categories, sales stages, and financial details.
    Central to the sales pipeline tracking functionality.
    """
    __tablename__ = 'opportunity'

    # Primary columns
    opportunity_id = db.Column(db.Integer, primary_key=True)
    opportunity_name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    
    # Sales tracking fields
    forecast_category = db.Column(db.String(20), nullable=False)  # Values: 'omit', 'pipeline', 'upside', 'commit', 'closed-won'
    sales_stage = db.Column(db.String(50), nullable=False)  # Values: 'qualify', 'refine', 'tech-eval/soln-dev', 'proposal/negotiation', 'migrate'
    close_date = db.Column(db.Date, nullable=False)
    probability = db.Column(db.Numeric(5, 2), nullable=False)  # Percentage chance of closing
    amount = db.Column(db.Numeric(15, 2), nullable=False)  # Dollar value of opportunity
    
    # Timestamp fields
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # Currently commented out to simplify the initial implementation
    # signings = db.relationship('Signing', backref='opportunity', lazy='dynamic')
    # revenue = db.relationship('Revenue', backref='opportunity', lazy='dynamic')
    # wins = db.relationship('Win', backref='opportunity', lazy='dynamic')
    # update_events = db.relationship('UpdateEvent', backref='opportunity', lazy='dynamic')
    
    def to_dict(self):
        """Convert opportunity object to dictionary for API responses"""
        return {
            'opportunity_id': self.opportunity_id,
            'opportunity_name': self.opportunity_name,
            'client_id': self.client_id,
            'product_id': self.product_id,
            'forecast_category': self.forecast_category,
            'sales_stage': self.sales_stage,
            'close_date': self.close_date.strftime('%Y-%m-%d') if self.close_date else None,
            'probability': float(self.probability) if self.probability else None,
            'amount': float(self.amount) if self.amount else None,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S') if self.created_date else None,
            'last_modified_date': self.last_modified_date.strftime('%Y-%m-%d %H:%M:%S') if self.last_modified_date else None
        }


class Signing(db.Model):
    """
    Signing Model
    
    Represents contract signings with clients.
    Contains the financial details of a signed contract including value and term.
    Tracks when opportunities convert to actual contracts.
    """
    __tablename__ = 'signing'

    # Primary columns
    signing_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    
    # Financial details
    total_contract_value = db.Column(db.Numeric(15, 2), nullable=False)  # Total value over contract term
    incremental_acv = db.Column(db.Numeric(15, 2))  # Annual Contract Value increment
    
    # Date fields
    start_date = db.Column(db.Date, nullable=False)  # Contract start date
    end_date = db.Column(db.Date, nullable=False)  # Contract end date
    signing_date = db.Column(db.Date, nullable=False)  # When contract was signed
    
    # Fiscal period
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)  # Values: 1-4

    # Relationships
    # Currently commented out to simplify the initial implementation
    # revenue = db.relationship('Revenue', backref='signing', lazy='dynamic')
    
    def to_dict(self):
        """Convert signing object to dictionary for API responses"""
        return {
            'signing_id': self.signing_id,
            'opportunity_id': self.opportunity_id,
            'client_id': self.client_id,
            'product_id': self.product_id,
            'total_contract_value': float(self.total_contract_value) if self.total_contract_value else None,
            'incremental_acv': float(self.incremental_acv) if self.incremental_acv else None,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'signing_date': self.signing_date.strftime('%Y-%m-%d') if self.signing_date else None,
            'fiscal_year': self.fiscal_year,
            'fiscal_quarter': self.fiscal_quarter
        }


class Revenue(db.Model):
    """
    Revenue Model
    
    Tracks revenue generated from signed contracts.
    Breaks down revenue by fiscal periods (year, quarter, month).
    Used for financial reporting and analysis.
    """
    __tablename__ = 'revenue'

    # Primary columns
    revenue_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    signing_id = db.Column(db.Integer, db.ForeignKey('signing.signing_id'))  # Can be null if forecast revenue
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    
    # Fiscal period
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)  # Values: 1-4
    month = db.Column(db.Integer, nullable=False)  # Values: 1-12
    
    # Financial data
    amount = db.Column(db.Numeric(15, 2), nullable=False)  # Dollar amount of revenue
    
    def to_dict(self):
        """Convert revenue object to dictionary for API responses"""
        return {
            'revenue_id': self.revenue_id,
            'opportunity_id': self.opportunity_id,
            'client_id': self.client_id,
            'signing_id': self.signing_id,
            'product_id': self.product_id,
            'fiscal_year': self.fiscal_year,
            'fiscal_quarter': self.fiscal_quarter,
            'month': self.month,
            'amount': float(self.amount) if self.amount else None
        }


class Win(db.Model):
    """
    Win Model
    
    Tracks technical wins with clients (GCP and Data Analytics).
    Different from signings - represents technical adoption achievements.
    Used for tracking sales team accomplishments against targets.
    """
    __tablename__ = 'win'

    # Primary columns
    win_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    
    # Win classification
    win_category = db.Column(db.String(10), nullable=False)  # Values: 'gcp', 'da' (data analytics)
    win_level = db.Column(db.Integer, nullable=False)  # GCP: 1-3, DA: 1-2
    win_multiplier = db.Column(db.Numeric(3, 1), nullable=False)  # Values: 0.5, 1.0
    
    # Fiscal period
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)  # Values: 1-4
    
    # Table constraints
    __table_args__ = (
        # Ensures only one win per category/level/year for each client
        db.UniqueConstraint('client_id', 'win_category', 'win_level', 'fiscal_year', name='unique_win_per_category_level_year'),
    )
    
    def to_dict(self):
        """Convert win object to dictionary for API responses"""
        return {
            'win_id': self.win_id,
            'client_id': self.client_id,
            'win_category': self.win_category,
            'win_level': self.win_level,
            'win_multiplier': float(self.win_multiplier) if self.win_multiplier else None,
            'fiscal_year': self.fiscal_year,
            'fiscal_quarter': self.fiscal_quarter,
            'opportunity_id': self.opportunity_id,
            'product_id': self.product_id
        }


class YearlyTarget(db.Model):
    """
    Yearly Target Model
    
    Defines annual targets for users (primarily account executives).
    Targets can be for different metrics (revenue, signings, wins, pipeline).
    Used for performance tracking and goal setting.
    """
    __tablename__ = 'yearlytarget'

    # Primary columns
    target_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(20), nullable=False)  # Values: 'revenue', 'signings', 'wins', 'pipeline'
    amount = db.Column(db.Numeric(15, 2), nullable=False)  # Target amount (dollars or count)
    
    # Relationships
    # Currently commented out to simplify the initial implementation
    # quarterly_targets = db.relationship('QuarterlyTarget', backref='yearly_target', lazy='dynamic')
    
    # Table constraints
    __table_args__ = (
        # Ensures only one target per type/year for each user
        db.UniqueConstraint('user_id', 'fiscal_year', 'target_type', name='unique_target_per_user_year_type'),
    )
    
    def to_dict(self):
        """Convert target object to dictionary for API responses"""
        return {
            'target_id': self.target_id,
            'user_id': self.user_id,
            'fiscal_year': self.fiscal_year,
            'target_type': self.target_type,
            'amount': float(self.amount) if self.amount else None
        }


class QuarterlyTarget(db.Model):
    """
    Quarterly Target Model
    
    Breaks down yearly targets into quarterly percentages.
    Allows for non-uniform distribution of targets across quarters.
    Used for more granular performance tracking.
    """
    __tablename__ = 'quarterlytarget'

    # Primary columns
    quarterly_target_id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('yearlytarget.target_id'), nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)  # Values: 1-4
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    percentage = db.Column(db.Numeric(5, 2), nullable=False)  # Percentage of yearly target (0-100)
    
    # Table constraints
    __table_args__ = (
        # Ensures only one entry per quarter for each target
        db.UniqueConstraint('target_id', 'fiscal_quarter', name='unique_quarterly_target'),
    )
    
    def to_dict(self):
        """Convert quarterly target object to dictionary for API responses"""
        return {
            'quarterly_target_id': self.quarterly_target_id,
            'target_id': self.target_id,
            'fiscal_quarter': self.fiscal_quarter,
            'user_id': self.user_id,
            'percentage': float(self.percentage) if self.percentage else None
        }


class UpdateEvent(db.Model):
    """
    Update Event Model
    
    Metadata for opportunity update events.
    Tracks when opportunities are updated and groups related field changes.
    Used for audit trail and change history.
    """
    __tablename__ = 'updateevent'

    # Primary columns
    change_batch_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    change_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    # Currently commented out to simplify the initial implementation
    # updates = db.relationship('OpportunityUpdateLog', backref='update_event', lazy='dynamic')
    
    def to_dict(self):
        """Convert event object to dictionary for API responses"""
        return {
            'change_batch_id': self.change_batch_id,
            'opportunity_id': self.opportunity_id,
            'change_date': self.change_date.strftime('%Y-%m-%d %H:%M:%S') if self.change_date else None
        }


class OpportunityUpdateLog(db.Model):
    """
    Opportunity Update Log Model
    
    Detailed log of changes to opportunity fields.
    Records the specific fields that changed and their old/new values.
    Provides complete audit history of opportunity changes.
    """
    __tablename__ = 'opportunityupdatelog'

    # Primary columns
    log_id = db.Column(db.Integer, primary_key=True)
    change_batch_id = db.Column(db.Integer, db.ForeignKey('updateevent.change_batch_id'), nullable=False)
    field_name = db.Column(db.String(50), nullable=False)  # Name of the field that changed
    old_value = db.Column(db.Text, nullable=False)  # Previous value (stored as text)
    new_value = db.Column(db.Text, nullable=False)  # New value (stored as text)
    
    # Table constraints
    __table_args__ = (
        # Ensures only one entry per field in each change batch
        db.UniqueConstraint('change_batch_id', 'field_name', name='unique_field_per_batch'),
    )
    
    def to_dict(self):
        """Convert log entry to dictionary for API responses"""
        return {
            'log_id': self.log_id,
            'change_batch_id': self.change_batch_id,
            'field_name': self.field_name,
            'old_value': self.old_value,
            'new_value': self.new_value
        }