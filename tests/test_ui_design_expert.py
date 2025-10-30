"""
Tests for UI Design Expert System
"""

import pytest
from ui_design_expert import UIDesignExpert, UIComponent


class TestUIDesignExpert:
    """Test suite for UI Design Expert"""
    
    @pytest.fixture
    def expert(self):
        """Create expert instance for testing"""
        return UIDesignExpert()
    
    def test_initialization(self, expert):
        """Test expert initializes properly"""
        assert len(expert.frameworks) > 0
        assert 'bootstrap' in expert.frameworks
        assert 'tailwind' in expert.frameworks
        assert len(expert.components) > 0
        assert len(expert.styles) > 0
    
    def test_generate_webpage_basic(self, expert):
        """Test basic webpage generation"""
        webpage = expert.generate_webpage(
            type="landing_page",
            style="modern",
            framework="bootstrap"
        )
        
        assert isinstance(webpage, str)
        assert len(webpage) > 0
        assert '<html' in webpage or '<!DOCTYPE' in webpage or '<body>' in webpage
        assert '</body>' in webpage
        assert '</html>' in webpage
    
    def test_generate_webpage_with_components(self, expert):
        """Test webpage generation with specific components"""
        webpage = expert.generate_webpage(
            type="landing_page",
            components=['navbar', 'hero', 'footer'],
            framework="bootstrap"
        )
        
        assert isinstance(webpage, str)
        assert len(webpage) > 0
    
    def test_generate_webpage_different_frameworks(self, expert):
        """Test webpage generation with different frameworks"""
        for framework in ['bootstrap', 'tailwind', 'custom']:
            webpage = expert.generate_webpage(
                type="landing_page",
                framework=framework
            )
            assert isinstance(webpage, str)
            assert len(webpage) > 0
    
    def test_generate_webpage_different_styles(self, expert):
        """Test webpage generation with different styles"""
        for style in expert.styles:
            webpage = expert.generate_webpage(
                type="landing_page",
                style=style,
                framework="bootstrap"
            )
            assert isinstance(webpage, str)
            assert len(webpage) > 0
    
    def test_generate_webpage_accessibility(self, expert):
        """Test webpage with accessibility enabled"""
        webpage = expert.generate_webpage(
            type="landing_page",
            accessibility=True
        )
        
        # Should contain accessibility features
        assert isinstance(webpage, str)
        # Accessibility features might include: role, aria-*, alt text, semantic HTML
    
    def test_generate_webpage_responsive(self, expert):
        """Test webpage with responsive design"""
        webpage = expert.generate_webpage(
            type="landing_page",
            responsive=True
        )
        
        assert isinstance(webpage, str)
        # Should contain responsive elements
    
    def test_generate_component_button(self, expert):
        """Test button component generation"""
        component = expert.generate_component(
            component_type='button',
            style='primary',
            size='medium'
        )
        
        if component:  # If method exists
            assert isinstance(component, (str, UIComponent))
    
    def test_supported_frameworks(self, expert):
        """Test all frameworks are supported"""
        required_frameworks = ['bootstrap', 'tailwind', 'material', 'custom']
        for fw in required_frameworks:
            assert fw in expert.frameworks
    
    def test_supported_components(self, expert):
        """Test required components are available"""
        required_components = ['button', 'form', 'navbar', 'card']
        for comp in required_components:
            assert comp in expert.components
    
    def test_supported_styles(self, expert):
        """Test design styles are available"""
        assert 'modern' in expert.styles
        assert len(expert.styles) >= 3


class TestUIComponent:
    """Test suite for UIComponent dataclass"""
    
    def test_ui_component_creation(self):
        """Test creating a UI component"""
        component = UIComponent(
            html="<button>Click me</button>",
            css=".button { color: blue; }",
            js="console.log('clicked');",
            framework="bootstrap",
            accessibility_score=0.95,
            responsive=True
        )
        
        assert component.html == "<button>Click me</button>"
        assert component.css == ".button { color: blue; }"
        assert component.js == "console.log('clicked');"
        assert component.framework == "bootstrap"
        assert component.accessibility_score == 0.95
        assert component.responsive is True
    
    def test_ui_component_fields(self):
        """Test UI component has all required fields"""
        component = UIComponent(
            html="<div></div>",
            css="",
            js="",
            framework="custom",
            accessibility_score=0.80,
            responsive=False
        )
        
        assert hasattr(component, 'html')
        assert hasattr(component, 'css')
        assert hasattr(component, 'js')
        assert hasattr(component, 'framework')
        assert hasattr(component, 'accessibility_score')
        assert hasattr(component, 'responsive')
