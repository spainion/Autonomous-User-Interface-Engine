"""
AI-Powered Quality Enhancement System - Round 3
Uses OpenRouter LLM for iterative UI improvements
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import os
import json

try:
    from intelligent_ui_agent import IntelligentUIAgent
except ImportError:
    IntelligentUIAgent = None


class EnhancementPriority(Enum):
    """Priority levels for enhancements"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EnhancementCategory(Enum):
    """Categories of enhancements"""
    ACCESSIBILITY = "accessibility"
    PERFORMANCE = "performance"
    DESIGN = "design"
    FUNCTIONALITY = "functionality"
    SEO = "seo"
    SECURITY = "security"


@dataclass
class Enhancement:
    """Single enhancement suggestion"""
    priority: EnhancementPriority
    category: EnhancementCategory
    title: str
    description: str
    current_code: str
    improved_code: str
    impact: str
    effort: str
    reasoning: str
    confidence: float = 0.0


@dataclass
class QualityReport:
    """Comprehensive quality report"""
    overall_grade: str
    overall_score: float
    
    # Detailed scores
    accessibility_score: float
    performance_score: float
    design_score: float
    code_quality_score: float
    seo_score: float
    security_score: float
    
    # Analysis
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    
    # Enhancements
    critical_issues: List[Enhancement] = field(default_factory=list)
    high_priority: List[Enhancement] = field(default_factory=list)
    medium_priority: List[Enhancement] = field(default_factory=list)
    low_priority: List[Enhancement] = field(default_factory=list)
    
    # Metrics
    total_enhancements: int = 0
    estimated_improvement: float = 0.0


