# Enhanced UI Building & API Integration Guide

## Overview

This guide covers the new enhanced UI building methods and API integration capabilities added to the Autonomous User Interface Engine.

## Date
2025-11-13

## Version
2.0.0 (Enhanced)

---

## 🎨 Enhanced UI Builder

### Overview

The Enhanced UI Builder provides modern methods for building user interfaces with support for multiple frameworks, automatic responsive design, built-in accessibility, and PWA capabilities.

### Key Features

1. **Multi-Framework Support**
   - HTML/CSS/JavaScript (vanilla)
   - React
   - Vue
   - Svelte
   - Angular
   - Tailwind CSS
   - Bootstrap

2. **Component System**
   - Reusable component definitions
   - Component composition
   - Props and children support
   - Accessibility attributes
   - Responsive configurations

3. **Automated Features**
   - Automatic responsive design
   - Built-in accessibility (WCAG 2.1)
   - Theme management (light, dark, high-contrast)
   - PWA manifest and service worker generation

4. **Layout Options**
   - Vertical stacking
   - Horizontal flex layout
   - Grid-based layouts
   - Custom breakpoints

### Quick Start

```python
from enhanced_ui_builder import EnhancedUIBuilder, UIFramework, ComponentType

# Initialize builder with framework
builder = EnhancedUIBuilder(framework=UIFramework.REACT)

# Create navigation component
nav = builder.create_component(
    name="MainNav",
    component_type=ComponentType.NAVIGATION,
    content='<ul><li><a href="#">Home</a></li></ul>',
    props={'brand': 'MyApp', 'variant': 'navbar-dark'}
)

# Create form component
form = builder.create_component(
    name="ContactForm",
    component_type=ComponentType.FORM,
    content='<input type="email" class="form-control" required>',
    props={'submit_text': 'Send Message'}
)

# Compose components
page = builder.build_page(
    title="My Application",
    components=[nav, form],
    theme="light",
    include_pwa=True
)

# Generate HTML document
html = builder.generate_html_document(page)
```

### Component Types

The builder supports these component types:

- **LAYOUT**: Page structure and containers
- **NAVIGATION**: Navigation bars, menus, breadcrumbs
- **FORM**: Forms, inputs, validation
- **DATA_DISPLAY**: Tables, lists, cards
- **FEEDBACK**: Alerts, modals, toasts
- **MEDIA**: Images, videos, galleries
- **INTERACTIVE**: Buttons, toggles, accordions

### Framework-Specific Generation

#### React Component Example

```python
builder = EnhancedUIBuilder(framework=UIFramework.REACT)
component = builder.create_component(
    name="UserCard",
    component_type=ComponentType.DATA_DISPLAY,
    content="<h3>{props.name}</h3><p>{props.email}</p>",
    props={'name': 'John Doe', 'email': 'john@example.com'}
)

# Generates:
# import React from 'react';
# function UserCard(props) {
#     return (
#         <div className="data_display">
#             <h3>{props.name}</h3><p>{props.email}</p>
#         </div>
#     );
# }
# export default UserCard;
```

#### Vue Component Example

```python
builder = EnhancedUIBuilder(framework=UIFramework.VUE)
component = builder.create_component(
    name="UserCard",
    component_type=ComponentType.DATA_DISPLAY,
    content="<h3>{{ name }}</h3><p>{{ email }}</p>",
    props={'name': 'John Doe', 'email': 'john@example.com'}
)

# Generates Vue single-file component with template, script, and style
```

### Accessibility Features

All components automatically include:

- Semantic HTML elements
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Color contrast compliance
- Focus indicators

```python
# Accessibility automatically added
component = builder.create_component(
    name="Button",
    component_type=ComponentType.INTERACTIVE,
    accessibility=True  # Default: True
)

# Results in:
# <button role="button" aria-label="interactive component">...</button>
```

### Responsive Design

Components automatically include responsive configurations:

```python
component.responsive_config = {
    'xs': {'width': '100%', 'columns': 1},   # Mobile
    'sm': {'width': '100%', 'columns': 1},   # Small tablets
    'md': {'width': '100%', 'columns': 2},   # Tablets
    'lg': {'width': '100%', 'columns': 3},   # Desktops
    'xl': {'width': '100%', 'columns': 4}    # Large screens
}
```

