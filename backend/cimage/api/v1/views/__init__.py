#!/usr/bin/python3
"""Contains the Blueprint for the API"""
from flask import Blueprint

cimage_views = Blueprint("cimage_views", __name__)
api_bp = Blueprint("api_bp", __name__, url_prefix="/api/v1")


from cimage.api.v1.views.index import *
from cimage.api.v1.views.api_blueprint import *