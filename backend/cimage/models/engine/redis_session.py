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
        """Delete an item from the session"""
        redis_client = self.get_redis(self.app)
        redis_client.delete(key)

    def clear(self, key):
        """Clear the entire session associated with key"""
        for session_key in self.get_redis(self.app).keys(f"image:{key}"):
            self.delete(session_key.decode("utf-8"))

    def update(self, session_id, data):
        """Update the session data associated with the given ID"""
        redis_client = self.get_redis(self.app)
        redis_client.hmset(session_id, data)
    def exists(self, key):
        """Check if a key exists in Redis"""
        redis_client = self.get_redis(self.app)
        return redis_client.exists(key)

    def reload(self, key, ttl=3600):
        """
        Reloads (extends) the session TTL (time-to-live) in Redis for a specific session key.
        """
        redis_client = self.get_redis(self.app)
        session_key = f"{session.sid}:{key}"
        
        # Check if the session key exists in Redis
        if redis_client.exists(session_key):
            # Extend the TTL for the session key
            redis_client.expire(session_key, ttl)

    
    def set_image(self, image_id, image_data):
        """
        Set an image in the session using the provided image_id.

        Args:
            image_id (str): The unique identifier for the image.
            image_data (bytes): The image data to store.
        """
        session_key = f"image:{image_id}"
        self.set(session_key, image_data)

    def get_image(self, image_id):
        """
        Get an image from the session using the provided image_id.

        Args:
            image_id (str): The unique identifier for the image.

        Returns:
            bytes or None: The image data if found, or None if not found.
        """
        session_key = f"image:{image_id}"
        return self.get(session_key)

    def delete_image(self, image_id):
        """
        Delete an image from the session using the provided image_id.

        Args:
            image_id (str): The unique identifier for the image.
        """
        session_key = f"image:{image_id}"
        self.delete(session_key)

    def get_all_images(self):
        """
        Get all images stored in the session.

        Returns:
            dict: A dictionary containing image IDs as keys and image data as values.
        """
        image_data = {}
        for key in self.get_redis(self.app).keys("image:*"):
            image_id = key.decode("utf-8").split(":")[1]
            image_data[image_id] = self.get(key)
        return image_data

    def copy_image_address(self, image_id):
        """
        Copy the address (session key) of an image using the provided image_id.

        Args:
            image_id (str): The unique identifier for the image.

        Returns:
            str: The session key (address) of the image.
        """
        return f"image:{image_id}"
    
    def clear_all_images(self):
        """
        Clear (delete) all images stored in the Redis session.
        """
        redis_keys = self.get_redis(self.app).keys("image:*")
        if redis_keys:
            for key in redis_keys:
                self.delete(key.decode("utf-8"))
        else:
            raise ValueError("No images found in the session")