### PWA Support

Generate Progressive Web App features:

```python
# Build page with PWA support
page = builder.build_page(
    title="My PWA",
    components=components,
    include_pwa=True
)

# Generate PWA manifest
manifest = builder.generate_pwa_manifest(page)

# Generate service worker
service_worker = builder.generate_service_worker()

# Results in:
# - manifest.json with app configuration
# - service-worker.js with caching logic
# - Offline-first capabilities
```

### Theme Management

Three built-in themes with customization:

```python
# Built-in themes
themes = ['light', 'dark', 'high_contrast']

# Custom theme
builder.themes['custom'] = {
    'background': '#f0f0f0',
    'text': '#333333',
    'primary': '#007bff',
    'secondary': '#6c757d'
}

# Apply theme
page = builder.build_page(
    title="Themed App",
    components=components,
    theme='dark'
)
```

---

## 🚀 Enhanced API Integration

### Overview

The Enhanced API Integration system provides comprehensive tools for building modern REST APIs with authentication, rate limiting, auto-documentation, and client SDK generation.

### Key Features

1. **API Development**
   - Decorator-based route definition
   - HTTP method support (GET, POST, PUT, PATCH, DELETE)
   - Request validation
   - Response standardization

2. **Security**
   - Multiple authentication types (API key, Bearer token, OAuth2, JWT, Basic)
   - Rate limiting (per minute/hour/day)
   - CORS support
   - Middleware system

3. **Documentation**
   - OpenAPI 3.0 specification generation
   - Postman collection export
   - GraphQL schema generation
   - Interactive API explorer

4. **Client SDKs**
   - Python client generation
   - JavaScript client generation
   - TypeScript client generation
   - Auto-typed interfaces

### Quick Start

```python
from enhanced_api_integrations import (
    EnhancedAPIIntegration,
    HTTPMethod,
    AuthType
)

# Initialize API
api = EnhancedAPIIntegration(
    app_name="My API",
    version="1.0.0"
)

# Define endpoints
@api.route('/users', method=HTTPMethod.GET, tags=['users'])
def get_users(request):
    """Get all users"""
    return {'users': [...]}

@api.route('/users', method=HTTPMethod.POST, 
          auth_required=True, 
          rate_limit=10,  # 10 requests per minute
          tags=['users'])
def create_user(request):
    """Create a new user"""
    return {'user': {...}}

# Add middleware
@api.use_middleware
def log_requests(path, method, headers, body):
    print(f"Request: {method} {path}")
    return None  # Continue processing

# Handle requests
response = api.handle_request(
    path='/users',
    method='GET',
    headers={'Authorization': 'Bearer token'}
)
```

### Authentication

Support for multiple authentication types:

```python
# API Key authentication
@api.authenticate(AuthType.API_KEY)
def api_key_auth(request):
    api_key = request['headers'].get('X-API-Key')
    return validate_api_key(api_key)

# JWT authentication
@api.authenticate(AuthType.JWT)
def jwt_auth(request):
    token = request['headers'].get('Authorization', '').replace('Bearer ', '')
    return validate_jwt(token)

# OAuth2 authentication
@api.authenticate(AuthType.OAUTH2)
def oauth2_auth(request):
    token = request['headers'].get('Authorization', '').replace('Bearer ', '')
    return validate_oauth_token(token)
```

### Rate Limiting

Protect endpoints with rate limiting:

```python
# Limit to 10 requests per minute
@api.route('/api/data', 
          method=HTTPMethod.GET,
          rate_limit=10)
def get_data(request):
    return {'data': [...]}

# Custom rate limit configuration
rate_limit_config = RateLimitConfig(
    requests_per_minute=60,
    requests_per_hour=1000,
    requests_per_day=10000,
    burst_size=10
)
```

### Standardized Responses

All responses follow a consistent structure:

```python
{
    "status_code": 200,
    "data": {...},
    "message": "Success",
    "errors": [],
    "metadata": {...},
    "timestamp": "2025-11-13T04:00:00Z"
}
```

### OpenAPI Documentation

Generate complete OpenAPI 3.0 specification:

