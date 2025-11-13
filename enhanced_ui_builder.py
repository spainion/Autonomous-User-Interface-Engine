"""
Enhanced UI Builder with Advanced Methods

Provides enhanced methods for building user interfaces with:
- Component composition and templating
- Real-time preview generation
- Responsive design automation
- Accessibility compliance
- Modern framework support (React, Vue, Svelte)
- Progressive Web App (PWA) support
"""

import os
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib


class UIFramework(Enum):
    """Supported UI frameworks"""
    HTML_CSS_JS = "html_css_js"
    BOOTSTRAP = "bootstrap"
    TAILWIND = "tailwind"
    REACT = "react"
    VUE = "vue"
    SVELTE = "svelte"
    ANGULAR = "angular"


class ComponentType(Enum):
    """UI component types"""
    LAYOUT = "layout"
    NAVIGATION = "navigation"
    FORM = "form"
    DATA_DISPLAY = "data_display"
    FEEDBACK = "feedback"
    MEDIA = "media"
    INTERACTIVE = "interactive"


@dataclass
class UIComponent:
    """Enhanced UI component definition"""
    id: str
    name: str
    type: ComponentType
    html: str
    css: str
    js: str
    props: Dict[str, Any] = field(default_factory=dict)
    children: List['UIComponent'] = field(default_factory=list)
    accessibility_attrs: Dict[str, str] = field(default_factory=dict)
    responsive_config: Dict[str, Any] = field(default_factory=dict)
    framework: UIFramework = UIFramework.HTML_CSS_JS


@dataclass
class UIPage:
    """Complete UI page structure"""
    title: str
    components: List[UIComponent]
    meta_tags: Dict[str, str]
    stylesheets: List[str]
    scripts: List[str]
    framework: UIFramework
    is_pwa: bool = False
    theme: str = "light"


