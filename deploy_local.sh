#!/bin/bash

# Local deployment script for Platform Issue Triage Tool
# This script builds the frontend and starts the production server

set -e

echo "============================================"
echo "Platform Issue Triage Tool - Local Deploy"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

echo "Step 1: Installing frontend dependencies..."
cd frontend
npm install

echo ""
echo "Step 2: Building frontend for production..."
npm run build

echo ""
echo "Step 3: Installing Python dependencies..."
cd ..
pip install -r requirements.txt

echo ""
echo "Step 4: Starting production server..."
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