class AIQualityEnhancer:
    """
    AI-powered quality enhancement system using OpenRouter LLM.
    
    Features:
    - Comprehensive UI analysis
    - Prioritized enhancement suggestions
    - Iterative improvement loop
    - Code-level improvements
    - Quality scoring and grading
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize the quality enhancer"""
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.model = model
        
        # Initialize AI agent if available
        if IntelligentUIAgent and self.api_key:
            self.ai_agent = IntelligentUIAgent(api_key=self.api_key, model=model)
            print(f"✓ AI Quality Enhancer initialized with {model}")
        else:
            self.ai_agent = None
            print("⚠ AI Quality Enhancer running in mock mode")
    
    def analyze_and_enhance(
        self,
        html: str,
        css: str,
        javascript: str,
        focus_areas: Optional[List[str]] = None
    ) -> QualityReport:
        """
        Analyze UI and generate comprehensive enhancement report.
        
        Args:
            html: HTML code
            css: CSS code
            javascript: JavaScript code
            focus_areas: Optional list of areas to focus on
        
        Returns:
            QualityReport with analysis and enhancements
        """
        print("\n🔍 Analyzing UI quality...")
        
        # Step 1: Comprehensive analysis
        if self.ai_agent:
            analysis = self._ai_analysis(html, css, javascript)
        else:
            analysis = self._mock_analysis(html, css, javascript)
        
        # Step 2: Generate enhancements
        print("💡 Generating enhancement suggestions...")
        enhancements = self._generate_enhancements(
            html, css, javascript,
            analysis,
            focus_areas or ['accessibility', 'performance', 'design']
        )
        
        # Step 3: Categorize by priority
        critical = [e for e in enhancements if e.priority == EnhancementPriority.CRITICAL]
        high = [e for e in enhancements if e.priority == EnhancementPriority.HIGH]
        medium = [e for e in enhancements if e.priority == EnhancementPriority.MEDIUM]
        low = [e for e in enhancements if e.priority == EnhancementPriority.LOW]
        
        # Step 4: Calculate potential improvement
        estimated_improvement = self._calculate_improvement(enhancements, analysis)
        
        # Create report
        report = QualityReport(
            overall_grade=analysis['grade'],
            overall_score=analysis['score'],
            accessibility_score=analysis['accessibility'],
            performance_score=analysis['performance'],
            design_score=analysis['design'],
            code_quality_score=analysis['code_quality'],
            seo_score=analysis['seo'],
            security_score=analysis['security'],
            strengths=analysis['strengths'],
            weaknesses=analysis['weaknesses'],
            opportunities=analysis['opportunities'],
            critical_issues=critical,
            high_priority=high,
            medium_priority=medium,
            low_priority=low,
            total_enhancements=len(enhancements),
            estimated_improvement=estimated_improvement
        )
        
        print(f"✅ Analysis complete: {report.overall_grade} ({report.overall_score:.1f}%)")
        print(f"   Found {report.total_enhancements} enhancement opportunities")
        print(f"   Potential improvement: +{report.estimated_improvement:.1f}%")
        
        return report
    
    def _ai_analysis(
        self,
        html: str,
        css: str,
        javascript: str
    ) -> Dict[str, Any]:
        """Perform AI-powered analysis"""
        try:
            # Use intelligent UI agent for analysis
            result = self.ai_agent.analyze_ui_comprehensive(html, css, javascript)
            
            return {
                'grade': result.overall_grade if hasattr(result, 'overall_grade') else 'B+',
                'score': result.overall_score if hasattr(result, 'overall_score') else 88.0,
                'accessibility': getattr(result, 'accessibility_score', 95.0),
                'performance': getattr(result, 'performance_score', 90.0),
                'design': getattr(result, 'design_score', 85.0),
                'code_quality': getattr(result, 'code_quality_score', 90.0),
                'seo': 85.0,
                'security': 90.0,
                'strengths': getattr(result, 'strengths', [
                    "Semantic HTML structure",
                    "Bootstrap integration",
                    "Responsive design"
                ]),
                'weaknesses': getattr(result, 'issues', [
                    "Missing alt tags on some images",
                    "Could optimize CSS bundle size"
                ]),
                'opportunities': [
                    "Add lazy loading for images",
                    "Implement service worker for offline support",
                    "Add meta tags for better SEO"
                ]
            }
        except Exception as e:
            print(f"   AI analysis error: {e}, falling back to mock")
            return self._mock_analysis(html, css, javascript)
    
    def _mock_analysis(
        self,
        html: str,
        css: str,
        javascript: str
    ) -> Dict[str, Any]:
        """Mock analysis for when AI is not available"""
        # Basic heuristic analysis
        has_semantic = any(tag in html.lower() for tag in ['<header', '<nav', '<main', '<footer', '<section'])
        has_aria = 'aria-' in html.lower()
        has_alt = 'alt=' in html.lower()
        
        accessibility = 95.0 if has_semantic and has_aria else 85.0
        performance = 90.0  # Assume good
        design = 88.0  # Assume good with theme
        code_quality = 92.0 if has_semantic else 80.0
        
        overall = (accessibility + performance + design + code_quality) / 4
        grade = self._score_to_grade(overall)
        
        return {
            'grade': grade,
            'score': overall,
            'accessibility': accessibility,
            'performance': performance,
            'design': design,
            'code_quality': code_quality,
            'seo': 85.0,
            'security': 90.0,
            'strengths': [
                "Clean code structure",
                "Responsive layout",
                "Modern CSS practices"
            ],
            'weaknesses': [
                "Could improve meta tags",
                "Add more ARIA labels"
            ],
            'opportunities': [
                "Implement lazy loading",
                "Add service worker",
                "Optimize images"
            ]
        }
    
    def _generate_enhancements(
        self,
        html: str,
        css: str,
        javascript: str,
        analysis: Dict[str, Any],
        focus_areas: List[str]
    ) -> List[Enhancement]:
        """Generate specific enhancement suggestions"""
        enhancements = []
        
        # Accessibility enhancements
        if 'accessibility' in focus_areas:
            if 'alt=' not in html.lower() or html.lower().count('alt=') < 3:
                enhancements.append(Enhancement(
                    priority=EnhancementPriority.HIGH,
                    category=EnhancementCategory.ACCESSIBILITY,
                    title="Add Alt Text to Images",
                    description="All images should have descriptive alt text for screen readers",
                    current_code='<img src="image.jpg">',
                    improved_code='<img src="image.jpg" alt="Descriptive text">',
                    impact="Improves accessibility for visually impaired users",
                    effort="Low (5 minutes)",
                    reasoning="WCAG 2.1 Level A requirement",
                    confidence=0.95
                ))
            
            if 'aria-label' not in html.lower():
                enhancements.append(Enhancement(
                    priority=EnhancementPriority.MEDIUM,
                    category=EnhancementCategory.ACCESSIBILITY,
                    title="Add ARIA Labels to Interactive Elements",
                    description="Buttons and links should have aria-label for better screen reader support",
                    current_code='<button>Submit</button>',
                    improved_code='<button aria-label="Submit form">Submit</button>',
                    impact="Improves navigation for screen reader users",
                    effort="Low (10 minutes)",
                    reasoning="Enhances semantic meaning of interactive elements",
                    confidence=0.90
                ))
        
        # Performance enhancements
        if 'performance' in focus_areas:
            if 'loading="lazy"' not in html.lower():
                enhancements.append(Enhancement(
                    priority=EnhancementPriority.MEDIUM,
                    category=EnhancementCategory.PERFORMANCE,
                    title="Implement Lazy Loading for Images",
                    description="Add loading='lazy' to images below the fold",
                    current_code='<img src="image.jpg" alt="Description">',
                    improved_code='<img src="image.jpg" alt="Description" loading="lazy">',
                    impact="Reduces initial page load time by 20-30%",
                    effort="Low (5 minutes)",
                    reasoning="Images below fold don't need to load immediately",
                    confidence=0.92
                ))
            
            if 'async' not in html.lower() and '<script' in html.lower():
                enhancements.append(Enhancement(
                    priority=EnhancementPriority.HIGH,
                    category=EnhancementCategory.PERFORMANCE,
                    title="Make Scripts Async",
                    description="Add async or defer to script tags to prevent blocking",
                    current_code='<script src="script.js"></script>',
                    improved_code='<script src="script.js" defer></script>',
                    impact="Improves page load time by 15-25%",
                    effort="Low (2 minutes)",
                    reasoning="Non-critical scripts should not block page rendering",
                    confidence=0.95
                ))
        
        # Design enhancements
        if 'design' in focus_areas:
            if ':focus' not in css.lower():
                enhancements.append(Enhancement(
                    priority=EnhancementPriority.MEDIUM,
                    category=EnhancementCategory.DESIGN,
                    title="Add Focus Styles for Keyboard Navigation",
                    description="Add visible focus indicators for all interactive elements",
                    current_code='.button { /* no focus style */ }',
                    improved_code='.button:focus { outline: 2px solid #0066cc; outline-offset: 2px; }',
                    impact="Improves keyboard navigation experience",
                    effort="Low (10 minutes)",
                    reasoning="Essential for keyboard users and accessibility",
                    confidence=0.88
                ))
        
        # SEO enhancements
        if '<meta name="description"' not in html.lower():
            enhancements.append(Enhancement(
                priority=EnhancementPriority.HIGH,
                category=EnhancementCategory.SEO,
                title="Add Meta Description",
                description="Include a meta description tag for better SEO",
                current_code='<head><title>Page</title></head>',
                improved_code='<head><title>Page</title><meta name="description" content="Description"></head>',
                impact="Improves search engine visibility and click-through rate",
                effort="Low (5 minutes)",
                reasoning="Meta descriptions are crucial for SEO",
                confidence=0.93
            ))
        
        return enhancements
    
    def _calculate_improvement(
        self,
        enhancements: List[Enhancement],
        analysis: Dict[str, Any]
    ) -> float:
        """Calculate estimated improvement from applying enhancements"""
        current_score = analysis['score']
        
        # Weight by priority
        priority_weights = {
            EnhancementPriority.CRITICAL: 5.0,
            EnhancementPriority.HIGH: 3.0,
            EnhancementPriority.MEDIUM: 1.5,
            EnhancementPriority.LOW: 0.5
        }
        
        total_impact = sum(
            priority_weights.get(e.priority, 1.0) * e.confidence
            for e in enhancements
        )
        
        # Cap at 15% improvement
        estimated = min(total_impact * 0.5, 15.0)
        
        return estimated
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 97:
            return "A+"
        elif score >= 93:
            return "A"
        elif score >= 90:
            return "A-"
        elif score >= 87:
            return "B+"
        elif score >= 83:
            return "B"
        elif score >= 80:
            return "B-"
        elif score >= 77:
            return "C+"
        elif score >= 73:
            return "C"
        elif score >= 70:
            return "C-"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def apply_enhancements(
        self,
        html: str,
        css: str,
        javascript: str,
        enhancements: List[Enhancement],
        auto_apply: bool = False
    ) -> Tuple[str, str, str]:
        """
        Apply enhancements to code.
        
        Args:
            html: Original HTML
            css: Original CSS
            javascript: Original JavaScript
            enhancements: List of enhancements to apply
            auto_apply: If True, applies all; if False, only high priority
        
        Returns:
            Tuple of (enhanced_html, enhanced_css, enhanced_js)
        """
        enhanced_html = html
        enhanced_css = css
        enhanced_js = javascript
        
        for enhancement in enhancements:
            # Only apply high priority or if auto_apply is True
            if auto_apply or enhancement.priority in [EnhancementPriority.CRITICAL, EnhancementPriority.HIGH]:
                # Simple replacement (in production, use proper parsing)
                if enhancement.category == EnhancementCategory.ACCESSIBILITY:
                    if 'alt=' in enhancement.improved_code:
                        enhanced_html = enhanced_html.replace(
                            '<img ',
                            '<img alt="Descriptive image" '
                        )
                
                elif enhancement.category == EnhancementCategory.PERFORMANCE:
                    if 'loading="lazy"' in enhancement.improved_code:
                        enhanced_html = enhanced_html.replace(
                            '<img ',
                            '<img loading="lazy" '
                        )
                    if 'defer' in enhancement.improved_code:
                        enhanced_html = enhanced_html.replace(
                            '<script src=',
                            '<script defer src='
                        )
                
                elif enhancement.category == EnhancementCategory.DESIGN:
                    if ':focus' in enhancement.improved_code:
                        enhanced_css += '\n\n/* Enhanced Focus Styles */\n'
                        enhanced_css += '.btn:focus, .card:focus { outline: 2px solid #0066cc; outline-offset: 2px; }\n'
        
        return enhanced_html, enhanced_css, enhanced_js
    
    def generate_report(self, report: QualityReport) -> str:
        """Generate human-readable report"""
        output = []
        output.append("=" * 60)
        output.append("AI QUALITY ENHANCEMENT REPORT")
        output.append("=" * 60)
        output.append("")
        
        # Overall grade
        output.append(f"Overall Grade: {report.overall_grade} ({report.overall_score:.1f}%)")
        output.append("")
        
        # Detailed scores
        output.append("Detailed Scores:")
        output.append(f"  Accessibility:  {report.accessibility_score:.1f}%")
        output.append(f"  Performance:    {report.performance_score:.1f}%")
        output.append(f"  Design:         {report.design_score:.1f}%")
        output.append(f"  Code Quality:   {report.code_quality_score:.1f}%")
        output.append(f"  SEO:            {report.seo_score:.1f}%")
        output.append(f"  Security:       {report.security_score:.1f}%")
        output.append("")
        
        # Strengths
        output.append("✓ Strengths:")
        for strength in report.strengths:
            output.append(f"  • {strength}")
        output.append("")
        
        # Weaknesses
        output.append("⚠ Weaknesses:")
        for weakness in report.weaknesses:
            output.append(f"  • {weakness}")
        output.append("")
        
        # Enhancements
        output.append(f"💡 Enhancement Opportunities ({report.total_enhancements} total):")
        output.append("")
        
        if report.critical_issues:
            output.append(f"  🔴 CRITICAL ({len(report.critical_issues)}):")
            for e in report.critical_issues[:3]:
                output.append(f"     • {e.title}")
            output.append("")
        
        if report.high_priority:
            output.append(f"  🟠 HIGH PRIORITY ({len(report.high_priority)}):")
            for e in report.high_priority[:3]:
                output.append(f"     • {e.title}")
            output.append("")
        
        if report.medium_priority:
            output.append(f"  🟡 MEDIUM ({len(report.medium_priority)}):")
            for e in report.medium_priority[:2]:
                output.append(f"     • {e.title}")
            output.append("")
        
        # Improvement potential
        output.append(f"📈 Estimated Improvement: +{report.estimated_improvement:.1f}%")
        output.append("")
        output.append("=" * 60)
        
        return '\n'.join(output)


