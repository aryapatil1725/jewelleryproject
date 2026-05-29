#!/usr/bin/env python3
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'jewellery project', 'jewellery project'))

# Import the Flask app
from app import app

if __name__ == "__main__":
    app.run()