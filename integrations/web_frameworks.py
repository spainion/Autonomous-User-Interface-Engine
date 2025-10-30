"""
Web Framework Integrations for Context Engine

Provides middleware and adapters for popular web frameworks:
- Flask
- FastAPI
- Django
- Express.js compatibility
"""

from typing import Any, Callable, Optional
import json


class FlaskContextMiddleware:
    """Flask middleware for automatic context injection"""
    
    def __init__(self, app, context_engine):
        self.app = app
        self.context_engine = context_engine
        self._setup_middleware()
    
    def _setup_middleware(self):
        """Setup Flask middleware"""
        @self.app.before_request
        def inject_context():
            from flask import g, request
            # Store context engine in Flask's g object
            g.context_engine = self.context_engine
            
            # Add request info to context
            if hasattr(request, 'json') and request.json:
                node = self.context_engine.add_node_with_text(
                    json.dumps(request.json),
                    f"request_{request.endpoint}"
                )
                g.request_node = node
        
        @self.app.after_request
        def store_response(response):
            from flask import g
            # Optionally store response in context
            if hasattr(g, 'request_node') and response.status_code == 200:
                try:
                    response_data = response.get_json()
                    if response_data:
                        self.context_engine.add_node_with_text(
                            json.dumps(response_data),
                            f"response_{g.request_node.id}"
                        )
                except Exception:
                    pass
            return response


class FastAPIContextDependency:
    """FastAPI dependency for context injection"""
    
    def __init__(self, context_engine):
        self.context_engine = context_engine
    
    async def __call__(self):
        """Return context engine for dependency injection"""
        return self.context_engine


class DjangoContextMiddleware:
    """Django middleware for context integration"""
    
    def __init__(self, get_response, context_engine=None):
        self.get_response = get_response
        self.context_engine = context_engine
    
    def __call__(self, request):
        # Add context engine to request
        request.context_engine = self.context_engine
        
        # Process request
        response = self.get_response(request)
        
        return response


class ExpressJSCompatibleAPI:
    """Express.js-style API for Node.js interoperability"""
    
    def __init__(self, context_engine):
        self.context_engine = context_engine
        self.routes = {}
    
    def route(self, path: str, method: str = "GET"):
        """Decorator for defining routes"""
        def decorator(func: Callable):
            self.routes[f"{method}:{path}"] = func
            return func
        return decorator
    
    def use(self, middleware: Callable):
        """Add middleware (Express.js style)"""
        pass  # Middleware implementation
    
    def get_route_handler(self, path: str, method: str = "GET"):
        """Get handler for a route"""
        return self.routes.get(f"{method}:{path}")


# Factory functions for easy setup
def setup_flask(app, context_engine):
    """Setup Flask integration"""
    return FlaskContextMiddleware(app, context_engine)


def setup_fastapi(context_engine):
    """Setup FastAPI integration"""
    from fastapi import Depends
    dependency = FastAPIContextDependency(context_engine)
    return dependency


def setup_django(context_engine):
    """Setup Django integration"""
    def middleware_factory(get_response):
        return DjangoContextMiddleware(get_response, context_engine)
    return middleware_factory
