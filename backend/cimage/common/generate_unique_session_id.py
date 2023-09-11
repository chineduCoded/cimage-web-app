#!/usr/bin/python3
"""Generate unique session ID"""
import random
import string
import time


def generate_unique_session_id(length=10):
    # Define characters to choose from for the session ID
    characters = string.ascii_uppercase + string.digits
    
    # Generate a timestamp component (time-based)
    timestamp = int(time.time() * 1000)  # Convert current time to milliseconds
    
    # Generate a random component (randomly chosen characters)
    random_part = ''.join(random.choice(characters) for _ in range(length - len(str(timestamp))))
    
    # Combine timestamp and random components
    session_id = str(timestamp) + random_part
    
    return session_id