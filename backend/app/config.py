"""
Configuration Module

This module defines configuration for the application.
It uses environment variables loaded from a .env file to
configure the application, especially database connections.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration class.
    
    This class contains settings common to all environments.
    """
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event system for performance
    
    # Development mode enabled by default
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    
    Used for local development.
    """
    # Development-specific settings can be added here later
    pass


# Use development config as the only config for now
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}