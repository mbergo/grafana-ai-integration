#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Set the FLASK_APP environment variable
export FLASK_APP=app.py

# Run the Flask application
flask run
