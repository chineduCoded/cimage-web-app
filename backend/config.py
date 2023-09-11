#!/usr/bin/python3
"""Configuration"""
import os
from dotenv import load_dotenv
import redis

load_dotenv()

class Config:
    # Flask app configuration
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    CIMAGE_STORAGE_TYPE = os.getenv("CIMAGE_STORAGE_TYPE")

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