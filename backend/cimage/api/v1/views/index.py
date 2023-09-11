#!/usr/bin/python3
"""Index.py"""
from datetime import datetime
import sys
from flask import render_template, jsonify
from cimage.api.v1.views import cimage_views


@cimage_views.route("/")
def index():
    """Home page"""
    context = {
        "page_title": "API Home",
        "current_year": datetime.now().year
    }
    return render_template("home.html", **context)

@cimage_views.route("/status", methods=["GET"])
def status():
    """Checks the running state of cimage"""
    return jsonify({"Status": "running"}), 200