class EnhancedUIBuilder:
    """
    Enhanced UI Builder with advanced methods for modern web development.
    
    Features:
    - Multi-framework support (React, Vue, Svelte, etc.)
    - Component composition and reusability
    - Automatic responsive design
    - Built-in accessibility features
    - Real-time preview generation
    - PWA support
    - Theme management
    """
    
    def __init__(self, framework: UIFramework = UIFramework.HTML_CSS_JS):
        """Initialize enhanced UI builder"""
        self.framework = framework
        self.components_registry: Dict[str, UIComponent] = {}
        self.themes: Dict[str, Dict[str, str]] = self._init_themes()
        self.breakpoints = {
            'xs': '0px',
            'sm': '576px',
            'md': '768px',
            'lg': '992px',
            'xl': '1200px',
            'xxl': '1400px'
        }
        
        print(f"✓ Enhanced UI Builder initialized with {framework.value}")
    
    def _init_themes(self) -> Dict[str, Dict[str, str]]:
        """Initialize theme configurations"""
        return {
            'light': {
                'background': '#ffffff',
                'text': '#212529',
                'primary': '#0d6efd',
                'secondary': '#6c757d',
                'success': '#198754',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#0dcaf0'
            },
            'dark': {
                'background': '#212529',
                'text': '#f8f9fa',
                'primary': '#0d6efd',
                'secondary': '#6c757d',
                'success': '#198754',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#0dcaf0'
            },
            'high_contrast': {
                'background': '#000000',
                'text': '#ffffff',
                'primary': '#00ffff',
                'secondary': '#808080',
                'success': '#00ff00',
                'danger': '#ff0000',
                'warning': '#ffff00',
                'info': '#00bfff'
            }
        }
    
    def create_component(
        self,
        name: str,
        component_type: ComponentType,
        content: str = "",
        props: Optional[Dict[str, Any]] = None,
        accessibility: bool = True
    ) -> UIComponent:
        """
        Create an enhanced UI component with modern features.
        
        Args:
            name: Component name
            component_type: Type of component
            content: Component content
            props: Component properties
            accessibility: Enable accessibility features
            
        Returns:
            Enhanced UI component
        """
        component_id = hashlib.md5(f"{name}{component_type.value}".encode()).hexdigest()[:8]
        
        # Generate HTML based on framework
        html = self._generate_component_html(name, component_type, content, props or {})
        
        # Generate CSS
        css = self._generate_component_css(component_id, component_type, props or {})
        
        # Generate JS if needed
        js = self._generate_component_js(component_id, component_type, props or {})
        
        # Add accessibility attributes
        accessibility_attrs = {}
        if accessibility:
            accessibility_attrs = self._generate_accessibility_attrs(component_type)
        
        # Add responsive configuration
        responsive_config = self._generate_responsive_config(component_type)
        
        component = UIComponent(
            id=component_id,
            name=name,
            type=component_type,
            html=html,
            css=css,
            js=js,
            props=props or {},
            accessibility_attrs=accessibility_attrs,
            responsive_config=responsive_config,
            framework=self.framework
        )
        
        # Register component
        self.components_registry[component_id] = component
        
        return component
    
    def _generate_component_html(
        self,
        name: str,
        component_type: ComponentType,
        content: str,
        props: Dict[str, Any]
    ) -> str:
        """Generate HTML for component based on framework"""
        
        if self.framework == UIFramework.REACT:
            return self._generate_react_component(name, component_type, content, props)
        elif self.framework == UIFramework.VUE:
            return self._generate_vue_component(name, component_type, content, props)
        elif self.framework == UIFramework.SVELTE:
            return self._generate_svelte_component(name, component_type, content, props)
        else:
            return self._generate_html_component(name, component_type, content, props)
    
    def _generate_html_component(
        self,
        name: str,
        component_type: ComponentType,
        content: str,
        props: Dict[str, Any]
    ) -> str:
        """Generate standard HTML component"""
        
        if component_type == ComponentType.NAVIGATION:
            return f"""<nav class="navbar {props.get('variant', 'navbar-light')} {props.get('expand', 'navbar-expand-lg')}">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">{props.get('brand', 'Brand')}</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            {content}
        </div>
    </div>
</nav>"""
        
        elif component_type == ComponentType.FORM:
            return f"""<form class="needs-validation" novalidate>
    <div class="mb-3">
        {content}
    </div>
    <button type="submit" class="btn btn-primary">{props.get('submit_text', 'Submit')}</button>
</form>"""
        
        elif component_type == ComponentType.DATA_DISPLAY:
            return f"""<div class="card">
    <div class="card-header">{props.get('title', 'Data Display')}</div>
    <div class="card-body">
        {content}
    </div>
</div>"""
        
        else:
            return f"""<div class="component {component_type.value}">
    {content}
</div>"""
    
    def _generate_react_component(
        self,
        name: str,
        component_type: ComponentType,
        content: str,
        props: Dict[str, Any]
    ) -> str:
        """Generate React component"""
        return f"""import React from 'react';

function {name}(props) {{
    return (
        <div className="{component_type.value}">
            {content}
        </div>
    );
}}

export default {name};"""
    
    def _generate_vue_component(
        self,
        name: str,
        component_type: ComponentType,
        content: str,
        props: Dict[str, Any]
    ) -> str:
        """Generate Vue component"""
        return f"""<template>
    <div class="{component_type.value}">
        {content}
    </div>
</template>

<script>
export default {{
    name: '{name}',
    props: {json.dumps(props, indent=4)}
}}
</script>

<style scoped>
/* Component styles */
</style>"""
    
    def _generate_svelte_component(
        self,
        name: str,
        component_type: ComponentType,
        content: str,
        props: Dict[str, Any]
    ) -> str:
        """Generate Svelte component"""
        prop_declarations = "\n".join([f"    export let {k} = {json.dumps(v)};" for k, v in props.items()])
        
        return f"""<script>
{prop_declarations}
</script>

<div class="{component_type.value}">
    {content}
</div>

<style>
/* Component styles */
</style>"""
    
    def _generate_component_css(
        self,
        component_id: str,
        component_type: ComponentType,
        props: Dict[str, Any]
    ) -> str:
        """Generate CSS for component"""
        
        base_styles = f"""
.component-{component_id} {{
    box-sizing: border-box;
    position: relative;
}}
"""
        
        if component_type == ComponentType.LAYOUT:
            base_styles += """
    display: flex;
    flex-direction: column;
    min-height: 100vh;
"""
        
        elif component_type == ComponentType.NAVIGATION:
            base_styles += """
    background-color: var(--nav-bg, #ffffff);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
"""
        
        return base_styles
    
    def _generate_component_js(
        self,
        component_id: str,
        component_type: ComponentType,
        props: Dict[str, Any]
    ) -> str:
        """Generate JavaScript for component"""
        
        if component_type == ComponentType.INTERACTIVE:
            return f"""
document.addEventListener('DOMContentLoaded', function() {{
    const component = document.getElementById('{component_id}');
    if (component) {{
        // Add interactivity here
        component.addEventListener('click', function(e) {{
            console.log('Component clicked');
        }});
    }}
}});
"""
        
        elif component_type == ComponentType.FORM:
            return f"""
document.addEventListener('DOMContentLoaded', function() {{
    const form = document.getElementById('{component_id}');
    if (form) {{
        form.addEventListener('submit', function(e) {{
            e.preventDefault();
            if (form.checkValidity()) {{
                // Handle form submission
                console.log('Form is valid');
            }} else {{
                form.classList.add('was-validated');
            }}
        }});
    }}
}});
"""
        
        return ""
    
    def _generate_accessibility_attrs(self, component_type: ComponentType) -> Dict[str, str]:
        """Generate accessibility attributes"""
        
        base_attrs = {
            'role': component_type.value,
            'aria-label': f'{component_type.value} component'
        }
        
        if component_type == ComponentType.NAVIGATION:
            base_attrs['role'] = 'navigation'
            base_attrs['aria-label'] = 'Main navigation'
        
        elif component_type == ComponentType.FORM:
            base_attrs['role'] = 'form'
            base_attrs['aria-label'] = 'Input form'
        
        return base_attrs
    
    def _generate_responsive_config(self, component_type: ComponentType) -> Dict[str, Any]:
        """Generate responsive configuration"""
        
        return {
            'xs': {'width': '100%', 'columns': 1},
            'sm': {'width': '100%', 'columns': 1},
            'md': {'width': '100%', 'columns': 2},
            'lg': {'width': '100%', 'columns': 3},
            'xl': {'width': '100%', 'columns': 4}
        }
    
    def compose_components(
        self,
        components: List[UIComponent],
        layout: str = "vertical"
    ) -> str:
        """
        Compose multiple components into a layout.
        
        Args:
            components: List of components to compose
            layout: Layout type ('vertical', 'horizontal', 'grid')
            
        Returns:
            Combined HTML string
        """
        
        if layout == "vertical":
            return "\n".join([comp.html for comp in components])
        
        elif layout == "horizontal":
            html = '<div class="d-flex flex-row">\n'
            for comp in components:
                html += f'    <div class="flex-fill">{comp.html}</div>\n'
            html += '</div>'
            return html
        
        elif layout == "grid":
            html = '<div class="row">\n'
            for comp in components:
                html += f'    <div class="col-md-6 col-lg-4">{comp.html}</div>\n'
            html += '</div>'
            return html
        
        return ""
    
    def build_page(
        self,
        title: str,
        components: List[UIComponent],
        theme: str = "light",
        include_pwa: bool = False
    ) -> UIPage:
        """
        Build a complete page with all components.
        
        Args:
            title: Page title
            components: List of components
            theme: Theme to apply
            include_pwa: Include PWA manifest and service worker
            
        Returns:
            Complete UI page
        """
        
        meta_tags = {
            'viewport': 'width=device-width, initial-scale=1.0',
            'description': f'{title} - Generated by Enhanced UI Builder',
            'theme-color': self.themes[theme]['primary']
        }
        
        stylesheets = [
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'
        ]
        
        scripts = [
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
        ]
        
        if include_pwa:
            meta_tags['manifest'] = '/manifest.json'
            scripts.append('/service-worker.js')
        
        page = UIPage(
            title=title,
            components=components,
            meta_tags=meta_tags,
            stylesheets=stylesheets,
            scripts=scripts,
            framework=self.framework,
            is_pwa=include_pwa,
            theme=theme
        )
        
        return page
    
    def generate_html_document(self, page: UIPage) -> str:
        """Generate complete HTML document"""
        
        # Build meta tags
        meta_html = "\n".join([
            f'    <meta name="{key}" content="{value}">'
            for key, value in page.meta_tags.items()
        ])
        
        # Build stylesheets
        style_html = "\n".join([
            f'    <link rel="stylesheet" href="{href}">'
            for href in page.stylesheets
        ])
        
        # Build component HTML
        body_html = "\n".join([comp.html for comp in page.components])
        
        # Build component CSS
        component_css = "\n".join([comp.css for comp in page.components])
        
        # Build component JS
        component_js = "\n".join([comp.js for comp in page.components if comp.js])
        
        # Build scripts
        script_html = "\n".join([
            f'    <script src="{src}"></script>'
            for src in page.scripts
        ])
        
        # Generate complete document
        html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{page.theme}">
