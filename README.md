# Facebook Login Using Python

A comprehensive implementation of Facebook Login and Graph API integration using Python Flask.

## Features

- 🔐 **OAuth 2.0 Login**: Complete Facebook OAuth implementation
- 🌐 **Web Interface**: Beautiful Flask web app with login/logout
- 📱 **Graph API Client**: Standalone client for Facebook Graph API
- 🔄 **Session Management**: Secure user session handling
- 📊 **API Endpoints**: RESTful endpoints for user data
- 🛡️ **Error Handling**: Robust error handling and validation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Configure OAuth redirect URIs

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Facebook app credentials
```

### 4. Run the Application

```bash
python facebook_login.py
```

Visit `http://localhost:5000` to see the login interface.

## Project Structure

```
├── facebook_login.py       # Main Flask application with OAuth
├── facebook_api_client.py  # Standalone Graph API client
├── examples.py            # Usage examples and demonstrations
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Facebook App Setup

### 1. Create Facebook App

1. Visit [Facebook Developers](https://developers.facebook.com/apps/)
2. Click "Create App"
3. Choose "Consumer" app type
4. Fill in app details

### 2. Configure Facebook Login

1. In your app dashboard, click "Add Product"
2. Add "Facebook Login"
3. Go to Facebook Login → Settings
4. Add Valid OAuth Redirect URIs:
   - `http://localhost:5000/callback` (for development)
   - `https://yourdomain.com/callback` (for production)

### 3. Get App Credentials

1. Go to Settings → Basic
2. Copy your App ID and App Secret
3. Add them to your `.env` file

## Usage Examples

### Web-based OAuth Login

```python
# The main Flask app provides routes for:
# /login - Initiate Facebook login
# /callback - Handle OAuth callback
# /user - Get current user info (JSON)
# /logout - Logout user
```

### Programmatic API Access

```python
from facebook_api_client import FacebookGraphAPI

# Initialize with access token
api = FacebookGraphAPI('your_access_token')

# Get user profile
profile = api.get_user_profile()
print(f"Hello, {profile['name']}!")

# Get user posts
posts = api.get_user_posts(limit=10)
for post in posts['data']:
    print(post.get('message', 'No message'))

# Get page information
page_info = api.get_page_info('page_id')
print(f"Page: {page_info['name']}")
```

### Flask Integration

```python
from flask import Flask, session
from facebook_api_client import FacebookGraphAPI

@app.route('/dashboard')
def dashboard():
    access_token = session.get('access_token')
    if access_token:
        api = FacebookGraphAPI(access_token)
        profile = api.get_user_profile()
        return render_template('dashboard.html', user=profile)
    return redirect('/login')
```

## API Reference

### FacebookGraphAPI Class

#### User Operations
- `get_user_profile(user_id, fields)` - Get user profile information
- `get_user_posts(user_id, limit)` - Get user's posts
- `get_user_photos(user_id, limit)` - Get user's photos
- `get_user_friends(user_id)` - Get user's friends (limited)

#### Page Operations
- `get_page_info(page_id, fields)` - Get page information
- `get_page_posts(page_id, limit)` - Get page posts
- `post_to_page(page_id, message, page_token)` - Post to page
- `search_pages(query, limit)` - Search for pages

#### Utility Operations
- `validate_token()` - Validate access token
- `get_insights(object_id, metric, period)` - Get analytics data

## Environment Variables

Create a `.env` file with the following variables:

```env
FACEBOOK_CLIENT_ID=your_facebook_app_id
FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=your-secret-key-for-flask-sessions
```

## Permissions and Scopes

The application requests the following Facebook permissions:
- `email` - Access to user's email address
- `public_profile` - Access to public profile information

For additional functionality, you may need:
- `user_posts` - Access to user's posts
- `user_photos` - Access to user's photos
- `pages_read_engagement` - Read page insights
- `pages_manage_posts` - Post to pages

## Security Considerations

1. **Never expose your App Secret** - Keep it secure on the server
2. **Use HTTPS in production** - Required for OAuth callbacks
3. **Validate all tokens** - Check token validity before API calls
4. **Handle token expiration** - Implement token refresh logic
5. **Limit permissions** - Only request necessary permissions

## Troubleshooting

### Common Issues

1. **"Invalid OAuth access token"**
   - Check if token has expired
   - Verify token was generated for your app
   - Ensure required permissions are granted

2. **"URL not allowed by the Application configuration"**
   - Add your callback URL to Facebook app settings
   - Check for typos in the redirect URI

3. **"This app is in development mode"**
   - Add test users in Facebook app dashboard
   - Or submit app for review to make it public

4. **Permission errors**
   - Check if user granted required permissions
   - Some permissions require app review

### Testing

1. Use [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/) to test API calls
2. Generate test access tokens for development
3. Use Facebook's webhook testing tools for callback URLs

## Production Deployment

1. **Update redirect URIs** in Facebook app settings
2. **Use HTTPS** for all OAuth callbacks
3. **Set secure environment variables**
4. **Configure proper error logging**
5. **Implement rate limiting**
6. **Add monitoring and health checks**

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Facebook's documentation
3. Create an issue in this repository