```python
# Generate OpenAPI spec
openapi_spec = api.generate_openapi_spec()

# Result:
{
    "openapi": "3.0.0",
    "info": {
        "title": "My API",
        "version": "1.0.0"
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "Get all users",
                "tags": ["users"],
                "responses": {...}
            }
        }
    }
}

# Export to file
with open('openapi.json', 'w') as f:
    json.dump(openapi_spec, f, indent=2)
```

### Postman Collection

Generate Postman collection for testing:

```python
# Generate Postman collection
collection = api.generate_postman_collection()

# Export to file
with open('postman_collection.json', 'w') as f:
    json.dump(collection, f, indent=2)

# Import into Postman:
# 1. Open Postman
# 2. Click "Import"
# 3. Select postman_collection.json
# 4. All endpoints ready to test
```

### GraphQL Schema

Convert REST API to GraphQL schema:

```python
# Generate GraphQL schema
schema = api.generate_graphql_schema()

# Result:
type Query {
    users: String
    health: String
}

type Mutation {
    users(input: String!): String
}
```

### Client SDK Generation

Auto-generate client SDKs:

#### Python Client

```python
# Generate Python client
python_client = api.generate_client_sdk('python')

# Usage:
from api_client import MyAPIClient

client = MyAPIClient(
    base_url="https://api.example.com",
    api_key="your_api_key"
)

users = client.get_users()
new_user = client.create_user(name="John", email="john@example.com")
```

#### JavaScript Client

```python
# Generate JavaScript client
js_client = api.generate_client_sdk('javascript')

# Usage:
import MyAPIClient from './api-client';

const client = new MyAPIClient(
    'https://api.example.com',
    'your_api_key'
);

const users = await client.request('/users', 'GET');
```

#### TypeScript Client

```python
# Generate TypeScript client
ts_client = api.generate_client_sdk('typescript')

# Usage:
import MyAPIClient from './api-client';

const client = new MyAPIClient(
    'https://api.example.com',
    'your_api_key'
);

const users = await client.request<User[]>('/users', 'GET');
```

---

## 🔗 Integration Examples

### Example 1: Complete Web Application

```python
from enhanced_ui_builder import EnhancedUIBuilder, UIFramework
from enhanced_api_integrations import EnhancedAPIIntegration, HTTPMethod

# Setup API
api = EnhancedAPIIntegration(app_name="My App")

@api.route('/api/data', method=HTTPMethod.GET)
def get_data(request):
    return {'items': [...]}

# Setup UI Builder
builder = EnhancedUIBuilder(framework=UIFramework.HTML_CSS_JS)

# Create UI components
nav = builder.create_component(...)
main = builder.create_component(...)
footer = builder.create_component(...)

# Build page
page = builder.build_page(
    title="My Application",
    components=[nav, main, footer],
    theme="dark",
    include_pwa=True
)

# Generate output
html = builder.generate_html_document(page)
manifest = builder.generate_pwa_manifest(page)
service_worker = builder.generate_service_worker()

# Export API docs
openapi = api.generate_openapi_spec()
postman = api.generate_postman_collection()
```

### Example 2: React Application with REST API

```python
# API Backend
api = EnhancedAPIIntegration(app_name="React App API")

@api.route('/api/users', method=HTTPMethod.GET, tags=['users'])
def get_users(request):
    return {'users': [...]}

# React Frontend
builder = EnhancedUIBuilder(framework=UIFramework.REACT)

app = builder.create_component(
    name="App",
    component_type=ComponentType.LAYOUT,
    content="<UserList /><UserForm />"
)

# Generate client SDK
client_sdk = api.generate_client_sdk('javascript')

# Deploy together
```

### Example 3: Multilingual PWA

```python
# Build multilingual PWA
builder = EnhancedUIBuilder(framework=UIFramework.VUE)

# Components with i18n support
nav = builder.create_component(
    name="Navigation",
    component_type=ComponentType.NAVIGATION,
    props={
        'brand': '{{ $t("app.name") }}',
        'items': []
    }
)

# Build PWA
page = builder.build_page(
    title="Multilingual App",
    components=[nav, ...],
    include_pwa=True,
    theme="light"
)

# Generate PWA assets
manifest = builder.generate_pwa_manifest(page)
service_worker = builder.generate_service_worker()
```

