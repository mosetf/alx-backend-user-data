#!/usr/bin/env python3
"""
Simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()