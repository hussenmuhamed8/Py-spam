#!/usr/bin/env python3
"""
Standalone Facebook Graph API Client
This module provides a standalone client for Facebook Graph API operations.
"""

import requests
import json
from typing import Dict, List, Optional

class FacebookGraphAPI:
    """
    A comprehensive Facebook Graph API client for various operations
    """
    
    def __init__(self, access_token: str):
        """
        Initialize the Facebook Graph API client
        
        Args:
            access_token (str): Facebook access token
        """
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None, data: Dict = None) -> Dict:
        """
        Make a request to Facebook Graph API
        
        Args:
            endpoint (str): API endpoint
            method (str): HTTP method
            params (dict): Query parameters
            data (dict): Request body data
            
        Returns:
            dict: API response
        """
        url = f"{self.base_url}/{endpoint}"
        
        if params is None:
            params = {}
        
        params['access_token'] = self.access_token
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error response: {e.response.text}")
            raise
    
    def get_user_profile(self, user_id: str = "me", fields: str = "id,name,email,picture") -> Dict:
        """
        Get user profile information
        
        Args:
            user_id (str): User ID or 'me' for current user
            fields (str): Comma-separated list of fields to retrieve
            
        Returns:
            dict: User profile data
        """
        return self._make_request(user_id, params={"fields": fields})
    
    def get_user_posts(self, user_id: str = "me", limit: int = 25) -> Dict:
        """
        Get user's posts
        
        Args:
            user_id (str): User ID or 'me' for current user
            limit (int): Number of posts to retrieve
            
        Returns:
            dict: Posts data
        """
        return self._make_request(f"{user_id}/posts", params={"limit": limit})
    
    def get_user_photos(self, user_id: str = "me", limit: int = 25) -> Dict:
        """
        Get user's photos
        
        Args:
            user_id (str): User ID or 'me' for current user
            limit (int): Number of photos to retrieve
            
        Returns:
            dict: Photos data
        """
        return self._make_request(f"{user_id}/photos", params={"limit": limit})
    
    def get_page_info(self, page_id: str, fields: str = "id,name,about,category,fan_count") -> Dict:
        """
        Get Facebook page information
        
        Args:
            page_id (str): Page ID
            fields (str): Comma-separated list of fields to retrieve
            
        Returns:
            dict: Page information
        """
        return self._make_request(page_id, params={"fields": fields})
    
    def get_page_posts(self, page_id: str, limit: int = 25) -> Dict:
        """
        Get posts from a Facebook page
        
        Args:
            page_id (str): Page ID
            limit (int): Number of posts to retrieve
            
        Returns:
            dict: Page posts data
        """
        return self._make_request(f"{page_id}/posts", params={"limit": limit})
    
    def post_to_page(self, page_id: str, message: str, page_access_token: str) -> Dict:
        """
        Post a message to a Facebook page
        
        Args:
            page_id (str): Page ID
            message (str): Message to post
            page_access_token (str): Page access token
            
        Returns:
            dict: Post response
        """
        # Temporarily use page access token
        original_token = self.access_token
        self.access_token = page_access_token
        
        try:
            result = self._make_request(f"{page_id}/feed", method="POST", data={"message": message})
            return result
        finally:
            # Restore original token
            self.access_token = original_token
    
    def get_user_friends(self, user_id: str = "me") -> Dict:
        """
        Get user's friends (limited due to Facebook policy changes)
        
        Args:
            user_id (str): User ID or 'me' for current user
            
        Returns:
            dict: Friends data (may be limited)
        """
        return self._make_request(f"{user_id}/friends")
    
    def search_pages(self, query: str, limit: int = 25) -> Dict:
        """
        Search for Facebook pages
        
        Args:
            query (str): Search query
            limit (int): Number of results to retrieve
            
        Returns:
            dict: Search results
        """
        return self._make_request("search", params={
            "q": query,
            "type": "page",
            "limit": limit
        })
    
    def get_insights(self, object_id: str, metric: str, period: str = "day") -> Dict:
        """
        Get insights/analytics data
        
        Args:
            object_id (str): Object ID (page, post, etc.)
            metric (str): Metric to retrieve
            period (str): Time period (day, week, month, lifetime)
            
        Returns:
            dict: Insights data
        """
        return self._make_request(f"{object_id}/insights", params={
            "metric": metric,
            "period": period
        })
    
    def validate_token(self) -> Dict:
        """
        Validate the current access token
        
        Returns:
            dict: Token validation data
        """
        return self._make_request("me", params={"fields": "id"})

# Example usage functions
def example_user_operations(access_token: str):
    """
    Example of user-related operations
    """
    print("Facebook API - User Operations Example")
    print("=" * 40)
    
    api = FacebookGraphAPI(access_token)
    
    try:
        # Get user profile
        print("1. Getting user profile...")
        profile = api.get_user_profile()
        print(f"User: {profile.get('name')} (ID: {profile.get('id')})")
        
        # Get user posts
        print("\n2. Getting user posts...")
        posts = api.get_user_posts(limit=5)
        print(f"Found {len(posts.get('data', []))} posts")
        
        # Get user photos
        print("\n3. Getting user photos...")
        photos = api.get_user_photos(limit=5)
        print(f"Found {len(photos.get('data', []))} photos")
        
        # Validate token
        print("\n4. Validating token...")
        validation = api.validate_token()
        print(f"Token is valid for user ID: {validation.get('id')}")
        
    except Exception as e:
        print(f"Error: {e}")

def example_page_operations(access_token: str, page_id: str):
    """
    Example of page-related operations
    """
    print("Facebook API - Page Operations Example")
    print("=" * 40)
    
    api = FacebookGraphAPI(access_token)
    
    try:
        # Get page info
        print("1. Getting page information...")
        page_info = api.get_page_info(page_id)
        print(f"Page: {page_info.get('name')} (Category: {page_info.get('category')})")
        
        # Get page posts
        print("\n2. Getting page posts...")
        posts = api.get_page_posts(page_id, limit=5)
        print(f"Found {len(posts.get('data', []))} posts")
        
        # Search pages
        print("\n3. Searching for pages...")
        search_results = api.search_pages("technology", limit=3)
        print(f"Found {len(search_results.get('data', []))} pages")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage
    print("Facebook Graph API Client")
    print("=" * 25)
    print("This is a standalone client for Facebook Graph API.")
    print("To use it, you need a valid Facebook access token.")
    print("\nExample usage:")
    print("1. Get an access token from Facebook Developers")
    print("2. Create an instance: api = FacebookGraphAPI('your_token')")
    print("3. Call methods: profile = api.get_user_profile()")
    print("\nAvailable methods:")
    
    methods = [method for method in dir(FacebookGraphAPI) if not method.startswith('_')]
    for method in methods:
        print(f"  - {method}")