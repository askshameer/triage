#!/usr/bin/env python3
"""
WSGI configuration for Hostinger Passenger deployment
Place this file in your domain's root directory
"""

import sys
import os

# Get the absolute path to your application
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to virtual environment Python interpreter
INTERP = os.path.join(CURRENT_DIR, 'venv', 'bin', 'python3')

# If running under Passenger, use the virtual environment Python
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add your application directory to the Python path
sys.path.insert(0, CURRENT_DIR)

# Change to the application directory
os.chdir(CURRENT_DIR)

# Import the Flask application
from app import app as application

# For debugging (remove in production)
# application.config['DEBUG'] = False
