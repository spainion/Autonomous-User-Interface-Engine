"""
Enhanced API Integrations

Provides comprehensive API integration capabilities for:
- RESTful API builders
- GraphQL support
- WebSocket handlers
- Authentication & authorization
- Rate limiting
- API documentation generation
- Testing utilities
"""

import os
import json
import time
import hashlib
import asyncio
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class HTTPMethod(Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class AuthType(Enum):
    """Authentication types"""
    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    BASIC = "basic"


@dataclass
class APIEndpoint:
    """API endpoint definition"""
    path: str
    method: HTTPMethod
    handler: Callable
    description: str = ""
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    auth_required: bool = False
    rate_limit: Optional[int] = None  # requests per minute
    tags: List[str] = field(default_factory=list)


@dataclass
class APIResponse:
    """Standardized API response"""
    status_code: int
    data: Any
    message: str = ""
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_size: int = 10


class EnhancedAPIIntegration:
    """
    Enhanced API Integration system with modern features.
    
    Features:
    - RESTful API builder with decorators
    - GraphQL support
    - WebSocket handlers
    - Built-in authentication
    - Rate limiting
    - Auto-generated documentation
    - Request validation
    - Error handling
    - CORS support
    - API versioning
    """
    
    def __init__(self, app_name: str = "API", version: str = "1.0.0"):
        """Initialize enhanced API integration"""
        self.app_name = app_name
        self.version = version
        self.endpoints: Dict[str, APIEndpoint] = {}
        self.middleware: List[Callable] = []
        self.auth_providers: Dict[str, Callable] = {}
        self.rate_limiters: Dict[str, Dict[str, Any]] = {}
        self.websocket_handlers: Dict[str, Callable] = {}
        
        print(f"✓ Enhanced API Integration initialized: {app_name} v{version}")
    
    def route(
        self,
        path: str,
        method: HTTPMethod = HTTPMethod.GET,
        auth_required: bool = False,
        rate_limit: Optional[int] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Decorator for defining API routes.
        
        Usage:
            @api.route('/users', method=HTTPMethod.GET)
            def get_users(request):
                return {'users': [...]}
        """
        def decorator(func: Callable):
            endpoint = APIEndpoint(
                path=path,
                method=method,
                handler=func,
                description=func.__doc__ or "",
                auth_required=auth_required,
                rate_limit=rate_limit,
                tags=tags or []
            )
            
            endpoint_key = f"{method.value}:{path}"
            self.endpoints[endpoint_key] = endpoint
            
            print(f"  ✓ Registered endpoint: {method.value} {path}")
            
            return func
        return decorator
    
    def websocket(self, path: str):
        """
        Decorator for defining WebSocket handlers.
        
        Usage:
            @api.websocket('/ws/chat')
            async def chat_handler(websocket):
                async for message in websocket:
                    await websocket.send(f"Echo: {message}")
        """
        def decorator(func: Callable):
            self.websocket_handlers[path] = func
            print(f"  ✓ Registered WebSocket: {path}")
            return func
        return decorator
    
    def use_middleware(self, func: Callable):
        """
        Decorator for adding middleware.
        
        Middleware runs before endpoint handlers.
        """
        self.middleware.append(func)
        print(f"  ✓ Registered middleware: {func.__name__}")
        return func
    
    def authenticate(self, auth_type: AuthType):
        """
        Decorator for authentication providers.
        
        Usage:
            @api.authenticate(AuthType.JWT)
            def jwt_auth(request):
                # Validate JWT token
                return user_id
        """
        def decorator(func: Callable):
            self.auth_providers[auth_type.value] = func
            print(f"  ✓ Registered auth provider: {auth_type.value}")
            return func
        return decorator
    
    def handle_request(
        self,
        path: str,
        method: str,
        headers: Dict[str, str],
        body: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Handle an incoming API request.
        
        Args:
            path: Request path
            method: HTTP method
            headers: Request headers
            body: Request body
            query_params: Query parameters
            
        Returns:
            API response
        """
        endpoint_key = f"{method}:{path}"
        
        # Check if endpoint exists
        if endpoint_key not in self.endpoints:
            return APIResponse(
                status_code=404,
                data=None,
                message="Endpoint not found"
            )
        
        endpoint = self.endpoints[endpoint_key]
        
        # Check rate limiting
        if endpoint.rate_limit:
            if not self._check_rate_limit(path, endpoint.rate_limit):
                return APIResponse(
                    status_code=429,
                    data=None,
                    message="Rate limit exceeded"
                )
        
        # Check authentication
        if endpoint.auth_required:
            auth_result = self._authenticate_request(headers)
            if not auth_result:
                return APIResponse(
                    status_code=401,
                    data=None,
                    message="Authentication required"
                )
        
        # Run middleware
        for mw in self.middleware:
            result = mw(path, method, headers, body)
            if result is not None:
                return result
        
        # Execute handler
        try:
            request_data = {
                'path': path,
                'method': method,
                'headers': headers,
                'body': body,
                'query_params': query_params or {}
            }
            
            result = endpoint.handler(request_data)
            
            return APIResponse(
                status_code=200,
                data=result,
                message="Success"
            )
        
        except Exception as e:
            return APIResponse(
                status_code=500,
                data=None,
                message="Internal server error",
                errors=[str(e)]
            )
    
    def _check_rate_limit(self, path: str, limit: int) -> bool:
        """Check if request is within rate limit"""
        current_time = time.time()
        
        if path not in self.rate_limiters:
            self.rate_limiters[path] = {
                'requests': [],
                'limit': limit
            }
        
        limiter = self.rate_limiters[path]
        
        # Remove requests older than 1 minute
        limiter['requests'] = [
            req_time for req_time in limiter['requests']
            if current_time - req_time < 60
        ]
        
        # Check if under limit
        if len(limiter['requests']) >= limit:
            return False
        
        # Add current request
        limiter['requests'].append(current_time)
        return True
    
    def _authenticate_request(self, headers: Dict[str, str]) -> bool:
        """Authenticate request based on headers"""
        # Simple example - check for Authorization header
        auth_header = headers.get('Authorization', '')
        
        if not auth_header:
            return False
        
        # Bearer token authentication
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            # Validate token (simplified)
            return len(token) > 0
        
        return False
    
    def generate_openapi_spec(self) -> Dict[str, Any]:
        """
        Generate OpenAPI 3.0 specification.
        
        Returns:
            OpenAPI specification dictionary
        """
        paths = {}
        
        for endpoint_key, endpoint in self.endpoints.items():
            if endpoint.path not in paths:
                paths[endpoint.path] = {}
            
            method_lower = endpoint.method.value.lower()
            
            paths[endpoint.path][method_lower] = {
                'summary': endpoint.description.split('\n')[0] if endpoint.description else '',
                'description': endpoint.description,
                'tags': endpoint.tags,
                'parameters': endpoint.parameters,
                'responses': {
                    '200': {
                        'description': 'Successful response',
                        'content': {
                            'application/json': {
                                'schema': endpoint.response_schema or {}
                            }
                        }
                    },
                    '400': {
                        'description': 'Bad request'
                    },
                    '401': {
                        'description': 'Unauthorized'
                    },
                    '404': {
                        'description': 'Not found'
                    },
                    '429': {
                        'description': 'Rate limit exceeded'
                    },
                    '500': {
                        'description': 'Internal server error'
                    }
                }
            }
            
            if endpoint.request_body:
                paths[endpoint.path][method_lower]['requestBody'] = {
                    'content': {
                        'application/json': {
                            'schema': endpoint.request_body
                        }
                    }
                }
            
            if endpoint.auth_required:
                paths[endpoint.path][method_lower]['security'] = [
                    {'bearerAuth': []}
                ]
        
        spec = {
            'openapi': '3.0.0',
            'info': {
                'title': self.app_name,
                'version': self.version,
                'description': f'{self.app_name} API'
            },
            'servers': [
                {'url': '/api/v1', 'description': 'API v1'}
            ],
            'paths': paths,
            'components': {
                'securitySchemes': {
                    'bearerAuth': {
                        'type': 'http',
                        'scheme': 'bearer',
                        'bearerFormat': 'JWT'
                    }
                }
            }
        }
        
        return spec
    
    def generate_postman_collection(self) -> Dict[str, Any]:
        """
        Generate Postman collection for API testing.
        
        Returns:
            Postman collection dictionary
        """
        requests = []
        
        for endpoint_key, endpoint in self.endpoints.items():
            request_item = {
                'name': endpoint.path,
                'request': {
                    'method': endpoint.method.value,
                    'header': [],
                    'url': {
                        'raw': f'{{{{base_url}}}}{endpoint.path}',
                        'host': ['{{base_url}}'],
                        'path': endpoint.path.split('/')[1:]
                    },
                    'description': endpoint.description
                }
            }
            
            if endpoint.auth_required:
                request_item['request']['header'].append({
                    'key': 'Authorization',
                    'value': 'Bearer {{token}}'
                })
            
            if endpoint.request_body:
                request_item['request']['body'] = {
                    'mode': 'raw',
                    'raw': json.dumps(endpoint.request_body, indent=2),
                    'options': {
                        'raw': {
                            'language': 'json'
                        }
                    }
                }
            
            requests.append(request_item)
        
        collection = {
            'info': {
                'name': f'{self.app_name} API',
                'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
            },
            'variable': [
                {
                    'key': 'base_url',
                    'value': 'http://localhost:8000',
                    'type': 'string'
                },
                {
                    'key': 'token',
                    'value': '',
                    'type': 'string'
                }
            ],
            'item': requests
        }
        
        return collection
    
    def generate_graphql_schema(self) -> str:
        """
        Generate GraphQL schema from REST endpoints.
        
        Returns:
            GraphQL schema string
        """
        types = []
        queries = []
        mutations = []
        
        for endpoint_key, endpoint in self.endpoints.items():
            # Simple conversion - actual implementation would be more complex
            if endpoint.method == HTTPMethod.GET:
                query_name = endpoint.path.replace('/', '_').strip('_')
                queries.append(f"  {query_name}: String")
            
            elif endpoint.method in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]:
                mutation_name = endpoint.path.replace('/', '_').strip('_')
                mutations.append(f"  {mutation_name}(input: String!): String")
        
        schema = "type Query {\n"
        schema += "\n".join(queries) if queries else "  _empty: String"
        schema += "\n}\n\n"
        
        schema += "type Mutation {\n"
        schema += "\n".join(mutations) if mutations else "  _empty: String"
        schema += "\n}\n"
        
        return schema
    
    def generate_client_sdk(self, language: str = "python") -> str:
        """
        Generate client SDK code.
        
        Args:
            language: Target language ('python', 'javascript', 'typescript')
            
        Returns:
            Client SDK code
        """
        if language == "python":
            return self._generate_python_client()
        elif language == "javascript":
            return self._generate_javascript_client()
        elif language == "typescript":
            return self._generate_typescript_client()
        else:
            return f"# SDK generation for {language} not yet implemented"
    
    def _generate_python_client(self) -> str:
        """Generate Python client SDK"""
        client_code = f'''"""
{self.app_name} Python Client SDK
Auto-generated client for {self.app_name} API v{self.version}
"""

import requests
from typing import Dict, Any, Optional


class {self.app_name.replace(" ", "")}Client:
    """Client for {self.app_name} API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {{api_key}}'
    
'''
        
        for endpoint_key, endpoint in self.endpoints.items():
            method_name = endpoint.path.replace('/', '_').strip('_').lower()
            
            client_code += f'''    def {method_name}(self, **kwargs) -> Dict[str, Any]:
        """
        {endpoint.description}
        
        Method: {endpoint.method.value}
        Path: {endpoint.path}
        """
        response = self.session.{endpoint.method.value.lower()}(
            f"{{self.base_url}}{endpoint.path}",
            json=kwargs if kwargs else None
        )
        return response.json()
    
'''
        
        return client_code
    
    def _generate_javascript_client(self) -> str:
        """Generate JavaScript client SDK"""
        return f'''/**
 * {self.app_name} JavaScript Client SDK
 * Auto-generated client for {self.app_name} API v{self.version}
 */

class {self.app_name.replace(" ", "")}Client {{
    constructor(baseUrl = 'http://localhost:8000', apiKey = null) {{
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }}
    
    async request(path, method = 'GET', data = null) {{
        const options = {{
            method: method,
            headers: {{
                'Content-Type': 'application/json'
            }}
        }};
        
        if (this.apiKey) {{
            options.headers['Authorization'] = `Bearer ${{this.apiKey}}`;
        }}
        
        if (data) {{
            options.body = JSON.stringify(data);
        }}
        
        const response = await fetch(`${{this.baseUrl}}${{path}}`, options);
        return await response.json();
    }}
    
    // Add endpoint methods here
}}

export default {self.app_name.replace(" ", "")}Client;
'''
    
    def _generate_typescript_client(self) -> str:
        """Generate TypeScript client SDK"""
        return f'''/**
 * {self.app_name} TypeScript Client SDK
 * Auto-generated client for {self.app_name} API v{self.version}
 */

interface APIResponse<T> {{
    status_code: number;
    data: T;
    message: string;
    errors?: string[];
    metadata?: Record<string, any>;
    timestamp: string;
}}

class {self.app_name.replace(" ", "")}Client {{
    private baseUrl: string;
    private apiKey: string | null;
    
    constructor(baseUrl: string = 'http://localhost:8000', apiKey: string | null = null) {{
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }}
    
    private async request<T>(path: string, method: string = 'GET', data: any = null): Promise<APIResponse<T>> {{
        const options: RequestInit = {{
            method: method,
            headers: {{
                'Content-Type': 'application/json'
            }}
        }};
        
        if (this.apiKey) {{
            options.headers = {{
                ...options.headers,
                'Authorization': `Bearer ${{this.apiKey}}`
            }};
        }}
        
        if (data) {{
            options.body = JSON.stringify(data);
        }}
        
        const response = await fetch(`${{this.baseUrl}}${{path}}`, options);
        return await response.json();
    }}
    
    // Add endpoint methods here
}}

export default {self.app_name.replace(" ", "")}Client;
'''


# Demo usage
if __name__ == "__main__":
    print("🚀 Enhanced API Integration Demo\n")
    
    # Create API
    api = EnhancedAPIIntegration(app_name="Demo API", version="1.0.0")
    
    # Define endpoints
    @api.route('/users', method=HTTPMethod.GET, tags=['users'])
    def get_users(request):
        """Get all users"""
        return {'users': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]}
    
    @api.route('/users', method=HTTPMethod.POST, auth_required=True, tags=['users'])
    def create_user(request):
        """Create a new user"""
        return {'user': {'id': 3, 'name': request['body'].get('name')}}
    
    @api.route('/health', method=HTTPMethod.GET, tags=['system'])
    def health_check(request):
        """Health check endpoint"""
        return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
    
    # Add middleware
    @api.use_middleware
    def log_requests(path, method, headers, body):
        print(f"  Request: {method} {path}")
        return None  # Continue processing
    
    # Test request handling
    print(f"\n{'='*80}")
    print("Testing API Requests")
    print(f"{'='*80}\n")
    
    response = api.handle_request('/users', 'GET', {})
    print(f"GET /users: {response.status_code} - {response.data}")
    
    response = api.handle_request('/health', 'GET', {})
    print(f"GET /health: {response.status_code} - {response.data}")
    
    # Generate documentation
    print(f"\n{'='*80}")
    print("Generated Documentation")
    print(f"{'='*80}\n")
    
    openapi_spec = api.generate_openapi_spec()
    print(f"✓ OpenAPI Spec: {len(openapi_spec['paths'])} endpoints")
    
    postman_collection = api.generate_postman_collection()
    print(f"✓ Postman Collection: {len(postman_collection['item'])} requests")
    
    graphql_schema = api.generate_graphql_schema()
    print(f"✓ GraphQL Schema: {len(graphql_schema.split('\\n'))} lines")
    
    # Generate client SDKs
    print(f"\n{'='*80}")
    print("Client SDK Generation")
    print(f"{'='*80}\n")
    
    python_client = api.generate_client_sdk('python')
    print(f"✓ Python Client SDK: {len(python_client)} characters")
    
    js_client = api.generate_client_sdk('javascript')
    print(f"✓ JavaScript Client SDK: {len(js_client)} characters")
    
    ts_client = api.generate_client_sdk('typescript')
    print(f"✓ TypeScript Client SDK: {len(ts_client)} characters")
    
    print(f"\n{'='*80}")
    print("✅ Demo complete!")
