#!/usr/bin/env python3
import sys
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the app directory to Python path
APP_DIR = os.path.join(BASE_DIR, 'jewellery project', 'jewellery project')
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Change to the app directory to ensure imports work
os.chdir(APP_DIR)

# Import the Flask app
from app import app

if __name__ == "__main__":
    app.run()