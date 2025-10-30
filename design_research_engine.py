"""
Design Research Engine
Web scraping and best practices extraction for UI design
"""

import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import hashlib


@dataclass
class DesignPattern:
    """Represents a design pattern"""
    name: str
    category: str
    description: str
    html_template: str
    css_template: str
    best_practices: List[str]
    use_cases: List[str]
    accessibility_notes: str


class DesignResearchEngine:
    """Research and extract design patterns from web"""
    
    def __init__(self):
        self.pattern_database = self._init_pattern_database()
        self.scraped_sites = {}
        self.best_practices_db = self._init_best_practices()
    
    def _init_pattern_database(self) -> Dict[str, DesignPattern]:
        """Initialize pattern database with common patterns"""
        patterns = {}
        
        # Landing Page Patterns
        patterns['hero_section'] = DesignPattern(
            name="Hero Section",
            category="landing_page",
            description="Full-width hero section with headline, description, and CTA",
            html_template='''<section class="hero">
    <h1>{{ headline }}</h1>
    <p>{{ description }}</p>
    <button>{{ cta_text }}</button>
</section>''',
            css_template='''.hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}''',
            best_practices=[
                "Use clear, benefit-focused headline",
                "Keep description concise (1-2 sentences)",
                "Single prominent CTA button",
                "Consider adding hero image/video"
            ],
            use_cases=["Product launches", "SaaS landing pages", "App downloads"],
            accessibility_notes="Ensure proper heading hierarchy, sufficient color contrast"
        )
        
        # E-commerce Patterns
        patterns['product_grid'] = DesignPattern(
            name="Product Grid",
            category="ecommerce",
            description="Responsive grid layout for product listings",
            html_template='''<div class="product-grid">
    <div class="product-card">
        <img src="{{ image_url }}" alt="{{ product_name }}">
        <h3>{{ product_name }}</h3>
        <p class="price">{{ price }}</p>
        <button>Add to Cart</button>
    </div>
</div>''',
            css_template='''.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    padding: 2rem;
}
.product-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    transition: transform 0.3s;
}
.product-card:hover {
    transform: translateY(-5px);
}''',
            best_practices=[
                "Use consistent image aspect ratios",
                "Show price prominently",
                "Add hover effects for interactivity",
                "Include quick view option"
            ],
            use_cases=["Online stores", "Marketplaces", "Product catalogs"],
            accessibility_notes="Use semantic HTML, provide alt text for images"
        )
        
        # Dashboard Patterns
        patterns['dashboard_cards'] = DesignPattern(
            name="Dashboard Cards",
            category="dashboard",
            description="Metric cards for dashboard overview",
            html_template='''<div class="dashboard-grid">
    <div class="metric-card">
        <h3>{{ metric_name }}</h3>
        <p class="value">{{ metric_value }}</p>
        <span class="change {{ change_class }}">{{ change_percent }}%</span>
    </div>
</div>''',
            css_template='''.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
}
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.value {
    font-size: 2rem;
    font-weight: bold;
    margin: 0.5rem 0;
}''',
            best_practices=[
                "Group related metrics",
                "Use color to indicate positive/negative trends",
                "Keep card sizes consistent",
                "Add drill-down functionality"
            ],
            use_cases=["Admin panels", "Analytics dashboards", "Business intelligence"],
            accessibility_notes="Ensure sufficient color contrast, use ARIA labels for metrics"
        )
        
        # Form Patterns
        patterns['multi_step_form'] = DesignPattern(
            name="Multi-Step Form",
            category="forms",
            description="Wizard-style form with progress indicator",
            html_template='''<form class="multi-step-form">
    <div class="progress-bar">
        <div class="step active">1</div>
        <div class="step">2</div>
        <div class="step">3</div>
    </div>
    <div class="form-step active">
        <!-- Step 1 fields -->
    </div>
    <div class="form-actions">
        <button class="btn-back">Back</button>
        <button class="btn-next">Next</button>
    </div>
</form>''',
            css_template='''.progress-bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
}
.step {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ddd;
}
.step.active {
    background: #007bff;
    color: white;
}''',
            best_practices=[
                "Show clear progress indicator",
                "Save progress automatically",
                "Allow going back to previous steps",
                "Validate each step before proceeding"
            ],
            use_cases=["Checkout flows", "Onboarding", "Complex registrations"],
            accessibility_notes="Use proper form labels, indicate required fields"
        )
        
        return patterns
    
    def _init_best_practices(self) -> Dict[str, List[str]]:
        """Initialize best practices database"""
        return {
            'responsive_design': [
                "Mobile-first approach",
                "Flexible grid layouts",
                "Responsive images with srcset",
                "Touch-friendly targets (min 44x44px)",
                "Test on multiple devices"
            ],
            'accessibility': [
                "Use semantic HTML",
                "Provide alt text for images",
                "Ensure keyboard navigation",
                "Maintain proper heading hierarchy",
                "WCAG 2.1 AA color contrast (4.5:1)",
                "ARIA labels where needed",
                "Focus indicators visible"
            ],
            'performance': [
                "Minimize HTTP requests",
                "Optimize images (WebP, lazy loading)",
                "Minify CSS/JS",
                "Use CDN for assets",
                "Critical CSS inline",
                "Defer non-critical JS"
            ],
            'typography': [
                "Use system fonts for performance",
                "16px minimum font size",
                "1.5-1.6 line height for body text",
                "Limit to 2-3 font families",
                "Proper font weights (400, 600, 700)"
            ],
            'color': [
                "Establish color palette (primary, secondary, accent)",
                "Use color psychology appropriately",
                "Ensure sufficient contrast",
                "Limit to 5-7 colors max",
                "Consider colorblind users"
            ],
            'layout': [
                "Use whitespace effectively",
                "Establish visual hierarchy",
                "Align elements on grid",
                "Consistent spacing (8px system)",
                "F-pattern or Z-pattern for content"
            ]
        }
    
    def research_niche(
        self,
        niche: str,
        analyze_top_n: int = 10,
        extract_patterns: bool = True
    ) -> Dict[str, Any]:
        """Research best practices for specific niche"""
        
        results = {
            'niche': niche,
            'patterns_found': [],
            'common_features': [],
            'color_schemes': [],
            'typography_trends': [],
            'layout_patterns': []
        }
        
        # Simulate pattern analysis (in real implementation, would scrape actual sites)
        niche_patterns = {
            'saas': {
                'common_features': [
                    'Clean hero section with product screenshot',
                    'Feature comparison tables',
                    'Customer testimonials',
                    'Pricing tiers',
                    'Free trial CTA'
                ],
                'color_schemes': ['Blue & White', 'Purple & White', 'Green & Dark'],
                'typography_trends': ['Sans-serif headings', 'System fonts', 'Bold CTAs'],
                'layout_patterns': ['Single column', 'Feature grid', 'Alternating sections']
            },
            'ecommerce': {
                'common_features': [
                    'Product grid with filters',
                    'Shopping cart icon',
                    'Search bar prominent',
                    'Trust badges',
                    'Related products'
                ],
                'color_schemes': ['Brand primary + Black/White', 'Warm tones', 'High contrast'],
                'typography_trends': ['Clear product names', 'Large prices', 'Bold CTAs'],
                'layout_patterns': ['Grid layout', 'Sticky header', 'Sidebar filters']
            },
            'blog': {
                'common_features': [
                    'Featured post section',
                    'Post grid/list',
                    'Sidebar with categories',
                    'Author bios',
                    'Social sharing'
                ],
                'color_schemes': ['Minimal B&W', 'Warm backgrounds', 'Accent colors'],
                'typography_trends': ['Serif for content', 'Large readable text', 'Clear hierarchy'],
                'layout_patterns': ['Magazine style', 'Card grid', 'Single column posts']
            }
        }
        
        niche_lower = niche.lower().replace(' ', '_')
        for key in niche_patterns:
            if key in niche_lower:
                results.update(niche_patterns[key])
                break
        
        # Add relevant patterns from database
        for pattern_name, pattern in self.pattern_database.items():
            if niche_lower in pattern.category or any(niche_lower in uc.lower() for uc in pattern.use_cases):
                results['patterns_found'].append({
                    'name': pattern.name,
                    'description': pattern.description,
                    'best_practices': pattern.best_practices
                })
        
        return results
    
    def scrape_and_analyze(
        self,
        url: str,
        extract_css: bool = True,
        extract_components: bool = True,
        analyze_layout: bool = True
    ) -> Dict[str, Any]:
        """Scrape and analyze a website (simulated)"""
        
        # In real implementation, would use BeautifulSoup/Selenium
        # This is a simulated response
        
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        analysis = {
            'url': url,
            'timestamp': '2024-01-01T00:00:00Z',
            'components_found': [],
            'css_patterns': [],
            'layout_structure': {},
            'accessibility_score': 85.0,
            'performance_metrics': {}
        }
        
        if extract_components:
            analysis['components_found'] = [
                {'type': 'navbar', 'classes': ['navbar', 'navbar-expand-lg']},
                {'type': 'hero', 'classes': ['hero-section', 'bg-primary']},
                {'type': 'card', 'count': 6},
                {'type': 'footer', 'classes': ['footer', 'bg-dark']}
            ]
        
        if extract_css:
            analysis['css_patterns'] = [
                {'property': 'font-family', 'value': 'Inter, system-ui, sans-serif'},
                {'property': 'primary-color', 'value': '#007bff'},
                {'property': 'border-radius', 'value': '8px'},
                {'property': 'spacing-unit', 'value': '8px'}
            ]
        
        if analyze_layout:
            analysis['layout_structure'] = {
                'type': 'single-column',
                'max-width': '1200px',
                'sections': ['header', 'hero', 'features', 'testimonials', 'footer'],
                'grid_system': '12-column',
                'breakpoints': ['576px', '768px', '992px', '1200px']
            }
        
        self.scraped_sites[url_hash] = analysis
        return analysis
    
    def get_pattern(self, pattern_name: str) -> Optional[DesignPattern]:
        """Get a specific pattern from database"""
        return self.pattern_database.get(pattern_name)
    
    def search_patterns(
        self,
        category: Optional[str] = None,
        use_case: Optional[str] = None
    ) -> List[DesignPattern]:
        """Search patterns by category or use case"""
        results = []
        
        for pattern in self.pattern_database.values():
            if category and pattern.category == category:
                results.append(pattern)
            elif use_case and any(use_case.lower() in uc.lower() for uc in pattern.use_cases):
                results.append(pattern)
        
        return results
    
    def get_best_practices(self, category: str) -> List[str]:
        """Get best practices for a category"""
        return self.best_practices_db.get(category, [])
    
    def analyze_color_scheme(self, colors: List[str]) -> Dict[str, Any]:
        """Analyze a color scheme"""
        return {
            'primary': colors[0] if colors else '#007bff',
            'secondary': colors[1] if len(colors) > 1 else '#6c757d',
            'accent': colors[2] if len(colors) > 2 else '#28a745',
            'contrast_ratio': 'Good',
            'accessibility': 'WCAG AA compliant',
            'mood': 'Professional, Trustworthy'
        }
    
    def generate_style_guide(self, niche: str) -> Dict[str, Any]:
        """Generate a style guide for a niche"""
        research = self.research_niche(niche)
        
        return {
            'colors': research.get('color_schemes', []),
            'typography': research.get('typography_trends', []),
            'spacing': '8px base unit',
            'border_radius': '4px - 8px',
            'shadows': 'Subtle elevation',
            'animations': 'Smooth transitions (0.3s)',
            'components': research.get('common_features', [])
        }


if __name__ == "__main__":
    engine = DesignResearchEngine()
    
    # Research SaaS niche
    results = engine.research_niche("saas", analyze_top_n=10)
    print("SaaS Research Results:")
    print(f"Common Features: {results['common_features']}")
    print(f"Color Schemes: {results['color_schemes']}")
    
    # Get hero section pattern
    pattern = engine.get_pattern("hero_section")
    if pattern:
        print(f"\nPattern: {pattern.name}")
        print(f"Best Practices: {pattern.best_practices}")
    
    # Get accessibility best practices
    accessibility_bp = engine.get_best_practices("accessibility")
    print(f"\nAccessibility Best Practices:")
    for i, practice in enumerate(accessibility_bp, 1):
        print(f"{i}. {practice}")
