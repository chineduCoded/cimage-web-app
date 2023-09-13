#!/usr/bin/python3
"""Generate unique session ID using strong cryptographic algorithm"""
import secrets
import string

def generate_unique_session_id(length=64):
    # Define characters to choose from for the session ID
    characters = string.ascii_lowercase + string.digits
    
    # Generate a random component using secrets
    random_part = ''.join(secrets.choice(characters) for _ in range(length))
    
    return random_part