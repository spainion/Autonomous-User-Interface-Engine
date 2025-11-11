"""
Natural Language UI Interpreter
Advanced NLP-to-UI conversion using OpenRouter LLM for intelligent UI generation
"""

import os
import requests
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class UIComponentType(Enum):
    """Types of UI components that can be identified"""
    NAVIGATION = "navigation"
    HEADER = "header"
    FOOTER = "footer"
    SIDEBAR = "sidebar"
    CARD = "card"
    BUTTON = "button"
    FORM = "form"
    INPUT = "input"
    TABLE = "table"
    CHART = "chart"
    GRID = "grid"
    LIST = "list"
    MODAL = "modal"
    DROPDOWN = "dropdown"
    TAB = "tab"
    ACCORDION = "accordion"
    CAROUSEL = "carousel"
    ALERT = "alert"
    BADGE = "badge"
    PROGRESS = "progress"
    BREADCRUMB = "breadcrumb"
    PAGINATION = "pagination"
    TIMELINE = "timeline"
    HERO = "hero"
    CTA = "cta"
    TESTIMONIAL = "testimonial"
    PRICING = "pricing"
    FAQ = "faq"
    CONTACT = "contact"
    GALLERY = "gallery"
    VIDEO = "video"
    AUDIO = "audio"
    MAP = "map"


class LayoutType(Enum):
    """Types of layout structures"""
    SINGLE_COLUMN = "single_column"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"
    GRID = "grid"
    MASONRY = "masonry"
    SIDEBAR_LEFT = "sidebar_left"
    SIDEBAR_RIGHT = "sidebar_right"
    SIDEBAR_BOTH = "sidebar_both"
    DASHBOARD = "dashboard"
    LANDING = "landing"
    BLOG = "blog"
    ECOMMERCE = "ecommerce"
    ADMIN = "admin"


@dataclass
class UIInterpretation:
    """Result of NLP interpretation"""
    components: List[Dict[str, Any]]
    layout_type: LayoutType
    color_scheme: Dict[str, str]
    style_preferences: List[str]
    responsive_requirements: Dict[str, bool]
    accessibility_features: List[str]
    interactions: List[str]
    framework_preferences: List[str]
    content_sections: List[Dict[str, Any]]
    ai_reasoning: str
    confidence: float
    suggested_enhancements: List[str]


