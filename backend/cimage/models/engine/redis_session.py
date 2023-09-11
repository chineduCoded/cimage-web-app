import redis
from flask import session
from flask_session import Session

class RedisClient:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.config.setdefault('SESSION_TYPE', 'redis')
        app.config.setdefault('SESSION_PERMANENT', False)
        app.config.setdefault('SESSION_USE_SIGNER', True)
        app.config.setdefault('SESSION_KEY_PREFIX', 'cimage_web')
        app.config.setdefault('SESSION_REDIS', self.get_redis(app))

        Session(app)

    def get_redis(self, app):
        return redis.StrictRedis(
            host=app.config.get('REDIS_HOST', 'localhost'),
            port=app.config.get('REDIS_PORT', 6379),
            db=app.config.get('REDIS_DB', 0)
        )

    def set(self, key, value, ttl=None):
        """Set a session key with an optional TTL (time-to-live)"""
        redis_client = self.get_redis(self.app)
        if ttl:
            redis_client.setex(key, ttl, value)
        else:
            self.get_redis(self.app).set(key, value)

    def get(self, identifier):
        """
        Get session data using either a key or a session ID.
        
        Args:
            identifier (str): The key or session ID to retrieve data for.
            
        Returns:
            bytes or None: The session data if found, or None if not found.
        """
        redis_client = self.get_redis(self.app)
        return redis_client.get(identifier)

    def delete(self, key):
        """Delete session"""
        session.pop(key, None)

    def clear(self, key):
        """Clear the entire session associated with key"""
        redis_client = self.get_redis(self.app)
        redis_client.delete(key)

    def update(self, session_id, data):
        """Update the session data associated with the given ID"""
        redis_client = self.get_redis(self.app)
        redis_client.hmget(session_id, data)

    def reload(self, key, ttl=3600):
        """
        Reloads (extends) the session ttl (time-to-live) in Redis for a specific session key.
        """
        if key in session:
            self.get_redis(self.app).expire(f"{session.sid}:{key}", ttl)