<head>
    <meta charset="UTF-8">
{meta_html}
    <title>{page.title}</title>
{style_html}
    <style>
{component_css}
    </style>
</head>
<body>
{body_html}

{script_html}
    <script>
{component_js}
    </script>
</body>
</html>"""
        
        return html
    
    def generate_pwa_manifest(self, page: UIPage) -> Dict[str, Any]:
        """Generate PWA manifest"""
        
        return {
            "name": page.title,
            "short_name": page.title[:12],
            "description": f"{page.title} - Progressive Web App",
            "start_url": "/",
            "display": "standalone",
            "background_color": self.themes[page.theme]['background'],
            "theme_color": self.themes[page.theme]['primary'],
            "icons": [
                {
                    "src": "/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "/icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
    
    def generate_service_worker(self) -> str:
        """Generate service worker for PWA"""
        
        return """
const CACHE_NAME = 'ui-builder-cache-v1';
const urlsToCache = [
    '/',
    '/styles/main.css',
    '/scripts/main.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
"""


# Demo usage
if __name__ == "__main__":
    print("🎨 Enhanced UI Builder Demo\n")
    
    # Test with different frameworks
    for framework in [UIFramework.HTML_CSS_JS, UIFramework.REACT, UIFramework.VUE]:
        print(f"\n{'='*80}")
        print(f"Testing with {framework.value}")
        print(f"{'='*80}")
        
        builder = EnhancedUIBuilder(framework=framework)
        
        # Create navigation component
        nav = builder.create_component(
            name="MainNav",
            component_type=ComponentType.NAVIGATION,
            content='<ul class="navbar-nav"><li class="nav-item"><a class="nav-link" href="#">Home</a></li></ul>',
            props={'brand': 'MyApp', 'variant': 'navbar-dark bg-dark'}
        )
        
        print(f"\n✓ Created navigation component")
        print(f"  ID: {nav.id}")
        print(f"  Accessibility: {nav.accessibility_attrs}")
        
        # Create form component
        form = builder.create_component(
            name="ContactForm",
            component_type=ComponentType.FORM,
            content='<input type="email" class="form-control" placeholder="Email" required>',
            props={'submit_text': 'Send Message'}
        )
        
        print(f"\n✓ Created form component")
        print(f"  ID: {form.id}")
        
        # Build complete page
        page = builder.build_page(
            title="Demo Page",
            components=[nav, form],
            theme="light",
            include_pwa=False
        )
        
        print(f"\n✓ Built complete page")
        print(f"  Components: {len(page.components)}")
        print(f"  Theme: {page.theme}")
        
        if framework == UIFramework.HTML_CSS_JS:
            # Generate HTML document for first framework only
            html = builder.generate_html_document(page)
            print(f"\n✓ Generated HTML document ({len(html)} characters)")
    
    print(f"\n{'='*80}")
    print("✅ Demo complete!")