class NLPUIInterpreter:
    """
    Advanced Natural Language UI Interpreter.
    
    Uses OpenRouter LLM to intelligently parse natural language descriptions
    of user interfaces and convert them into structured UI specifications.
    
    Features:
    - Intelligent component identification
    - Layout structure recognition
    - Color scheme extraction
    - Style preference detection
    - Responsive requirement parsing
    - Accessibility feature identification
    - Framework suggestion
    - Context-aware interpretation
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize the NLP UI interpreter"""
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.app_name = os.getenv('OPENROUTER_APP_NAME', 'UI-NLP-Interpreter')
        self.site_url = os.getenv('OPENROUTER_SITE_URL', 'https://github.com')
        
        # Available models
        self.models = {
            'gpt-4': 'openai/gpt-4-turbo-preview',
            'gpt-4-32k': 'openai/gpt-4-32k',
            'claude': 'anthropic/claude-3-opus',
            'claude-sonnet': 'anthropic/claude-3-sonnet',
            'gemini': 'google/gemini-pro',
            'mixtral': 'mistralai/mixtral-8x7b-instruct',
            'llama': 'meta-llama/llama-3-70b-instruct'
        }
        
        self.current_model = model
        
        # Component keywords mapping
        self.component_keywords = {
            UIComponentType.NAVIGATION: ['navigation', 'navbar', 'nav', 'menu', 'navigation bar', 'top bar'],
            UIComponentType.HEADER: ['header', 'top section', 'page header', 'site header'],
            UIComponentType.FOOTER: ['footer', 'bottom', 'page footer', 'site footer'],
            UIComponentType.SIDEBAR: ['sidebar', 'side panel', 'side menu', 'left panel', 'right panel'],
            UIComponentType.CARD: ['card', 'panel', 'box', 'container', 'widget'],
            UIComponentType.BUTTON: ['button', 'btn', 'call to action', 'cta', 'submit', 'action button'],
            UIComponentType.FORM: ['form', 'input form', 'contact form', 'signup form', 'login form'],
            UIComponentType.INPUT: ['input', 'field', 'text field', 'input field', 'form field'],
            UIComponentType.TABLE: ['table', 'data table', 'grid table', 'list table'],
            UIComponentType.CHART: ['chart', 'graph', 'visualization', 'plot', 'diagram'],
            UIComponentType.GRID: ['grid', 'photo grid', 'image grid', 'product grid'],
            UIComponentType.LIST: ['list', 'item list', 'list view', 'listing'],
            UIComponentType.MODAL: ['modal', 'dialog', 'popup', 'overlay'],
            UIComponentType.DROPDOWN: ['dropdown', 'select', 'picker', 'menu dropdown'],
            UIComponentType.TAB: ['tab', 'tabs', 'tabbed', 'tabbed interface'],
            UIComponentType.ACCORDION: ['accordion', 'expandable', 'collapsible'],
            UIComponentType.CAROUSEL: ['carousel', 'slider', 'slideshow', 'image slider'],
            UIComponentType.HERO: ['hero', 'hero section', 'banner', 'main banner'],
            UIComponentType.PRICING: ['pricing', 'pricing table', 'plans', 'subscription'],
            UIComponentType.TESTIMONIAL: ['testimonial', 'review', 'feedback', 'testimonials'],
            UIComponentType.GALLERY: ['gallery', 'image gallery', 'photo gallery', 'portfolio'],
        }
        
        # Color keywords
        self.color_keywords = {
            'blue': '#3b82f6',
            'red': '#ef4444',
            'green': '#10b981',
            'purple': '#8b5cf6',
            'pink': '#ec4899',
            'yellow': '#f59e0b',
            'orange': '#f97316',
            'teal': '#14b8a6',
            'cyan': '#06b6d4',
            'indigo': '#6366f1',
            'gray': '#6b7280',
            'slate': '#64748b',
        }
        
        # Style keywords
        self.style_keywords = {
            'modern': ['modern', 'contemporary', 'clean', 'minimal'],
            'classic': ['classic', 'traditional', 'elegant', 'timeless'],
            'bold': ['bold', 'vibrant', 'striking', 'eye-catching'],
            'minimal': ['minimal', 'minimalist', 'simple', 'clean'],
            'dark': ['dark', 'dark mode', 'dark theme', 'night mode'],
            'light': ['light', 'bright', 'airy', 'light theme'],
            'colorful': ['colorful', 'vibrant', 'lively', 'bright colors'],
            'professional': ['professional', 'corporate', 'business', 'formal'],
            'creative': ['creative', 'artistic', 'unique', 'innovative'],
            'playful': ['playful', 'fun', 'casual', 'friendly'],
        }
        
        print(f"✓ NLP UI Interpreter initialized with {model}")
    
    def interpret_ui_request(self, request: str, use_llm: bool = True) -> UIInterpretation:
        """
        Interpret a natural language UI request.
        
        Args:
            request: Natural language description of desired UI
            use_llm: Whether to use LLM for enhanced interpretation
        
        Returns:
            Structured UI interpretation
        """
        print(f"\n🧠 Interpreting UI request...")
        print(f"Request: {request[:100]}..." if len(request) > 100 else f"Request: {request}")
        
        # Basic pattern matching interpretation
        basic_interpretation = self._basic_interpretation(request)
        
        # Enhanced LLM interpretation if available
        if use_llm and self.api_key:
            try:
                llm_interpretation = self._llm_interpretation(request, basic_interpretation)
                print(f"✓ LLM interpretation complete (confidence: {llm_interpretation.confidence:.0%})")
                return llm_interpretation
            except Exception as e:
                print(f"⚠ LLM interpretation failed, using basic: {e}")
                return basic_interpretation
        else:
            print(f"✓ Basic interpretation complete (confidence: {basic_interpretation.confidence:.0%})")
            return basic_interpretation
    
    def _basic_interpretation(self, request: str) -> UIInterpretation:
        """
        Basic pattern matching interpretation without LLM.
        Fast and reliable fallback.
        """
        request_lower = request.lower()
        
        # Identify components
        components = []
        for comp_type, keywords in self.component_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                components.append({
                    'type': comp_type.value,
                    'priority': 'high' if keywords[0] in request_lower else 'medium',
                    'properties': {}
                })
        
        # Determine layout
        layout_type = LayoutType.SINGLE_COLUMN
        if 'sidebar' in request_lower:
            if 'left' in request_lower:
                layout_type = LayoutType.SIDEBAR_LEFT
            elif 'right' in request_lower:
                layout_type = LayoutType.SIDEBAR_RIGHT
            else:
                layout_type = LayoutType.SIDEBAR_LEFT
        elif 'dashboard' in request_lower:
            layout_type = LayoutType.DASHBOARD
        elif 'grid' in request_lower:
            layout_type = LayoutType.GRID
        elif 'three column' in request_lower or '3 column' in request_lower:
            layout_type = LayoutType.THREE_COLUMN
        elif 'two column' in request_lower or '2 column' in request_lower:
            layout_type = LayoutType.TWO_COLUMN
        
        # Extract colors
        color_scheme = {'primary': '#3b82f6', 'secondary': '#64748b', 'accent': '#8b5cf6'}
        for color_name, color_value in self.color_keywords.items():
            if color_name in request_lower:
                color_scheme['primary'] = color_value
                break
        
        # Detect style preferences
        style_preferences = []
        for style, keywords in self.style_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                style_preferences.append(style)
        
        if not style_preferences:
            style_preferences = ['modern']
        
        # Responsive requirements
        responsive_requirements = {
            'mobile': 'mobile' in request_lower or 'responsive' in request_lower,
            'tablet': 'tablet' in request_lower or 'responsive' in request_lower,
            'desktop': True,
        }
        
        # Accessibility features
        accessibility_features = []
        if 'accessible' in request_lower or 'accessibility' in request_lower:
            accessibility_features.extend(['aria-labels', 'semantic-html', 'keyboard-navigation', 'screen-reader'])
        else:
            accessibility_features = ['semantic-html']
        
        # Framework preferences
        framework_preferences = []
        if 'bootstrap' in request_lower:
            framework_preferences.append('bootstrap')
        if 'tailwind' in request_lower:
            framework_preferences.append('tailwind')
        if not framework_preferences:
            framework_preferences = ['bootstrap']  # Default to Bootstrap
        
        # Content sections
        content_sections = [
            {'type': 'header', 'priority': 'high'},
            {'type': 'main', 'priority': 'high'},
            {'type': 'footer', 'priority': 'medium'},
        ]
        
        return UIInterpretation(
            components=components,
            layout_type=layout_type,
            color_scheme=color_scheme,
            style_preferences=style_preferences,
            responsive_requirements=responsive_requirements,
            accessibility_features=accessibility_features,
            interactions=['click', 'hover'] if 'interactive' in request_lower else [],
            framework_preferences=framework_preferences,
            content_sections=content_sections,
            ai_reasoning="Basic pattern matching interpretation",
            confidence=0.7,
            suggested_enhancements=[]
        )
    
    def _llm_interpretation(self, request: str, basic_interp: UIInterpretation) -> UIInterpretation:
        """
        Enhanced interpretation using OpenRouter LLM.
        Provides more accurate and context-aware analysis.
        """
        prompt = f"""You are an expert UI/UX designer and front-end architect. Analyze this UI request and provide a detailed interpretation.

Request: "{request}"

Basic interpretation found these components: {[c['type'] for c in basic_interp.components]}

Please provide a comprehensive analysis including:
1. All UI components needed (navigation, forms, cards, buttons, etc.)
2. Recommended layout structure
3. Color scheme suggestions
4. Style preferences (modern, minimal, bold, etc.)
5. Responsive requirements
6. Accessibility features to include
7. Interactive elements needed
8. Framework recommendations (Bootstrap, Tailwind, custom)
9. Content sections to include
10. Any enhancements or additional features to consider

Respond in JSON format with these keys:
- components: array of {{type, priority, properties}}
- layout_type: string
- color_scheme: {{primary, secondary, accent}}
- style_preferences: array of strings
- responsive_requirements: {{mobile, tablet, desktop}} booleans
- accessibility_features: array of strings
- interactions: array of strings
- framework_preferences: array of strings
- content_sections: array of {{type, priority}}
- suggested_enhancements: array of strings
- reasoning: string explaining your decisions
- confidence: number 0-1

Be specific and practical."""

        try:
            response = requests.post(
                self.base_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'HTTP-Referer': self.site_url,
                    'X-Title': self.app_name,
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.models.get(self.current_model, self.models['gpt-4']),
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert UI/UX designer providing structured UI analysis in JSON format.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    llm_data = json.loads(json_match.group())
                    
                    # Parse layout type
                    layout_str = llm_data.get('layout_type', 'single_column')
                    layout_type = LayoutType.SINGLE_COLUMN
                    for lt in LayoutType:
                        if lt.value in layout_str.lower() or layout_str.lower() in lt.value:
                            layout_type = lt
                            break
                    
                    return UIInterpretation(
                        components=llm_data.get('components', basic_interp.components),
                        layout_type=layout_type,
                        color_scheme=llm_data.get('color_scheme', basic_interp.color_scheme),
                        style_preferences=llm_data.get('style_preferences', basic_interp.style_preferences),
                        responsive_requirements=llm_data.get('responsive_requirements', basic_interp.responsive_requirements),
                        accessibility_features=llm_data.get('accessibility_features', basic_interp.accessibility_features),
                        interactions=llm_data.get('interactions', []),
                        framework_preferences=llm_data.get('framework_preferences', ['bootstrap']),
                        content_sections=llm_data.get('content_sections', basic_interp.content_sections),
                        ai_reasoning=llm_data.get('reasoning', ''),
                        confidence=llm_data.get('confidence', 0.85),
                        suggested_enhancements=llm_data.get('suggested_enhancements', [])
                    )
            
            # Fallback to basic if API call failed
            return basic_interp
            
        except Exception as e:
            print(f"⚠ LLM API error: {e}")
            return basic_interp
    
    def suggest_components_for_intent(self, intent: str) -> List[Dict[str, Any]]:
        """
        Suggest appropriate components based on user intent.
        
        Args:
            intent: User's intent (e.g., 'landing page', 'dashboard', 'blog')
        
        Returns:
            List of suggested components
        """
        intent_lower = intent.lower()
        
        component_suggestions = {
            'landing': [
                {'type': 'hero', 'priority': 'critical'},
                {'type': 'navigation', 'priority': 'critical'},
                {'type': 'cta', 'priority': 'high'},
                {'type': 'card', 'priority': 'high'},
                {'type': 'testimonial', 'priority': 'medium'},
                {'type': 'pricing', 'priority': 'medium'},
                {'type': 'footer', 'priority': 'medium'},
            ],
            'dashboard': [
                {'type': 'navigation', 'priority': 'critical'},
                {'type': 'sidebar', 'priority': 'critical'},
                {'type': 'card', 'priority': 'high'},
                {'type': 'chart', 'priority': 'high'},
                {'type': 'table', 'priority': 'high'},
                {'type': 'badge', 'priority': 'medium'},
                {'type': 'dropdown', 'priority': 'medium'},
            ],
            'blog': [
                {'type': 'navigation', 'priority': 'critical'},
                {'type': 'header', 'priority': 'critical'},
                {'type': 'card', 'priority': 'high'},
                {'type': 'list', 'priority': 'high'},
                {'type': 'pagination', 'priority': 'medium'},
                {'type': 'sidebar', 'priority': 'medium'},
                {'type': 'footer', 'priority': 'medium'},
            ],
            'ecommerce': [
                {'type': 'navigation', 'priority': 'critical'},
                {'type': 'grid', 'priority': 'high'},
                {'type': 'card', 'priority': 'high'},
                {'type': 'button', 'priority': 'high'},
                {'type': 'dropdown', 'priority': 'high'},
                {'type': 'badge', 'priority': 'medium'},
                {'type': 'pagination', 'priority': 'medium'},
            ],
            'admin': [
                {'type': 'sidebar', 'priority': 'critical'},
                {'type': 'navigation', 'priority': 'critical'},
                {'type': 'table', 'priority': 'high'},
                {'type': 'form', 'priority': 'high'},
                {'type': 'modal', 'priority': 'high'},
                {'type': 'alert', 'priority': 'medium'},
                {'type': 'badge', 'priority': 'medium'},
            ],
        }
        
        # Find matching intent
        for key, components in component_suggestions.items():
            if key in intent_lower:
                return components
        
        # Default components for unknown intent
        return [
            {'type': 'navigation', 'priority': 'high'},
            {'type': 'header', 'priority': 'high'},
            {'type': 'card', 'priority': 'medium'},
            {'type': 'button', 'priority': 'medium'},
            {'type': 'footer', 'priority': 'low'},
        ]
    
    def extract_color_scheme(self, text: str) -> Dict[str, str]:
        """
        Extract color scheme from text description.
        
        Args:
            text: Text containing color information
        
        Returns:
            Dictionary with primary, secondary, and accent colors
        """
        text_lower = text.lower()
        colors = {'primary': '#3b82f6', 'secondary': '#64748b', 'accent': '#8b5cf6'}
        
        # Look for specific color names
        for color_name, color_value in self.color_keywords.items():
            if color_name in text_lower:
                colors['primary'] = color_value
                break
        
        # Look for hex colors
        hex_matches = re.findall(r'#[0-9a-fA-F]{6}', text)
        if hex_matches:
            colors['primary'] = hex_matches[0]
            if len(hex_matches) > 1:
                colors['secondary'] = hex_matches[1]
            if len(hex_matches) > 2:
                colors['accent'] = hex_matches[2]
        
        return colors
    
    def determine_responsive_strategy(self, requirements: Dict[str, bool]) -> Dict[str, Any]:
        """
        Determine responsive design strategy based on requirements.
        
        Args:
            requirements: Dictionary of device requirements
        
        Returns:
            Responsive strategy configuration
        """
        strategy = {
            'approach': 'mobile-first',
            'breakpoints': {},
            'grid_system': 'bootstrap',
            'fluid_typography': True,
            'flexible_images': True,
        }
        
        if requirements.get('mobile'):
            strategy['breakpoints']['xs'] = '0px'
            strategy['breakpoints']['sm'] = '576px'
        
        if requirements.get('tablet'):
            strategy['breakpoints']['md'] = '768px'
        
        if requirements.get('desktop'):
            strategy['breakpoints']['lg'] = '992px'
            strategy['breakpoints']['xl'] = '1200px'
            strategy['breakpoints']['xxl'] = '1400px'
        
        return strategy


# Demo usage
if __name__ == "__main__":
    interpreter = NLPUIInterpreter()
    
    # Example 1: Landing page
    request1 = """
    Create a modern SaaS landing page with a hero section, 
    navigation bar, pricing cards, and testimonials. 
    Use a blue color scheme and make it mobile-responsive.
    """
    
    result1 = interpreter.interpret_ui_request(request1)
    print(f"\n📊 Interpretation Result:")
    print(f"Components: {len(result1.components)}")
    print(f"Layout: {result1.layout_type.value}")
    print(f"Colors: {result1.color_scheme}")
    print(f"Styles: {result1.style_preferences}")
    print(f"Confidence: {result1.confidence:.0%}")
    
    # Example 2: Dashboard
    request2 = """
    Build a dashboard interface with a sidebar navigation,
    data visualization charts, statistics cards, and a data table.
    Dark theme with purple accents. Needs to work on tablets.
    """
    
    result2 = interpreter.interpret_ui_request(request2)
    print(f"\n📊 Interpretation Result 2:")
    print(f"Components: {len(result2.components)}")
    print(f"Layout: {result2.layout_type.value}")
    print(f"Framework: {result2.framework_preferences}")