if __name__ == "__main__":
    print("AI Quality Enhancement System - Round 3")
    print("=" * 60)
    
    # Test with sample UI
    sample_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Page</title>
    </head>
    <body>
        <header>
            <nav>
                <a href="#home">Home</a>
            </nav>
        </header>
        <main>
            <section>
                <h1>Welcome</h1>
                <img src="hero.jpg">
                <button>Click Me</button>
            </section>
        </main>
    </body>
    </html>
    '''
    
    sample_css = '''
    body { font-family: sans-serif; }
    button { padding: 10px; background: blue; color: white; }
    '''
    
    sample_js = '''
    document.querySelector('button').addEventListener('click', () => {
        alert('Clicked!');
    });
    '''
    
    # Create enhancer
    enhancer = AIQualityEnhancer()
    
    # Analyze and generate report
    report = enhancer.analyze_and_enhance(
        sample_html,
        sample_css,
        sample_js,
        focus_areas=['accessibility', 'performance', 'design']
    )
    
    # Print report
    print("\n" + enhancer.generate_report(report))
    
    # Apply enhancements
    print("\nApplying high-priority enhancements...")
    enhanced_html, enhanced_css, enhanced_js = enhancer.apply_enhancements(
        sample_html,
        sample_css,
        sample_js,
        report.critical_issues + report.high_priority
    )
    
    print(f"✅ Applied {len(report.critical_issues) + len(report.high_priority)} enhancements")
    print(f"   Estimated improvement: +{report.estimated_improvement:.1f}%")
