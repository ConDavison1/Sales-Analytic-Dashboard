from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(20), nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)  # Not actually hashed for now

    # Relationships
    # account_executives = db.relationship('DirectorAccountExecutive', 
    #                                      foreign_keys='DirectorAccountExecutive.director_id',
    #                                      backref='director', lazy='dynamic')
    # clients = db.relationship('Client', backref='account_executive', lazy='dynamic')
    # yearly_targets = db.relationship('YearlyTarget', backref='user', lazy='dynamic')
    # quarterly_targets = db.relationship('QuarterlyTarget', backref='user', lazy='dynamic')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role
        }


class DirectorAccountExecutive(db.Model):
    __tablename__ = 'directoraccountexecutive'

    account_executive_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    def to_dict(self):
        return {
            'account_executive_id': self.account_executive_id,
            'director_id': self.director_id
        }


class Client(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    account_executive_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    city = db.Column(db.String(50))
    province = db.Column(db.String(2))
    industry = db.Column(db.String(50))
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Relationships
    # opportunities = db.relationship('Opportunity', backref='client', lazy='dynamic')
    # signings = db.relationship('Signing', backref='client', lazy='dynamic')
    # revenue = db.relationship('Revenue', backref='client', lazy='dynamic')
    # wins = db.relationship('Win', backref='client', lazy='dynamic')
    
    def to_dict(self):
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
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    product_category = db.Column(db.String(50), nullable=False)

    # Relationships
    # opportunities = db.relationship('Opportunity', backref='product', lazy='dynamic')
    # signings = db.relationship('Signing', backref='product', lazy='dynamic')
    # revenue = db.relationship('Revenue', backref='product', lazy='dynamic')
    # wins = db.relationship('Win', backref='product', lazy='dynamic')
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_category': self.product_category
        }


class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    opportunity_id = db.Column(db.Integer, primary_key=True)
    opportunity_name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    forecast_category = db.Column(db.String(20), nullable=False)
    sales_stage = db.Column(db.String(50), nullable=False)
    close_date = db.Column(db.Date, nullable=False)
    probability = db.Column(db.Numeric(5, 2), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # signings = db.relationship('Signing', backref='opportunity', lazy='dynamic')
    # revenue = db.relationship('Revenue', backref='opportunity', lazy='dynamic')
    # wins = db.relationship('Win', backref='opportunity', lazy='dynamic')
    # update_events = db.relationship('UpdateEvent', backref='opportunity', lazy='dynamic')
    
    def to_dict(self):
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
    __tablename__ = 'signing'

    signing_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    total_contract_value = db.Column(db.Numeric(15, 2), nullable=False)
    incremental_acv = db.Column(db.Numeric(15, 2))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    signing_date = db.Column(db.Date, nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)

    # Relationships
    # revenue = db.relationship('Revenue', backref='signing', lazy='dynamic')
    
    def to_dict(self):
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
    __tablename__ = 'revenue'

    revenue_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    signing_id = db.Column(db.Integer, db.ForeignKey('signing.signing_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    def to_dict(self):
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
    __tablename__ = 'win'

    win_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    win_category = db.Column(db.String(10), nullable=False)
    win_level = db.Column(db.Integer, nullable=False)
    win_multiplier = db.Column(db.Numeric(3, 1), nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('client_id', 'win_category', 'win_level', 'fiscal_year', name='unique_win_per_category_level_year'),
    )
    
    def to_dict(self):
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
    __tablename__ = 'yearlytarget'

    target_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Relationships
    # quarterly_targets = db.relationship('QuarterlyTarget', backref='yearly_target', lazy='dynamic')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'fiscal_year', 'target_type', name='unique_target_per_user_year_type'),
    )
    
    def to_dict(self):
        return {
            'target_id': self.target_id,
            'user_id': self.user_id,
            'fiscal_year': self.fiscal_year,
            'target_type': self.target_type,
            'amount': float(self.amount) if self.amount else None
        }


class QuarterlyTarget(db.Model):
    __tablename__ = 'quarterlytarget'

    quarterly_target_id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('yearlytarget.target_id'), nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    percentage = db.Column(db.Numeric(5, 2), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('target_id', 'fiscal_quarter', name='unique_quarterly_target'),
    )
    
    def to_dict(self):
        return {
            'quarterly_target_id': self.quarterly_target_id,
            'target_id': self.target_id,
            'fiscal_quarter': self.fiscal_quarter,
            'user_id': self.user_id,
            'percentage': float(self.percentage) if self.percentage else None
        }


class UpdateEvent(db.Model):
    __tablename__ = 'updateevent'

    change_batch_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.opportunity_id'), nullable=False)
    change_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    # updates = db.relationship('OpportunityUpdateLog', backref='update_event', lazy='dynamic')
    
    def to_dict(self):
        return {
            'change_batch_id': self.change_batch_id,
            'opportunity_id': self.opportunity_id,
            'change_date': self.change_date.strftime('%Y-%m-%d %H:%M:%S') if self.change_date else None
        }


class OpportunityUpdateLog(db.Model):
    __tablename__ = 'opportunityupdatelog'

    log_id = db.Column(db.Integer, primary_key=True)
    change_batch_id = db.Column(db.Integer, db.ForeignKey('updateevent.change_batch_id'), nullable=False)
    field_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text, nullable=False)
    new_value = db.Column(db.Text, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('change_batch_id', 'field_name', name='unique_field_per_batch'),
    )
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'change_batch_id': self.change_batch_id,
            'field_name': self.field_name,
            'old_value': self.old_value,
            'new_value': self.new_value
        }