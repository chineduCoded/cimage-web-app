#!/usr/bin/python3
"""Configuration"""
import os
from dotenv import load_dotenv
import redis

load_dotenv()


class Config:
    # Flask app configuration
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Storage config
    CIMAGE_STORAGE_TYPE = os.getenv("CIMAGE_STORAGE_TYPE")

    # Twitter config
    TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWIITER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = "http://localhost:5000"
    ALLOWED_ORIGIN = "http://localhost:3000"
    # Redis session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'cimage_web'  # A unique prefix for your sessions
    
    # Redis config with default values or environments
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

    # Create a property for the SESSION_REDIS
    @property
    def SESSION_REDIS(self):
        return redis.StrictRedis(host=self.REDIS_HOST, port=self.REDIS_PORT, db=0)

class ProductionConfig(Config):
    DEBUG = False

# Define which configuration to use based on environment variable
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}