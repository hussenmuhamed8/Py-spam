#!/usr/bin/env python3
"""
Facebook Login Implementation using Python Flask and Facebook Graph API
This module provides both web-based OAuth login and programmatic API access.
"""

import os
import json
from flask import Flask, request, redirect, session, url_for, render_template_string, jsonify
import requests
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import facebook

# Load environment variables
load_dotenv()

# Facebook App Configuration
FACEBOOK_CLIENT_ID = os.getenv('FACEBOOK_CLIENT_ID', 'your_app_id_here')
FACEBOOK_CLIENT_SECRET = os.getenv('FACEBOOK_CLIENT_SECRET', 'your_app_secret_here')
FACEBOOK_REDIRECT_URI = os.getenv('FACEBOOK_REDIRECT_URI', 'http://localhost:5000/callback')

# Facebook OAuth URLs
FACEBOOK_AUTHORIZATION_BASE_URL = 'https://www.facebook.com/dialog/oauth'
FACEBOOK_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
FACEBOOK_SCOPE = ['email', 'public_profile']

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

class FacebookLogin:
    """Facebook Login handler class"""
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
    def get_authorization_url(self):
        """Get Facebook authorization URL"""
        facebook_oauth = OAuth2Session(
            self.client_id, 
            scope=FACEBOOK_SCOPE,
            redirect_uri=self.redirect_uri
        )
        authorization_url, state = facebook_oauth.authorization_url(
            FACEBOOK_AUTHORIZATION_BASE_URL
        )
        return authorization_url, state
    
    def get_access_token(self, authorization_response):
        """Exchange authorization code for access token"""
        facebook_oauth = OAuth2Session(
            self.client_id,
            redirect_uri=self.redirect_uri
        )
        
        token = facebook_oauth.fetch_token(
            FACEBOOK_TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret
        )
        return token
    
    def get_user_info(self, access_token):
        """Get user information from Facebook Graph API"""
        graph = facebook.GraphAPI(access_token=access_token)
        user_info = graph.get_object('me', fields='id,name,email,picture')
        return user_info

# Initialize Facebook Login
fb_login = FacebookLogin(FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, FACEBOOK_REDIRECT_URI)

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Login Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .fb-login-btn {
            background-color: #4267B2;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .fb-login-btn:hover {
            background-color: #365899;
        }
        .user-info {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .error {
            background: #ffe8e8;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            color: #d8000c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Login Demo</h1>
        
        {% if user_info %}
            <div class="user-info">
                <h3>Welcome, {{ user_info.name }}!</h3>
                <p><strong>ID:</strong> {{ user_info.id }}</p>
                <p><strong>Email:</strong> {{ user_info.get('email', 'Not provided') }}</p>
                {% if user_info.picture %}
                <img src="{{ user_info.picture.data.url }}" alt="Profile Picture" style="border-radius: 50%; width: 80px; height: 80px;">
                {% endif %}
                <br><br>
                <a href="/logout" class="fb-login-btn" style="background-color: #666;">Logout</a>
            </div>
        {% elif error %}
            <div class="error">
                <strong>Error:</strong> {{ error }}
            </div>
        {% else %}
            <p>Click the button below to login with Facebook:</p>
            <a href="/login" class="fb-login-btn">Login with Facebook</a>
        {% endif %}
        
        <hr style="margin: 30px 0;">
        
        <h3>API Endpoints:</h3>
        <ul>
            <li><code>GET /</code> - Main page</li>
            <li><code>GET /login</code> - Initiate Facebook login</li>
            <li><code>GET /callback</code> - Facebook callback</li>
            <li><code>GET /user</code> - Get current user info (JSON)</li>
            <li><code>GET /logout</code> - Logout</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    user_info = session.get('user_info')
    error = session.pop('error', None)
    
    return render_template_string(
        LOGIN_TEMPLATE,
        user_info=user_info,
        error=error
    )

@app.route('/login')
def login():
    """Initiate Facebook login"""
    try:
        authorization_url, state = fb_login.get_authorization_url()
        session['oauth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        session['error'] = f"Login error: {str(e)}"
        return redirect(url_for('index'))

@app.route('/callback')
def callback():
    """Facebook OAuth callback"""
    try:
        # Get the full callback URL
        authorization_response = request.url
        
        # Exchange code for token
        token = fb_login.get_access_token(authorization_response)
        access_token = token['access_token']
        
        # Get user information
        user_info = fb_login.get_user_info(access_token)
        
        # Store in session
        session['access_token'] = access_token
        session['user_info'] = user_info
        
        return redirect(url_for('index'))
        
    except Exception as e:
        session['error'] = f"Callback error: {str(e)}"
        return redirect(url_for('index'))

@app.route('/user')
def user():
    """Get current user info as JSON"""
    user_info = session.get('user_info')
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({'error': 'User not logged in'}), 401

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

# Programmatic Facebook API Access
class FacebookAPI:
    """Facebook Graph API client for programmatic access"""
    
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.graph = facebook.GraphAPI(access_token=access_token) if access_token else None
    
    def set_access_token(self, access_token):
        """Set access token"""
        self.access_token = access_token
        self.graph = facebook.GraphAPI(access_token=access_token)
    
    def get_user_profile(self, user_id='me', fields='id,name,email'):
        """Get user profile information"""
        if not self.graph:
            raise ValueError("Access token not set")
        return self.graph.get_object(user_id, fields=fields)
    
    def get_user_posts(self, user_id='me', limit=10):
        """Get user's posts"""
        if not self.graph:
            raise ValueError("Access token not set")
        return self.graph.get_connections(user_id, 'posts', limit=limit)
    
    def post_to_feed(self, message, user_id='me'):
        """Post to user's feed"""
        if not self.graph:
            raise ValueError("Access token not set")
        return self.graph.put_object(user_id, 'feed', message=message)
    
    def get_friends(self, user_id='me'):
        """Get user's friends list"""
        if not self.graph:
            raise ValueError("Access token not set")
        return self.graph.get_connections(user_id, 'friends')

# API Routes for programmatic access
@app.route('/api/profile')
def api_profile():
    """API endpoint to get user profile"""
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        fb_api = FacebookAPI(access_token)
        profile = fb_api.get_user_profile()
        return jsonify(profile)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts')
def api_posts():
    """API endpoint to get user posts"""
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        fb_api = FacebookAPI(access_token)
        posts = fb_api.get_user_posts()
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Facebook Login Demo Server")
    print("=" * 30)
    print(f"Client ID: {FACEBOOK_CLIENT_ID}")
    print(f"Redirect URI: {FACEBOOK_REDIRECT_URI}")
    print("\nMake sure to:")
    print("1. Set your Facebook App credentials in .env file")
    print("2. Add the redirect URI to your Facebook App settings")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("\nServer starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)