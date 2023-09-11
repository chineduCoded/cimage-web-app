#!/usr/bin/python3
"""Handles Logger"""
import os
import logging


def configure_logger(app):
    # Create a logger instance
    logger = logging.getLogger(__name__)

    # Configure log handlers (write logs to a file)
    log_dir = os.path.join(app.root_path, 'logs')  # Define log directory
    os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist
    log_file = os.path.join(log_dir, 'cimage.log')  # Define the log file path

    file_handler = logging.FileHandler(log_file)  # Log to a file
    file_handler.setLevel(logging.INFO)  # Set log level (e.g., INFO, ERROR, DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the log handler to the logger
    logger.addHandler(file_handler)

    # Set the logger level (you can adjust this based on your needs)
    logger.setLevel(logging.INFO)

    # Add the logger to the app's context so it can be accessed
    app.logger = logger