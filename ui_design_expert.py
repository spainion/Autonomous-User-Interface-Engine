"""
Expert UI Design System
Comprehensive HTML/CSS/JavaScript generation with framework support
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class UIComponent:
    """Represents a UI component"""
    html: str
    css: str
    js: str
    framework: str
    accessibility_score: float
    responsive: bool


class UIDesignExpert:
    """Expert system for UI design and generation"""
    
    def __init__(self):
        self.frameworks = {
            'bootstrap': 'Bootstrap 5',
            'tailwind': 'Tailwind CSS 3',
            'material': 'Material-UI',
            'custom': 'Custom CSS'
        }
        
        self.components = {
            'button': self._generate_button,
            'form': self._generate_form,
            'navbar': self._generate_navbar,
            'card': self._generate_card,
            'modal': self._generate_modal,
            'table': self._generate_table,
            'footer': self._generate_footer,
            'hero': self._generate_hero,
            'sidebar': self._generate_sidebar,
            'breadcrumb': self._generate_breadcrumb
        }
        
        self.styles = ['modern', 'minimal', 'corporate', 'creative', 'elegant']
    
    def generate_webpage(
        self,
        type: str = "landing_page",
        style: str = "modern",
        framework: str = "bootstrap",
        accessibility: bool = True,
        responsive: bool = True,
        components: Optional[List[str]] = None
    ) -> str:
        """Generate complete webpage with specified parameters"""
        
        if components is None:
            components = self._get_default_components(type)
        
        html_parts = []
        css_parts = []
        js_parts = []
        
        # HTML structure
        html_parts.append(self._generate_html_head(framework, style))
        html_parts.append('<body>')
        
        # Generate each component
        for comp_name in components:
            if comp_name in self.components:
                comp = self.components[comp_name](framework, style, accessibility)
                html_parts.append(comp.html)
                css_parts.append(comp.css)
                js_parts.append(comp.js)
        
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        # Combine CSS
        if css_parts:
            style_tag = f"<style>\n{chr(10).join(css_parts)}\n</style>"
            html_parts.insert(-2, style_tag)
        
        # Combine JS
        if js_parts:
            script_tag = f"<script>\n{chr(10).join(js_parts)}\n</script>"
            html_parts.insert(-1, script_tag)
        
        return '\n'.join(html_parts)
    
    def generate_component(
        self,
        component_type: str,
        style: str = "primary",
        size: str = "medium",
        animation: Optional[str] = None,
        framework: str = "bootstrap",
        accessibility: bool = True
    ) -> UIComponent:
        """Generate a specific UI component"""
        
        if component_type in self.components:
            return self.components[component_type](framework, style, accessibility)
        
        raise ValueError(f"Unknown component type: {component_type}")
    
    def _get_default_components(self, page_type: str) -> List[str]:
        """Get default components for page type"""
        templates = {
            'landing_page': ['navbar', 'hero', 'card', 'footer'],
            'dashboard': ['navbar', 'sidebar', 'card', 'table'],
            'blog': ['navbar', 'card', 'sidebar', 'footer'],
            'ecommerce': ['navbar', 'card', 'modal', 'footer']
        }
        return templates.get(page_type, ['navbar', 'card', 'footer'])
    
    def _generate_html_head(self, framework: str, style: str) -> str:
        """Generate HTML head with framework includes"""
        
        framework_cdn = {
            'bootstrap': '''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>''',
            'tailwind': '''
    <script src="https://cdn.tailwindcss.com"></script>''',
            'material': '''
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">''',
            'custom': ''
        }
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated UI</title>{framework_cdn.get(framework, '')}
</head>'''
    
    def _generate_button(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate button component"""
        
        if framework == 'bootstrap':
            html = f'''<button type="button" class="btn btn-{style}" aria-label="Action button">
    Click Me
</button>'''
            css = ""
            js = ""
        elif framework == 'tailwind':
            html = f'''<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" aria-label="Action button">
    Click Me
</button>'''
            css = ""
            js = ""
        else:
            html = '<button class="custom-btn" aria-label="Action button">Click Me</button>'
            css = '''.custom-btn {
    padding: 10px 20px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}
.custom-btn:hover {
    background: #0056b3;
    transform: translateY(-2px);
}'''
            js = ""
        
        return UIComponent(html, css, js, framework, 95.0, True)
    
    def _generate_form(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate form component"""
        
        if framework == 'bootstrap':
            html = '''<form class="needs-validation" novalidate>
    <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input type="email" class="form-control" id="email" aria-describedby="emailHelp" required>
        <div class="invalid-feedback">Please provide a valid email.</div>
    </div>
    <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" required>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>'''
            css = ""
            js = '''
// Bootstrap form validation
(function() {
    'use strict';
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();'''
        else:
            html = '''<form class="custom-form">
    <div class="form-group">
        <label for="email">Email address</label>
        <input type="email" id="email" name="email" required aria-required="true">
    </div>
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required aria-required="true">
    </div>
    <button type="submit">Submit</button>
</form>'''
            css = '''.custom-form {
    max-width: 400px;
    margin: 0 auto;
}
.form-group {
    margin-bottom: 1rem;
}
.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
.form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}'''
            js = ""
        
        return UIComponent(html, css, js, framework, 98.0, True)
    
    def _generate_navbar(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate navigation bar"""
        
        if framework == 'bootstrap':
            html = '''<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Brand</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" 
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Features</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Pricing</a></li>
                <li class="nav-item"><a class="nav-link" href="#">About</a></li>
            </ul>
        </div>
    </div>
</nav>'''
            css = ""
            js = ""
        else:
            html = '''<nav class="custom-navbar" role="navigation">
    <div class="nav-brand">Brand</div>
    <ul class="nav-menu">
        <li><a href="#">Home</a></li>
        <li><a href="#">Features</a></li>
        <li><a href="#">Pricing</a></li>
        <li><a href="#">About</a></li>
    </ul>
</nav>'''
            css = '''.custom-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #f8f9fa;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.nav-brand {
    font-size: 1.5rem;
    font-weight: bold;
}
.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
    margin: 0;
    padding: 0;
}
.nav-menu a {
    text-decoration: none;
    color: #333;
    transition: color 0.3s;
}
.nav-menu a:hover {
    color: #007bff;
}'''
            js = ""
        
        return UIComponent(html, css, js, framework, 96.0, True)
    
    def _generate_card(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate card component"""
        
        if framework == 'bootstrap':
            html = '''<div class="card" style="width: 18rem;">
    <img src="https://via.placeholder.com/300x200" class="card-img-top" alt="Card image">
    <div class="card-body">
        <h5 class="card-title">Card Title</h5>
        <p class="card-text">Some quick example text to build on the card title.</p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>'''
            css = ""
            js = ""
        else:
            html = '''<div class="custom-card">
    <img src="https://via.placeholder.com/300x200" alt="Card image">
    <div class="card-content">
        <h3>Card Title</h3>
        <p>Some quick example text to build on the card title.</p>
        <a href="#" class="card-link">Go somewhere</a>
    </div>
</div>'''
            css = '''.custom-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}
.custom-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.custom-card img {
    width: 100%;
    height: auto;
}
.card-content {
    padding: 1.5rem;
}
.card-link {
    color: #007bff;
    text-decoration: none;
}'''
            js = ""
        
        return UIComponent(html, css, js, framework, 94.0, True)
    
    def _generate_modal(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate modal component"""
        
        html = '''<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Modal Title</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">Modal content goes here</div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
            </div>
        </div>
    </div>
</div>'''
        
        return UIComponent(html, "", "", framework, 97.0, True)
    
    def _generate_table(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate table component"""
        
        html = '''<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
            <th scope="col">Role</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">1</th>
            <td>John Doe</td>
            <td>john@example.com</td>
            <td>Admin</td>
        </tr>
        <tr>
            <th scope="row">2</th>
            <td>Jane Smith</td>
            <td>jane@example.com</td>
            <td>User</td>
        </tr>
    </tbody>
</table>'''
        
        return UIComponent(html, "", "", framework, 95.0, True)
    
    def _generate_footer(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate footer component"""
        
        html = '''<footer class="bg-dark text-white py-4 mt-5">
    <div class="container">
        <div class="row">
            <div class="col-md-4">
                <h5>About</h5>
                <p>Company description goes here.</p>
            </div>
            <div class="col-md-4">
                <h5>Links</h5>
                <ul class="list-unstyled">
                    <li><a href="#" class="text-white">Home</a></li>
                    <li><a href="#" class="text-white">About</a></li>
                    <li><a href="#" class="text-white">Contact</a></li>
                </ul>
            </div>
            <div class="col-md-4">
                <h5>Contact</h5>
                <p>Email: info@example.com</p>
            </div>
        </div>
        <hr class="bg-white">
        <p class="text-center mb-0">&copy; 2024 Company Name. All rights reserved.</p>
    </div>
</footer>'''
        
        return UIComponent(html, "", "", framework, 93.0, True)
    
    def _generate_hero(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate hero section"""
        
        html = '''<section class="hero bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-md-6">
                <h1 class="display-4">Welcome to Our Platform</h1>
                <p class="lead">Build amazing things with our powerful tools and services.</p>
                <button class="btn btn-light btn-lg">Get Started</button>
            </div>
            <div class="col-md-6">
                <img src="https://via.placeholder.com/500x400" alt="Hero image" class="img-fluid">
            </div>
        </div>
    </div>
</section>'''
        
        return UIComponent(html, "", "", framework, 92.0, True)
    
    def _generate_sidebar(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate sidebar component"""
        
        html = '''<aside class="sidebar bg-light p-3" role="complementary">
    <h4>Navigation</h4>
    <ul class="nav flex-column">
        <li class="nav-item"><a class="nav-link active" href="#">Dashboard</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Users</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Settings</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Reports</a></li>
    </ul>
</aside>'''
        
        return UIComponent(html, "", "", framework, 94.0, True)
    
    def _generate_breadcrumb(self, framework: str, style: str, accessibility: bool) -> UIComponent:
        """Generate breadcrumb navigation"""
        
        html = '''<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">Home</a></li>
        <li class="breadcrumb-item"><a href="#">Library</a></li>
        <li class="breadcrumb-item active" aria-current="page">Data</li>
    </ol>
</nav>'''
        
        return UIComponent(html, "", "", framework, 98.0, True)
    
    def get_accessibility_score(self, html: str) -> float:
        """Calculate accessibility score for HTML"""
        score = 100.0
        
        # Check for common accessibility issues
        if 'alt=' not in html and '<img' in html:
            score -= 10
        if 'aria-label' not in html and 'button' in html:
            score -= 5
        if 'role=' not in html and 'nav' not in html:
            score -= 3
        
        return max(0, score)
    
    def optimize_performance(self, html: str, css: str, js: str) -> Dict[str, str]:
        """Optimize generated code for performance"""
        # Minify CSS (basic)
        css_optimized = css.replace('\n', '').replace('  ', '')
        
        # Minify JS (basic)
        js_optimized = js.replace('\n', '').replace('  ', '')
        
        return {
            'html': html,
            'css': css_optimized,
            'js': js_optimized
        }


if __name__ == "__main__":
    expert = UIDesignExpert()
    
    # Generate a landing page
    page = expert.generate_webpage(
        type="landing_page",
        style="modern",
        framework="bootstrap",
        accessibility=True
    )
    
    print("Generated Landing Page:")
    print(page[:500] + "...")
    
    # Generate individual button
    button = expert.generate_component("button", framework="custom")
    print("\nGenerated Button:")
    print(f"HTML: {button.html}")
    print(f"CSS: {button.css[:100]}...")
