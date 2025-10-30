"""
Design Orchestrator
End-to-end UI generation pipeline with multi-agent collaboration
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time

# Import our UI system components
try:
    from ui_design_expert import UIDesignExpert, UIComponent
    from design_research_engine import DesignResearchEngine
    from llm_ui_generator import LLMUIGenerator, LLMUIResult
except ImportError:
    # For standalone testing
    pass


@dataclass
class DesignResult:
    """Complete design result"""
    html: str
    css: str
    js: str
    quality_score: float
    accessibility_score: float
    performance_score: float
    improvements: List[str]
    research_data: Dict[str, Any]
    reasoning: str
    generation_time: float


class DesignOrchestrator:
    """Orchestrate complete UI generation pipeline"""
    
    def __init__(self):
        self.ui_expert = UIDesignExpert()
        self.research_engine = DesignResearchEngine()
        self.llm_generator = LLMUIGenerator()
        
        self.pipeline_stages = [
            'research',
            'generation',
            'enhancement',
            'quality_assurance',
            'optimization'
        ]
    
    def create_complete_ui(
        self,
        description: str,
        niche: Optional[str] = None,
        framework: str = 'bootstrap',
        research_enabled: bool = True,
        llm_reasoning: bool = True,
        generate_variants: int = 1,
        quality_assurance: bool = True,
        usability_testing: bool = False
    ) -> DesignResult:
        """Create complete UI through full pipeline"""
        
        start_time = time.time()
        
        # Stage 1: Research
        research_data = {}
        if research_enabled and niche:
            print(f"[Stage 1/5] Researching {niche} best practices...")
            research_data = self.research_engine.research_niche(niche, analyze_top_n=10)
        
        # Stage 2: Generation
        print(f"[Stage 2/5] Generating UI...")
        if llm_reasoning:
            # Use LLM for intelligent generation
            llm_result = self.llm_generator.generate_with_reasoning(
                prompt=description,
                model='gpt-4',
                enhance_prompt=True,
                research_enabled=research_enabled,
                framework=framework
            )
            html = llm_result.html
            css = llm_result.css
            js = llm_result.js
            reasoning = llm_result.reasoning
            initial_quality = llm_result.quality_score
        else:
            # Use expert system
            html = self.ui_expert.generate_webpage(
                type="landing_page",
                framework=framework,
                accessibility=True,
                responsive=True
            )
            css = ""
            js = ""
            reasoning = "Generated using expert system with best practices"
            initial_quality = 85.0
        
        # Stage 3: Enhancement
        print(f"[Stage 3/5] Enhancing design...")
        if llm_reasoning and quality_assurance:
            enhanced_result = self.llm_generator.critique_and_improve(
                html_code=html,
                css_code=css,
                js_code=js,
                focus="usability",
                iterations=1
            )
            html = enhanced_result.html
            css = enhanced_result.css
            js = enhanced_result.js
        
        # Stage 4: Quality Assurance
        print(f"[Stage 4/5] Running quality assurance...")
        quality_score = self._calculate_quality_score(html, css, js)
        accessibility_score = self.ui_expert.get_accessibility_score(html)
        performance_score = self._calculate_performance_score(html, css, js)
        improvements = self._generate_improvements(html, css, js, quality_score)
        
        # Stage 5: Optimization
        print(f"[Stage 5/5] Optimizing code...")
        optimized = self.ui_expert.optimize_performance(html, css, js)
        html = optimized['html']
        css = optimized['css']
        js = optimized['js']
        
        generation_time = time.time() - start_time
        
        print(f"✓ Complete! Generated in {generation_time:.2f}s")
        print(f"  Quality: {quality_score:.1f}/100")
        print(f"  Accessibility: {accessibility_score:.1f}/100")
        print(f"  Performance: {performance_score:.1f}/100")
        
        return DesignResult(
            html=html,
            css=css,
            js=js,
            quality_score=quality_score,
            accessibility_score=accessibility_score,
            performance_score=performance_score,
            improvements=improvements,
            research_data=research_data,
            reasoning=reasoning,
            generation_time=generation_time
        )
    
    def generate_design_system(
        self,
        brand_name: str,
        niche: str,
        primary_color: str,
        secondary_color: str
    ) -> Dict[str, Any]:
        """Generate complete design system"""
        
        print(f"Generating design system for {brand_name}...")
        
        # Research niche
        research = self.research_engine.research_niche(niche)
        
        # Generate style guide
        style_guide = self.research_engine.generate_style_guide(niche)
        
        # Generate components
        components = {}
        for comp_type in ['button', 'card', 'navbar', 'footer', 'form']:
            print(f"  Generating {comp_type}...")
            comp = self.ui_expert.generate_component(
                comp_type,
                framework='bootstrap',
                accessibility=True
            )
            components[comp_type] = comp
        
        design_system = {
            'brand': brand_name,
            'niche': niche,
            'colors': {
                'primary': primary_color,
                'secondary': secondary_color,
                'accent': '#28a745',
                'background': '#ffffff',
                'text': '#333333'
            },
            'typography': {
                'headings': 'Inter, sans-serif',
                'body': 'system-ui, sans-serif',
                'sizes': {
                    'h1': '2.5rem',
                    'h2': '2rem',
                    'h3': '1.5rem',
                    'body': '1rem'
                }
            },
            'spacing': {
                'unit': '8px',
                'scale': ['4px', '8px', '16px', '24px', '32px', '48px', '64px']
            },
            'components': components,
            'style_guide': style_guide,
            'research': research
        }
        
        print(f"✓ Design system complete!")
        return design_system
    
    def multi_agent_design(
        self,
        description: str,
        agent_count: int = 3,
        framework: str = 'bootstrap'
    ) -> List[DesignResult]:
        """Generate multiple designs using multi-agent approach"""
        
        print(f"Generating {agent_count} design variants...")
        
        results = []
        for i in range(agent_count):
            print(f"  Agent {i+1}/{agent_count} designing...")
            result = self.create_complete_ui(
                description=f"{description} (Variant {i+1})",
                framework=framework,
                research_enabled=True,
                llm_reasoning=True,
                quality_assurance=True
            )
            results.append(result)
        
        # Sort by quality score
        results.sort(key=lambda x: x.quality_score, reverse=True)
        
        print(f"✓ {agent_count} variants generated!")
        print(f"  Best quality: {results[0].quality_score:.1f}/100")
        
        return results
    
    def _calculate_quality_score(self, html: str, css: str, js: str) -> float:
        """Calculate overall quality score"""
        
        score = 70.0
        
        # HTML quality
        if '<html' in html and '</html>' in html:
            score += 5
        if 'DOCTYPE' in html:
            score += 3
        
        # Semantic HTML
        semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        if any(tag in html for tag in semantic_tags):
            score += 7
        
        # Accessibility
        if 'aria-' in html:
            score += 5
        if 'alt=' in html:
            score += 3
        
        # Responsive design
        if '@media' in css or 'responsive' in css.lower():
            score += 7
        
        return min(100.0, score)
    
    def _calculate_performance_score(self, html: str, css: str, js: str) -> float:
        """Calculate performance score"""
        
        score = 80.0
        
        # Check file sizes (estimated)
        html_size = len(html)
        css_size = len(css)
        js_size = len(js)
        
        total_size = html_size + css_size + js_size
        
        # Penalize large files
        if total_size > 100000:
            score -= 10
        elif total_size > 50000:
            score -= 5
        
        # Reward optimizations
        if 'async' in html or 'defer' in html:
            score += 5
        if 'lazy' in html.lower():
            score += 3
        
        return max(0, min(100.0, score))
    
    def _generate_improvements(
        self,
        html: str,
        css: str,
        js: str,
        quality_score: float
    ) -> List[str]:
        """Generate list of improvements"""
        
        improvements = []
        
        if quality_score < 90:
            if 'aria-' not in html:
                improvements.append("Add ARIA labels for better accessibility")
            if '@media' not in css:
                improvements.append("Add responsive breakpoints")
            if 'transition' not in css:
                improvements.append("Add smooth transitions for better UX")
        
        if '<img' in html and 'loading=' not in html:
            improvements.append("Add lazy loading to images")
        
        if '<form' in html and 'autocomplete' not in html:
            improvements.append("Add autocomplete attributes to forms")
        
        return improvements


if __name__ == "__main__":
    orchestrator = DesignOrchestrator()
    
    # Create complete UI
    result = orchestrator.create_complete_ui(
        description="Modern SaaS dashboard with metrics cards",
        niche="saas",
        framework="bootstrap",
        research_enabled=True,
        llm_reasoning=True,
        quality_assurance=True
    )
    
    print(f"\n=== Design Result ===")
    print(f"Quality: {result.quality_score:.1f}")
    print(f"Accessibility: {result.accessibility_score:.1f}")
    print(f"Performance: {result.performance_score:.1f}")
    print(f"Time: {result.generation_time:.2f}s")
    print(f"\nImprovements:")
    for imp in result.improvements:
        print(f"  - {imp}")
    
    # Generate design system
    print(f"\n=== Generating Design System ===")
    design_system = orchestrator.generate_design_system(
        brand_name="TechCorp",
        niche="saas",
        primary_color="#007bff",
        secondary_color="#6c757d"
    )
    
    print(f"Components: {list(design_system['components'].keys())}")
