"""
Prompt Enhancement System for UI Design
Optimizes and expands prompts with best practices and context
"""

from typing import Dict, List, Optional
import json

class PromptEnhancer:
    """Enhances UI design prompts with best practices and context"""
    
    def __init__(self):
        self.best_practices = self._load_best_practices()
        self.accessibility_requirements = self._load_accessibility_requirements()
        self.framework_specs = self._load_framework_specs()
    
    def enhance_prompt(self, prompt: str, 
                      inject_best_practices: bool = True,
                      add_accessibility: bool = True,
                      specify_framework: Optional[str] = None,
                      add_context: bool = True,
                      target_audience: Optional[str] = None,
                      niche: Optional[str] = None) -> str:
        """
        Enhance a UI design prompt
        
        Args:
            prompt: Original prompt
            inject_best_practices: Add best practices
            add_accessibility: Add accessibility requirements
            specify_framework: CSS framework to use
            add_context: Add contextual information
            target_audience: Target user audience
            niche: Design niche (e-commerce, SaaS, etc.)
            
        Returns:
            Enhanced prompt
        """
        enhanced = prompt
        
        # Add best practices
        if inject_best_practices:
            enhanced = self._inject_best_practices(enhanced, niche)
        
        # Add accessibility
        if add_accessibility:
            enhanced = self._add_accessibility(enhanced)
        
        # Add framework specification
        if specify_framework:
            enhanced = self._add_framework_spec(enhanced, specify_framework)
        
        # Add contextual information
        if add_context:
            enhanced = self._add_context(enhanced, target_audience, niche)
        
        return enhanced
    
    def _inject_best_practices(self, prompt: str, niche: Optional[str]) -> str:
        """Inject best practices into prompt"""
        practices = []
        
        # General best practices
        practices.extend([
            "Follow modern web design principles",
            "Ensure responsive design (mobile-first approach)",
            "Use consistent spacing and typography",
            "Implement proper visual hierarchy",
            "Optimize for performance (minimize HTTP requests)"
        ])
        
        # Niche-specific practices
        if niche:
            niche_practices = self.best_practices.get(niche, [])
            practices.extend(niche_practices)
        
        practices_text = ". ".join(practices)
        return f"{prompt}. {practices_text}"
    
    def _add_accessibility(self, prompt: str) -> str:
        """Add accessibility requirements"""
        accessibility_text = (
            "Ensure WCAG 2.1 AA compliance with proper ARIA labels, "
            "keyboard navigation support, sufficient color contrast (4.5:1 for text), "
            "screen reader compatibility, and focus indicators"
        )
        return f"{prompt}. {accessibility_text}"
    
    def _add_framework_spec(self, prompt: str, framework: str) -> str:
        """Add framework-specific requirements"""
        framework_specs = {
            'bootstrap': "Use Bootstrap 5 with utility classes, grid system (container, row, col-*), and components",
            'tailwind': "Use Tailwind CSS with utility-first classes, responsive modifiers (sm:, md:, lg:), and custom design system",
            'material-ui': "Follow Material Design principles with proper elevation, ripple effects, and consistent spacing",
            'bulma': "Use Bulma CSS framework with columns, elements, and modifiers",
            'foundation': "Use Foundation framework with XY grid, flex utilities, and motion UI"
        }
        
        spec = framework_specs.get(framework.lower(), f"Use {framework} framework")
        return f"{prompt}. {spec}"
    
    def _add_context(self, prompt: str, target_audience: Optional[str], 
                    niche: Optional[str]) -> str:
        """Add contextual information"""
        context_parts = []
        
        if target_audience:
            audience_context = {
                'enterprise': "Design for enterprise users with professional aesthetics, data-dense layouts, and advanced features",
                'consumer': "Design for general consumers with simple, intuitive interfaces and clear call-to-actions",
                'developer': "Design for developers with code-friendly interfaces, documentation, and technical details",
                'elderly': "Design for elderly users with larger text, simple navigation, and high contrast",
                'mobile-first': "Design primarily for mobile users with touch-friendly elements and simplified layouts"
            }
            context_parts.append(audience_context.get(target_audience, f"Target audience: {target_audience}"))
        
        if niche:
            niche_context = {
                'e-commerce': "Include product imagery, clear pricing, add-to-cart functionality, and trust signals",
                'saas': "Include pricing tiers, feature comparisons, demo CTAs, and social proof",
                'portfolio': "Showcase work samples, about section, contact form, and professional branding",
                'blog': "Include article cards, categories, search, and reading experience optimization",
                'landing': "Focus on single conversion goal with hero section, benefits, and prominent CTA"
            }
            context_parts.append(niche_context.get(niche, f"Niche: {niche}"))
        
        if context_parts:
            context_text = ". ".join(context_parts)
            return f"{prompt}. {context_text}"
        
        return prompt
    
    def _load_best_practices(self) -> Dict[str, List[str]]:
        """Load best practices database"""
        return {
            'e-commerce': [
                "Include high-quality product images with zoom functionality",
                "Show clear pricing and shipping information",
                "Display trust badges and security indicators",
                "Implement intuitive checkout process (progress indicator)",
                "Add product reviews and ratings"
            ],
            'saas': [
                "Clear value proposition above the fold",
                "Pricing table with feature comparisons",
                "Social proof (testimonials, logos, case studies)",
                "Free trial or demo CTA",
                "Feature highlights with icons"
            ],
            'dashboard': [
                "Data visualization with charts and graphs",
                "Quick stats/KPIs at top",
                "Filterable and sortable data tables",
                "Responsive sidebar navigation",
                "Search and notification features"
            ],
            'landing': [
                "Strong hero section with benefit-focused headline",
                "Single clear call-to-action",
                "Social proof section",
                "Feature/benefit highlights",
                "Trust signals and testimonials"
            ],
            'blog': [
                "Clean, readable typography",
                "Featured image for articles",
                "Category and tag organization",
                "Related articles section",
                "Social sharing buttons"
            ]
        }
    
    def _load_accessibility_requirements(self) -> Dict:
        """Load accessibility requirements"""
        return {
            'WCAG_AA': {
                'color_contrast': '4.5:1 for normal text, 3:1 for large text',
                'keyboard': 'All functionality available via keyboard',
                'aria': 'Proper ARIA labels for interactive elements',
                'focus': 'Visible focus indicators',
                'alt_text': 'Alternative text for images'
            },
            'WCAG_AAA': {
                'color_contrast': '7:1 for normal text, 4.5:1 for large text',
                'text_spacing': 'Line height 1.5x, paragraph spacing 2x',
                'resize': 'Text can be resized up to 200%',
                'reflow': 'Content reflows without horizontal scroll at 320px'
            }
        }
    
    def _load_framework_specs(self) -> Dict:
        """Load framework specifications"""
        return {
            'bootstrap': {
                'grid': '12-column responsive grid',
                'breakpoints': ['xs (<576px)', 'sm (≥576px)', 'md (≥768px)', 'lg (≥992px)', 'xl (≥1200px)', 'xxl (≥1400px)'],
                'components': 'Pre-built components (buttons, cards, modals, navbar, forms)'
            },
            'tailwind': {
                'approach': 'Utility-first CSS',
                'responsive': 'Mobile-first breakpoints (sm, md, lg, xl, 2xl)',
                'customization': 'Highly customizable via tailwind.config.js'
            },
            'material-ui': {
                'principles': 'Material Design by Google',
                'features': 'Elevation, motion, grid layout, theming',
                'components': 'Rich component library with variants'
            }
        }
    
    def expand_with_examples(self, prompt: str, include_wireframe: bool = False) -> str:
        """Expand prompt with examples and wireframe descriptions"""
        expansion = prompt
        
        # Detect component types
        if 'button' in prompt.lower():
            expansion += ". Include primary, secondary, and tertiary button variants with hover/active states"
        
        if 'form' in prompt.lower():
            expansion += ". Include input validation, error states, success messages, and loading indicators"
        
        if 'navigation' in prompt.lower() or 'navbar' in prompt.lower():
            expansion += ". Include logo, main navigation links, mobile hamburger menu, and search functionality"
        
        if 'card' in prompt.lower():
            expansion += ". Include image, title, description, and action button with hover effects"
        
        if include_wireframe:
            expansion += ". Provide clear visual hierarchy and layout structure description"
        
        return expansion
    
    def optimize_for_quality(self, prompt: str) -> str:
        """Optimize prompt for quality output"""
        quality_additions = [
            "Use modern design trends",
            "Ensure pixel-perfect alignment",
            "Add subtle animations and transitions",
            "Optimize loading performance",
            "Include dark mode support if applicable",
            "Follow brand consistency guidelines",
            "Test across different screen sizes"
        ]
        
        return f"{prompt}. {'. '.join(quality_additions)}"
    
    def inject_seo_requirements(self, prompt: str) -> str:
        """Inject SEO-related requirements"""
        seo_text = (
            "Include semantic HTML5 elements (header, nav, main, article, footer), "
            "proper heading hierarchy (h1-h6), descriptive alt text for images, "
            "meta descriptions, and structured data where applicable"
        )
        return f"{prompt}. {seo_text}"
