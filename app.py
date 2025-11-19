#!/usr/bin/env python3
"""
Web API for Platform Issue Triage Tool
Provides REST API endpoints for the triage functionality.
"""

from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os
import tempfile
import pandas as pd
from pathlib import Path
from triage_tool import TriageTool

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app, supports_credentials=True)  # Enable CORS with credentials

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-123456789')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_LOG_EXTENSIONS = {'log', 'txt', 'out'}
ALLOWED_EXCEL_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Hardcoded credentials (hashed)
# Username: sameer, Password: He110
USERS = {
    'sameer': generate_password_hash('He110')
}

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename, allowed_extensions):
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'version': '1.0'})


@app.route('/api/login', methods=['POST'])
def login():
    """
    Login endpoint.

    Expected JSON data:
    - username: Username
    - password: Password
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        # Check credentials
        if username in USERS and check_password_hash(USERS[username], password):
            session['username'] = username
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'username': username
            })
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'error': f'Login error: {str(e)}'}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint."""
    session.pop('username', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated."""
    if 'username' in session:
        return jsonify({
            'authenticated': True,
            'username': session['username']
        })
    return jsonify({'authenticated': False}), 401


@app.route('/api/triage', methods=['POST'])
@login_required
def perform_triage():
    """
    Perform triage on uploaded log file.

    Expected form data:
    - logfile: The log file to analyze
    - excel_file: (optional) Custom error mappings Excel file
    - max_errors: (optional) Maximum number of errors to return
    """
    try:
        # Validate log file
        if 'logfile' not in request.files:
            return jsonify({'error': 'No log file provided'}), 400

        log_file = request.files['logfile']
        if log_file.filename == '':
            return jsonify({'error': 'No log file selected'}), 400

        if not allowed_file(log_file.filename, ALLOWED_LOG_EXTENSIONS):
            return jsonify({'error': 'Invalid log file type. Allowed: .log, .txt, .out'}), 400

        # Save log file temporarily
        log_filename = secure_filename(log_file.filename)
        log_path = os.path.join(app.config['UPLOAD_FOLDER'], f"log_{os.getpid()}_{log_filename}")
        log_file.save(log_path)

        # Handle optional Excel file
        excel_path = 'error_mappings.xlsx'  # Default
        excel_temp_path = None

        if 'excel_file' in request.files:
            excel_file = request.files['excel_file']
            if excel_file.filename != '':
                if not allowed_file(excel_file.filename, ALLOWED_EXCEL_EXTENSIONS):
                    os.remove(log_path)
                    return jsonify({'error': 'Invalid Excel file type. Allowed: .xlsx, .xls'}), 400

                excel_filename = secure_filename(excel_file.filename)
                excel_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"excel_{os.getpid()}_{excel_filename}")
                excel_file.save(excel_temp_path)
                excel_path = excel_temp_path

        # Get max_errors parameter
        max_errors = request.form.get('max_errors', type=int)
        if max_errors is not None and max_errors < 1:
            max_errors = None

        # Initialize triage tool
        triage = TriageTool(excel_file=excel_path)

        # Load error mappings
        if not triage.load_error_mappings():
            # Cleanup
            os.remove(log_path)
            if excel_temp_path:
                os.remove(excel_temp_path)
            return jsonify({'error': 'Failed to load error mappings from Excel file'}), 400

        # Scan log file
        matches = triage.scan_log_file(log_path)

        # Prepare results
        results = []
        display_matches = matches[:max_errors] if max_errors else matches

        for line_num, log_line, interpretation in display_matches:
            results.append({
                'line_number': line_num,
                'log_line': log_line,
                'interpretation': interpretation
            })

        response_data = {
            'total_errors': len(matches),
            'displayed_errors': len(results),
            'results': results,
            'log_filename': log_filename,
            'mappings_count': len(triage.error_mappings)
        }

        # Cleanup temporary files
        os.remove(log_path)
        if excel_temp_path:
            os.remove(excel_temp_path)

        return jsonify(response_data)

    except Exception as e:
        # Cleanup on error
        if 'log_path' in locals() and os.path.exists(log_path):
            os.remove(log_path)
        if 'excel_temp_path' in locals() and excel_temp_path and os.path.exists(excel_temp_path):
            os.remove(excel_temp_path)

        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/validate-excel', methods=['POST'])
@login_required
def validate_excel():
    """
    Validate Excel file and return error mapping count.

    Expected form data:
    - excel_file: The Excel file to validate
    """
    try:
        if 'excel_file' not in request.files:
            return jsonify({'error': 'No Excel file provided'}), 400

        excel_file = request.files['excel_file']
        if excel_file.filename == '':
            return jsonify({'error': 'No Excel file selected'}), 400

        if not allowed_file(excel_file.filename, ALLOWED_EXCEL_EXTENSIONS):
            return jsonify({'error': 'Invalid Excel file type. Allowed: .xlsx, .xls'}), 400

        # Save temporarily
        excel_filename = secure_filename(excel_file.filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], f"validate_{os.getpid()}_{excel_filename}")
        excel_file.save(excel_path)

        # Validate
        triage = TriageTool(excel_file=excel_path)
        success = triage.load_error_mappings()

        if success:
            response = {
                'valid': True,
                'mappings_count': len(triage.error_mappings),
                'filename': excel_filename
            }
        else:
            response = {
                'valid': False,
                'error': 'Invalid Excel file format or no valid mappings found'
            }

        # Cleanup
        os.remove(excel_path)

        return jsonify(response)

    except Exception as e:
        if 'excel_path' in locals() and os.path.exists(excel_path):
            os.remove(excel_path)
        return jsonify({'error': f'Validation error: {str(e)}'}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve the React frontend or static files."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    # Check if default error_mappings.xlsx exists
    if not os.path.exists('error_mappings.xlsx'):
        print("Warning: error_mappings.xlsx not found in current directory.")
        print("Users will need to upload a custom Excel file.")

    print("Starting Platform Issue Triage Tool Web API...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
