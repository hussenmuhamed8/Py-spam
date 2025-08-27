#!/usr/bin/env python3
"""
Facebook Login Examples and Usage Demonstrations
This file contains various examples of how to use the Facebook login implementations.
"""

import os
import time
from dotenv import load_dotenv
from facebook_api_client import FacebookGraphAPI, example_user_operations, example_page_operations

# Load environment variables
load_dotenv()

def example_1_basic_profile_access():
    """
    Example 1: Basic user profile access
    """
    print("Example 1: Basic Profile Access")
    print("=" * 35)
    
    # You would get this token from the OAuth flow
    # For testing, you can get a temporary token from Facebook Graph API Explorer
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    try:
        api = FacebookGraphAPI(access_token)
        
        # Get basic profile information
        profile = api.get_user_profile(fields="id,name,email,picture")
        
        print(f"User ID: {profile.get('id')}")
        print(f"Name: {profile.get('name')}")
        print(f"Email: {profile.get('email', 'Not available')}")
        
        if 'picture' in profile:
            print(f"Profile Picture: {profile['picture']['data']['url']}")
            
    except Exception as e:
        print(f"Error: {e}")

def example_2_user_posts():
    """
    Example 2: Retrieving user posts
    """
    print("\nExample 2: User Posts")
    print("=" * 20)
    
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    try:
        api = FacebookGraphAPI(access_token)
        
        # Get user's recent posts
        posts = api.get_user_posts(limit=5)
        
        print(f"Found {len(posts.get('data', []))} posts:")
        
        for i, post in enumerate(posts.get('data', []), 1):
            print(f"\nPost {i}:")
            print(f"  ID: {post.get('id')}")
            print(f"  Message: {post.get('message', 'No message')[:100]}...")
            print(f"  Created: {post.get('created_time')}")
            
    except Exception as e:
        print(f"Error: {e}")

def example_3_page_information():
    """
    Example 3: Getting Facebook page information
    """
    print("\nExample 3: Page Information")
    print("=" * 26)
    
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    page_id = "YOUR_PAGE_ID_HERE"  # Replace with actual page ID
    
    try:
        api = FacebookGraphAPI(access_token)
        
        # Get page information
        page_info = api.get_page_info(page_id, fields="id,name,about,category,fan_count,website")
        
        print(f"Page Name: {page_info.get('name')}")
        print(f"Category: {page_info.get('category')}")
        print(f"About: {page_info.get('about', 'No description')[:100]}...")
        print(f"Fans: {page_info.get('fan_count', 'N/A')}")
        print(f"Website: {page_info.get('website', 'N/A')}")
        
        # Get recent page posts
        posts = api.get_page_posts(page_id, limit=3)
        print(f"\nRecent posts: {len(posts.get('data', []))}")
        
    except Exception as e:
        print(f"Error: {e}")

def example_4_search_pages():
    """
    Example 4: Searching for Facebook pages
    """
    print("\nExample 4: Search Pages")
    print("=" * 22)
    
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    try:
        api = FacebookGraphAPI(access_token)
        
        # Search for technology-related pages
        search_query = "python programming"
        results = api.search_pages(search_query, limit=5)
        
        print(f"Search results for '{search_query}':")
        
        for i, page in enumerate(results.get('data', []), 1):
            print(f"\n{i}. {page.get('name')}")
            print(f"   ID: {page.get('id')}")
            print(f"   Category: {page.get('category', 'N/A')}")
            
    except Exception as e:
        print(f"Error: {e}")

def example_5_flask_integration():
    """
    Example 5: How to integrate with Flask app
    """
    print("\nExample 5: Flask Integration")
    print("=" * 27)
    
    example_code = '''
# In your Flask route:
from facebook_api_client import FacebookGraphAPI

@app.route('/dashboard')
def dashboard():
    # Get access token from session
    access_token = session.get('access_token')
    
    if not access_token:
        return redirect(url_for('login'))
    
    try:
        api = FacebookGraphAPI(access_token)
        
        # Get user profile
        profile = api.get_user_profile()
        
        # Get recent posts
        posts = api.get_user_posts(limit=10)
        
        return render_template('dashboard.html', 
                             profile=profile, 
                             posts=posts)
    except Exception as e:
        flash(f'Error accessing Facebook API: {e}')
        return redirect(url_for('index'))
'''
    
    print("Here's how to integrate the Facebook API client with your Flask app:")
    print(example_code)

def example_6_token_validation():
    """
    Example 6: Token validation and error handling
    """
    print("\nExample 6: Token Validation")
    print("=" * 26)
    
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    try:
        api = FacebookGraphAPI(access_token)
        
        # Validate the token
        validation = api.validate_token()
        print(f"Token is valid for user: {validation.get('id')}")
        
        # You can also check token expiration and permissions
        # This would require additional API calls to /debug_token endpoint
        
    except Exception as e:
        print(f"Token validation failed: {e}")
        print("This usually means:")
        print("1. Token has expired")
        print("2. Token is invalid")
        print("3. App doesn't have required permissions")

def run_all_examples():
    """
    Run all examples
    """
    print("Facebook API Examples")
    print("=" * 20)
    print("Note: Replace 'YOUR_ACCESS_TOKEN_HERE' with actual tokens")
    print("You can get test tokens from Facebook Graph API Explorer")
    print("https://developers.facebook.com/tools/explorer/")
    
    example_1_basic_profile_access()
    example_2_user_posts()
    example_3_page_information()
    example_4_search_pages()
    example_5_flask_integration()
    example_6_token_validation()

if __name__ == "__main__":
    run_all_examples()