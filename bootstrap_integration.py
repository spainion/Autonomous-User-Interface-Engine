"""
Bootstrap 5 Integration Module
Full integration with Bootstrap 5 for responsive, production-ready UI generation
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class BootstrapBreakpoint(Enum):
    """Bootstrap responsive breakpoints"""
    XS = "xs"  # < 576px
    SM = "sm"  # ≥ 576px
    MD = "md"  # ≥ 768px
    LG = "lg"  # ≥ 992px
    XL = "xl"  # ≥ 1200px
    XXL = "xxl"  # ≥ 1400px


class BootstrapColor(Enum):
    """Bootstrap color variants"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"


class BootstrapSize(Enum):
    """Bootstrap size variants"""
    SM = "sm"
    MD = "md"
    LG = "lg"


@dataclass
class BootstrapComponent:
    """Bootstrap component with classes and HTML"""
    html: str
    classes: List[str]
    attributes: Dict[str, str]
    component_type: str


class BootstrapIntegration:
    """
    Complete Bootstrap 5 integration for UI generation.
    
    Features:
    - Full Bootstrap 5 class support
    - Responsive grid system
    - Utility classes
    - Component generation
    - Mobile-first approach
    - Accessibility built-in
    - CDN integration
    """
    
    BOOTSTRAP_VERSION = "5.3.2"
    CDN_CSS = f"https://cdn.jsdelivr.net/npm/bootstrap@{BOOTSTRAP_VERSION}/dist/css/bootstrap.min.css"
    CDN_JS = f"https://cdn.jsdelivr.net/npm/bootstrap@{BOOTSTRAP_VERSION}/dist/js/bootstrap.bundle.min.js"
    BOOTSTRAP_ICONS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css"
    
    def __init__(self):
        """Initialize Bootstrap integration"""
        self.breakpoints = {
            'xs': 0,
            'sm': 576,
            'md': 768,
            'lg': 992,
            'xl': 1200,
            'xxl': 1400
        }
        
        print("✓ Bootstrap 5 Integration initialized")
    
    def get_cdn_links(self, include_icons: bool = True) -> Dict[str, str]:
        """
        Get Bootstrap CDN links.
        
        Args:
            include_icons: Whether to include Bootstrap Icons
        
        Returns:
            Dictionary with CSS and JS CDN links
        """
        links = {
            'css': self.CDN_CSS,
            'js': self.CDN_JS
        }
        
        if include_icons:
            links['icons'] = self.BOOTSTRAP_ICONS
        
        return links
    
    def create_responsive_grid(
        self,
        columns: List[Dict[str, Any]],
        gutter: Optional[int] = None
    ) -> str:
        """
        Create a responsive Bootstrap grid.
        
        Args:
            columns: List of column configurations with content and breakpoint sizes
            gutter: Optional gutter size (0-5)
        
        Returns:
            HTML for responsive grid
        """
        gutter_class = f"g-{gutter}" if gutter is not None else ""
        
        html = f'<div class="container">\n'
        html += f'  <div class="row {gutter_class}">\n'
        
        for col in columns:
            # Build column classes
            col_classes = []
            
            # Add responsive classes
            for breakpoint in ['xs', 'sm', 'md', 'lg', 'xl', 'xxl']:
                if breakpoint in col and col[breakpoint]:
                    size = col[breakpoint]
                    if breakpoint == 'xs':
                        col_classes.append(f'col-{size}')
                    else:
                        col_classes.append(f'col-{breakpoint}-{size}')
            
            # Default to full width if no classes
            if not col_classes:
                col_classes = ['col-12']
            
            # Add additional classes
            if 'classes' in col:
                col_classes.extend(col['classes'])
            
            html += f'    <div class="{" ".join(col_classes)}">\n'
            html += f'      {col.get("content", "")}\n'
            html += f'    </div>\n'
        
        html += f'  </div>\n'
        html += f'</div>\n'
        
        return html
    
    def create_button(
        self,
        text: str,
        variant: str = "primary",
        size: Optional[str] = None,
        outline: bool = False,
        disabled: bool = False,
        additional_classes: Optional[List[str]] = None
    ) -> str:
        """
        Create a Bootstrap button.
        
        Args:
            text: Button text
            variant: Color variant (primary, secondary, success, etc.)
            size: Size variant (sm, lg)
            outline: Whether to use outline style
            disabled: Whether button is disabled
            additional_classes: Additional CSS classes
        
        Returns:
            HTML for button
        """
        classes = ['btn']
        
        # Variant
        if outline:
            classes.append(f'btn-outline-{variant}')
        else:
            classes.append(f'btn-{variant}')
        
        # Size
        if size:
            classes.append(f'btn-{size}')
        
        # Additional classes
        if additional_classes:
            classes.extend(additional_classes)
        
        # Attributes
        attrs = []
        if disabled:
            attrs.append('disabled')
        
        attr_str = ' '.join(attrs)
        class_str = ' '.join(classes)
        
        return f'<button type="button" class="{class_str}" {attr_str}>{text}</button>'
    
    def create_card(
        self,
        title: Optional[str] = None,
        content: str = "",
        footer: Optional[str] = None,
        image_url: Optional[str] = None,
        additional_classes: Optional[List[str]] = None
    ) -> str:
        """
        Create a Bootstrap card component.
        
        Args:
            title: Card title
            content: Card content
            footer: Card footer content
            image_url: Optional image URL
            additional_classes: Additional CSS classes
        
        Returns:
            HTML for card
        """
        classes = ['card']
        if additional_classes:
            classes.extend(additional_classes)
        
        html = f'<div class="{" ".join(classes)}">\n'
        
        # Image
        if image_url:
            html += f'  <img src="{image_url}" class="card-img-top" alt="Card image">\n'
        
        html += f'  <div class="card-body">\n'
        
        # Title
        if title:
            html += f'    <h5 class="card-title">{title}</h5>\n'
        
        # Content
        html += f'    <p class="card-text">{content}</p>\n'
        
        html += f'  </div>\n'
        
        # Footer
        if footer:
            html += f'  <div class="card-footer">\n'
            html += f'    {footer}\n'
            html += f'  </div>\n'
        
        html += f'</div>\n'
        
        return html
    
    def create_navbar(
        self,
        brand: str,
        links: List[Dict[str, str]],
        theme: str = "light",
        expand_breakpoint: str = "lg",
        additional_classes: Optional[List[str]] = None
    ) -> str:
        """
        Create a Bootstrap navbar.
        
        Args:
            brand: Brand name/logo
            links: List of navigation links {text, href, active}
            theme: Theme (light, dark)
            expand_breakpoint: When to expand (sm, md, lg, xl)
            additional_classes: Additional CSS classes
        
        Returns:
            HTML for navbar
        """
        classes = ['navbar', f'navbar-expand-{expand_breakpoint}']
        
        if theme == 'dark':
            classes.extend(['navbar-dark', 'bg-dark'])
        else:
            classes.extend(['navbar-light', 'bg-light'])
        
        if additional_classes:
            classes.extend(additional_classes)
        
        html = f'<nav class="{" ".join(classes)}">\n'
        html += f'  <div class="container-fluid">\n'
        html += f'    <a class="navbar-brand" href="#">{brand}</a>\n'
        html += f'    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">\n'
        html += f'      <span class="navbar-toggler-icon"></span>\n'
        html += f'    </button>\n'
        html += f'    <div class="collapse navbar-collapse" id="navbarNav">\n'
        html += f'      <ul class="navbar-nav ms-auto">\n'
        
        for link in links:
            active_class = ' active' if link.get('active') else ''
            html += f'        <li class="nav-item">\n'
            html += f'          <a class="nav-link{active_class}" href="{link.get("href", "#")}">{link.get("text", "")}</a>\n'
            html += f'        </li>\n'
        
        html += f'      </ul>\n'
        html += f'    </div>\n'
        html += f'  </div>\n'
        html += f'</nav>\n'
        
        return html
    
    def create_form(
        self,
        fields: List[Dict[str, Any]],
        submit_text: str = "Submit",
        inline: bool = False
    ) -> str:
        """
        Create a Bootstrap form.
        
        Args:
            fields: List of form fields
            submit_text: Submit button text
            inline: Whether form is inline
        
        Returns:
            HTML for form
        """
        form_class = "row g-3" if not inline else "row row-cols-auto g-3 align-items-center"
        
        html = f'<form class="{form_class}">\n'
        
        for field in fields:
            field_type = field.get('type', 'text')
            label = field.get('label', '')
            name = field.get('name', '')
            placeholder = field.get('placeholder', '')
            required = field.get('required', False)
            
            col_class = field.get('col_class', 'col-12' if not inline else 'col-auto')
            
            html += f'  <div class="{col_class}">\n'
            
            if label:
                html += f'    <label for="{name}" class="form-label">{label}</label>\n'
            
            req_attr = ' required' if required else ''
            
            if field_type == 'textarea':
                html += f'    <textarea class="form-control" id="{name}" name="{name}" placeholder="{placeholder}"{req_attr}></textarea>\n'
            elif field_type == 'select':
                html += f'    <select class="form-select" id="{name}" name="{name}"{req_attr}>\n'
                for option in field.get('options', []):
                    html += f'      <option value="{option}">{option}</option>\n'
                html += f'    </select>\n'
            else:
                html += f'    <input type="{field_type}" class="form-control" id="{name}" name="{name}" placeholder="{placeholder}"{req_attr}>\n'
            
            html += f'  </div>\n'
        
        html += f'  <div class="col-12">\n'
        html += f'    <button type="submit" class="btn btn-primary">{submit_text}</button>\n'
        html += f'  </div>\n'
        html += f'</form>\n'
        
        return html
    
    def create_alert(
        self,
        message: str,
        variant: str = "info",
        dismissible: bool = False
    ) -> str:
        """
        Create a Bootstrap alert.
        
        Args:
            message: Alert message
            variant: Color variant
            dismissible: Whether alert is dismissible
        
        Returns:
            HTML for alert
        """
        classes = ['alert', f'alert-{variant}']
        
        if dismissible:
            classes.append('alert-dismissible fade show')
        
        html = f'<div class="{" ".join(classes)}" role="alert">\n'
        html += f'  {message}\n'
        
        if dismissible:
            html += f'  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>\n'
        
        html += f'</div>\n'
        
        return html
    
    def create_badge(
        self,
        text: str,
        variant: str = "primary",
        pill: bool = False
    ) -> str:
        """Create a Bootstrap badge"""
        classes = ['badge', f'bg-{variant}']
        if pill:
            classes.append('rounded-pill')
        
        return f'<span class="{" ".join(classes)}">{text}</span>'
    
    def create_progress_bar(
        self,
        value: int,
        max_value: int = 100,
        variant: str = "primary",
        striped: bool = False,
        animated: bool = False
    ) -> str:
        """Create a Bootstrap progress bar"""
        percentage = (value / max_value) * 100
        
        classes = ['progress-bar', f'bg-{variant}']
        if striped:
            classes.append('progress-bar-striped')
        if animated:
            classes.append('progress-bar-animated')
        
        html = f'<div class="progress">\n'
        html += f'  <div class="{" ".join(classes)}" role="progressbar" style="width: {percentage}%" '
        html += f'aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="{max_value}">{value}%</div>\n'
        html += f'</div>\n'
        
        return html
    
    def create_modal(
        self,
        modal_id: str,
        title: str,
        content: str,
        footer: Optional[str] = None,
        size: Optional[str] = None
    ) -> str:
        """Create a Bootstrap modal"""
        modal_class = "modal-dialog"
        if size:
            modal_class += f' modal-{size}'
        
        html = f'<div class="modal fade" id="{modal_id}" tabindex="-1">\n'
        html += f'  <div class="{modal_class}">\n'
        html += f'    <div class="modal-content">\n'
        html += f'      <div class="modal-header">\n'
        html += f'        <h5 class="modal-title">{title}</h5>\n'
        html += f'        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>\n'
        html += f'      </div>\n'
        html += f'      <div class="modal-body">\n'
        html += f'        {content}\n'
        html += f'      </div>\n'
        
        if footer:
            html += f'      <div class="modal-footer">\n'
            html += f'        {footer}\n'
            html += f'      </div>\n'
        
        html += f'    </div>\n'
        html += f'  </div>\n'
        html += f'</div>\n'
        
        return html
    
    def create_tabs(
        self,
        tabs: List[Dict[str, str]],
        tab_id: str = "myTab"
    ) -> str:
        """Create Bootstrap tabs"""
        html = f'<ul class="nav nav-tabs" id="{tab_id}" role="tablist">\n'
        
        for i, tab in enumerate(tabs):
            active_class = ' active' if i == 0 else ''
            html += f'  <li class="nav-item" role="presentation">\n'
            html += f'    <button class="nav-link{active_class}" id="{tab["id"]}-tab" data-bs-toggle="tab" '
            html += f'data-bs-target="#{tab["id"]}" type="button" role="tab">{tab["title"]}</button>\n'
            html += f'  </li>\n'
        
        html += f'</ul>\n'
        html += f'<div class="tab-content" id="{tab_id}Content">\n'
        
        for i, tab in enumerate(tabs):
            active_class = ' show active' if i == 0 else ''
            html += f'  <div class="tab-pane fade{active_class}" id="{tab["id"]}" role="tabpanel">\n'
            html += f'    {tab["content"]}\n'
            html += f'  </div>\n'
        
        html += f'</div>\n'
        
        return html
    
    def create_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        striped: bool = True,
        hover: bool = True,
        bordered: bool = False,
        responsive: bool = True
    ) -> str:
        """Create a Bootstrap table"""
        classes = ['table']
        if striped:
            classes.append('table-striped')
        if hover:
            classes.append('table-hover')
        if bordered:
            classes.append('table-bordered')
        
        html = ''
        if responsive:
            html += '<div class="table-responsive">\n'
        
        html += f'<table class="{" ".join(classes)}">\n'
        html += f'  <thead>\n'
        html += f'    <tr>\n'
        
        for header in headers:
            html += f'      <th scope="col">{header}</th>\n'
        
        html += f'    </tr>\n'
        html += f'  </thead>\n'
        html += f'  <tbody>\n'
        
        for row in rows:
            html += f'    <tr>\n'
            for cell in row:
                html += f'      <td>{cell}</td>\n'
            html += f'    </tr>\n'
        
        html += f'  </tbody>\n'
        html += f'</table>\n'
        
        if responsive:
            html += '</div>\n'
        
        return html
    
    def get_utility_classes(self) -> Dict[str, List[str]]:
        """Get common Bootstrap utility classes"""
        return {
            'spacing': ['m-0', 'm-1', 'm-2', 'm-3', 'm-4', 'm-5', 'p-0', 'p-1', 'p-2', 'p-3', 'p-4', 'p-5'],
            'display': ['d-block', 'd-inline', 'd-flex', 'd-grid', 'd-none'],
            'flex': ['flex-row', 'flex-column', 'justify-content-center', 'align-items-center'],
            'text': ['text-start', 'text-center', 'text-end', 'text-muted', 'text-primary'],
            'colors': ['bg-primary', 'bg-secondary', 'bg-success', 'bg-danger', 'bg-warning', 'bg-info'],
            'sizing': ['w-25', 'w-50', 'w-75', 'w-100', 'h-25', 'h-50', 'h-75', 'h-100'],
            'borders': ['border', 'border-top', 'border-end', 'border-bottom', 'border-start', 'rounded'],
            'shadows': ['shadow-none', 'shadow-sm', 'shadow', 'shadow-lg'],
        }


# Demo usage
if __name__ == "__main__":
    bootstrap = BootstrapIntegration()
    
    print("=" * 60)
    print("Bootstrap 5 Integration Demo")
    print("=" * 60)
    
    # Grid
    grid = bootstrap.create_responsive_grid([
        {"content": "Column 1", "sm": 12, "md": 6, "lg": 4},
        {"content": "Column 2", "sm": 12, "md": 6, "lg": 4},
        {"content": "Column 3", "sm": 12, "md": 12, "lg": 4}
    ])
    print("\n✓ Grid created")
    
    # Button
    button = bootstrap.create_button("Click Me", variant="primary", size="lg")
    print("✓ Button created")
    
    # Card
    card = bootstrap.create_card(title="Card Title", content="Card content", footer="Card footer")
    print("✓ Card created")
    
    # Navbar
    navbar = bootstrap.create_navbar("Brand", [
        {"text": "Home", "href": "/", "active": True},
        {"text": "About", "href": "/about"},
        {"text": "Contact", "href": "/contact"}
    ])
    print("✓ Navbar created")
    
    print("\n✅ All Bootstrap components generated successfully!")