---

## 📊 Performance & Best Practices

### UI Builder Best Practices

1. **Framework Selection**
   - Use vanilla HTML/CSS/JS for static sites
   - Use React/Vue/Svelte for dynamic applications
   - Consider bundle size and performance

2. **Component Reusability**
   - Register commonly used components
   - Compose complex components from simpler ones
   - Use props for customization

3. **Accessibility**
   - Always enable accessibility features
   - Test with screen readers
   - Maintain color contrast ratios

4. **Responsive Design**
   - Test on multiple device sizes
   - Use responsive configurations
   - Consider mobile-first approach

5. **PWA Features**
   - Include PWA for offline capability
   - Cache critical resources
   - Provide offline fallbacks

### API Integration Best Practices

1. **Security**
   - Always use HTTPS in production
   - Implement authentication on sensitive endpoints
   - Use rate limiting to prevent abuse
   - Validate all inputs

2. **Documentation**
   - Generate OpenAPI specs for all APIs
   - Provide Postman collections for testing
   - Keep documentation up to date

3. **Error Handling**
   - Return consistent error responses
   - Include helpful error messages
   - Log errors for debugging

4. **Performance**
   - Implement caching where appropriate
   - Use rate limiting wisely
   - Monitor API performance

5. **Versioning**
   - Version your API (v1, v2, etc.)
   - Maintain backward compatibility
   - Deprecate old versions gracefully

---

## 🔧 Advanced Features

### Custom Component Templates

```python
# Define custom component template
builder.component_templates['custom_card'] = """
<div class="custom-card">
    <div class="card-header">{title}</div>
    <div class="card-body">{content}</div>
    <div class="card-footer">{footer}</div>
</div>
"""

# Use custom template
card = builder.create_component(
    name="CustomCard",
    template="custom_card",
    props={
        'title': 'My Card',
        'content': 'Card content',
        'footer': 'Card footer'
    }
)
```

### Middleware Chains

```python
# Add multiple middleware
@api.use_middleware
def authenticate(path, method, headers, body):
    # Authenticate request
    pass

@api.use_middleware
def log_request(path, method, headers, body):
    # Log request
    pass

@api.use_middleware
def validate_input(path, method, headers, body):
    # Validate input
    pass

# Middleware executes in order
```

### WebSocket Support

```python
# Define WebSocket handler
@api.websocket('/ws/chat')
async def chat_handler(websocket):
    async for message in websocket:
        # Process message
        response = process_chat(message)
        await websocket.send(response)

# Connect from client
# const ws = new WebSocket('ws://localhost:8000/ws/chat');
```

---

## 📝 Migration Guide

### From Basic UI Builder

```python
# Old way
old_ui = BasicUIBuilder()
html = old_ui.generate("<div>Hello</div>")

# New way
builder = EnhancedUIBuilder()
component = builder.create_component(
    name="Hello",
    component_type=ComponentType.LAYOUT,
    content="Hello"
)
page = builder.build_page("My App", [component])
html = builder.generate_html_document(page)
```

### From Basic API Integration

```python
# Old way
app = Flask(__name__)

@app.route('/users')
def get_users():
    return {'users': [...]}

# New way
api = EnhancedAPIIntegration(app_name="My API")

@api.route('/users', method=HTTPMethod.GET)
def get_users(request):
    return {'users': [...]}
```

---

## ✅ Summary

### Enhanced UI Builder
- ✅ Multi-framework support (React, Vue, Svelte, etc.)
- ✅ Automatic responsive design
- ✅ Built-in accessibility
- ✅ PWA support
- ✅ Theme management
- ✅ Component composition

### Enhanced API Integration
- ✅ Decorator-based routing
- ✅ Multiple authentication types
- ✅ Rate limiting
- ✅ OpenAPI documentation
- ✅ Postman collection export
- ✅ Client SDK generation (Python, JS, TS)
- ✅ WebSocket support

**Both systems are production-ready and fully tested!** 🚀

---

**Version**: 2.0.0  
**Date**: 2025-11-13  
**Status**: Production Ready
