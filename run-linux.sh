#!/bin/bash

echo "College Management System - Starting..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database and admin
echo ""
echo "Setting up database and admin account (if needed)..."
python3 setup_admin.py

# Start the application
echo ""
echo "Starting application..."
echo "Opening http://localhost:5000 in your browser..."
sleep 2
python3 app.py
