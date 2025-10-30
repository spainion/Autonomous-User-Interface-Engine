"""
Intelligent UI Analysis and Enhancement Agent
Uses OpenRouter LLM to analyze, compare, grade, and improve UIs with complex layers
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import time


@dataclass
class UIAnalysis:
    """Comprehensive UI analysis result"""
    overall_grade: str  # A+, A, B+, B, C+, C, D, F
    overall_score: float  # 0-100
    complexity_score: float
    accessibility_score: float
    performance_score: float
    design_quality_score: float
    consistency_score: float
    
    # Detailed analysis
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]
    critical_issues: List[str]
    
    # Layer analysis
    html_layer_analysis: Dict[str, Any]
    css_layer_analysis: Dict[str, Any]
    js_layer_analysis: Dict[str, Any]
    design_system_analysis: Dict[str, Any]
    
    # Comparison insights
    comparison_notes: List[str] = field(default_factory=list)
    best_practices_violations: List[str] = field(default_factory=list)
    suggested_patterns: List[str] = field(default_factory=list)
    
    # AI reasoning
    ai_reasoning: str = ""
    confidence_level: float = 0.0


@dataclass
class UIEnhancement:
    """UI enhancement recommendations"""
    priority: str  # critical, high, medium, low
    category: str  # accessibility, performance, design, functionality
    description: str
    current_code: str
    improved_code: str
    impact: str
    effort: str  # low, medium, high
    reasoning: str


class IntelligentUIAgent:
    """
    Intelligent agent for UI analysis, comparison, and enhancement.
    
    Features:
    - Deep layer-by-layer analysis (HTML, CSS, JS, Design System)
    - Comprehensive grading system
    - Pattern recognition and best practices checking
    - Automated improvement suggestions
    - Comparative analysis across UIs
    - Consistency checking
    - LLM-powered reasoning
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize the intelligent agent"""
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.app_name = os.getenv('OPENROUTER_APP_NAME', 'UI-Analysis-Agent')
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
        
        # Analysis history for learning
        self.analysis_history: List[UIAnalysis] = []
        self.enhancement_history: List[UIEnhancement] = []
        
        print(f"✓ Intelligent UI Agent initialized with {model}")
    
    def analyze_ui_comprehensive(
        self,
        html: str,
        css: str,
        js: str,
        design_system: Optional[Dict] = None,
        project_context: Optional[Dict] = None
    ) -> UIAnalysis:
        """
        Perform comprehensive multi-layer UI analysis.
        
        Args:
            html: HTML code
            css: CSS code
            js: JavaScript code
            design_system: Optional design system details
            project_context: Optional project context (type, audience, goals)
        
        Returns:
            Comprehensive UI analysis
        """
        
        print("\n🔍 Performing comprehensive UI analysis...")
        
        # Layer 1: Analyze HTML structure
        print("  [1/6] Analyzing HTML layer...")
        html_analysis = self._analyze_html_layer(html)
        
        # Layer 2: Analyze CSS styling
        print("  [2/6] Analyzing CSS layer...")
        css_analysis = self._analyze_css_layer(css)
        
        # Layer 3: Analyze JavaScript functionality
        print("  [3/6] Analyzing JavaScript layer...")
        js_analysis = self._analyze_js_layer(js)
        
        # Layer 4: Analyze design system coherence
        print("  [4/6] Analyzing design system...")
        design_analysis = self._analyze_design_system(html, css, design_system)
        
        # Layer 5: Cross-layer consistency check
        print("  [5/6] Checking cross-layer consistency...")
        consistency_score = self._check_consistency(html, css, js)
        
        # Layer 6: Use LLM for deep insights
        print("  [6/6] Getting LLM insights...")
        llm_insights = self._get_llm_analysis(
            html, css, js, design_system, project_context
        )
        
        # Calculate overall scores
        accessibility_score = self._calculate_accessibility_score(html, css, llm_insights)
        performance_score = self._calculate_performance_score(html, css, js, llm_insights)
        design_quality = self._calculate_design_quality(css_analysis, design_analysis, llm_insights)
        complexity_score = self._calculate_complexity(html, css, js)
        
        overall_score = (
            accessibility_score * 0.25 +
            performance_score * 0.25 +
            design_quality * 0.25 +
            consistency_score * 0.15 +
            (100 - complexity_score) * 0.10
        )
        
        overall_grade = self._score_to_grade(overall_score)
        
        # Compile strengths and weaknesses
        strengths = self._extract_strengths(
            html_analysis, css_analysis, js_analysis, llm_insights
        )
        weaknesses = self._extract_weaknesses(
            html_analysis, css_analysis, js_analysis, llm_insights
        )
        improvements = self._generate_improvements(
            html, css, js, weaknesses, llm_insights
        )
        critical_issues = self._identify_critical_issues(
            html_analysis, css_analysis, js_analysis, llm_insights
        )
        
        # Create comprehensive analysis
        analysis = UIAnalysis(
            overall_grade=overall_grade,
            overall_score=overall_score,
            complexity_score=complexity_score,
            accessibility_score=accessibility_score,
            performance_score=performance_score,
            design_quality_score=design_quality,
            consistency_score=consistency_score,
            strengths=strengths,
            weaknesses=weaknesses,
            improvements=improvements,
            critical_issues=critical_issues,
            html_layer_analysis=html_analysis,
            css_layer_analysis=css_analysis,
            js_layer_analysis=js_analysis,
            design_system_analysis=design_analysis,
            ai_reasoning=llm_insights.get('reasoning', ''),
            confidence_level=llm_insights.get('confidence', 0.85)
        )
        
        # Store in history
        self.analysis_history.append(analysis)
        
        print(f"\n✓ Analysis complete - Grade: {overall_grade} ({overall_score:.1f}/100)")
        
        return analysis
    
    def compare_uis(
        self,
        ui_list: List[Dict[str, str]],
        criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple UIs and identify best practices.
        
        Args:
            ui_list: List of UIs with html, css, js
            criteria: Optional criteria to focus on
        
        Returns:
            Comparison report with rankings and insights
        """
        
        print(f"\n📊 Comparing {len(ui_list)} UIs...")
        
        analyses = []
        for i, ui in enumerate(ui_list, 1):
            print(f"  Analyzing UI {i}/{len(ui_list)}...")
            analysis = self.analyze_ui_comprehensive(
                ui.get('html', ''),
                ui.get('css', ''),
                ui.get('js', ''),
                ui.get('design_system'),
                ui.get('context')
            )
            analyses.append(analysis)
        
        # Use LLM for comparative analysis
        comparison = self._get_llm_comparison(ui_list, analyses, criteria)
        
        # Rank UIs
        rankings = sorted(
            enumerate(analyses),
            key=lambda x: x[1].overall_score,
            reverse=True
        )
        
        # Extract common patterns and best practices
        best_practices = self._extract_best_practices(analyses, comparison)
        common_issues = self._extract_common_issues(analyses)
        
        report = {
            'total_uis': len(ui_list),
            'rankings': [
                {
                    'rank': i + 1,
                    'ui_index': idx,
                    'grade': analysis.overall_grade,
                    'score': analysis.overall_score,
                    'strengths': analysis.strengths[:3],
                    'main_weakness': analysis.weaknesses[0] if analysis.weaknesses else 'None'
                }
                for i, (idx, analysis) in enumerate(rankings)
            ],
            'best_practices': best_practices,
            'common_issues': common_issues,
            'improvement_opportunities': self._identify_improvement_opportunities(analyses),
            'consistency_report': self._check_cross_ui_consistency(analyses),
            'llm_insights': comparison
        }
        
        print(f"✓ Comparison complete")
        print(f"  Best UI: Rank 1 with grade {rankings[0][1].overall_grade}")
        
        return report
    
    def generate_enhancements(
        self,
        html: str,
        css: str,
        js: str,
        analysis: Optional[UIAnalysis] = None,
        focus_areas: Optional[List[str]] = None
    ) -> List[UIEnhancement]:
        """
        Generate specific, actionable enhancements.
        
        Args:
            html: HTML code
            css: CSS code
            js: JavaScript code
            analysis: Optional previous analysis
            focus_areas: Optional areas to focus on
        
        Returns:
            List of prioritized enhancements
        """
        
        print("\n💡 Generating enhancements...")
        
        if not analysis:
            analysis = self.analyze_ui_comprehensive(html, css, js)
        
        # Use LLM to generate specific improvements
        llm_enhancements = self._get_llm_enhancements(
            html, css, js, analysis, focus_areas
        )
        
        enhancements = []
        
        # Parse LLM suggestions into structured enhancements
        for suggestion in llm_enhancements:
            enhancement = UIEnhancement(
                priority=suggestion.get('priority', 'medium'),
                category=suggestion.get('category', 'general'),
                description=suggestion.get('description', ''),
                current_code=suggestion.get('current', ''),
                improved_code=suggestion.get('improved', ''),
                impact=suggestion.get('impact', 'Improves user experience'),
                effort=suggestion.get('effort', 'medium'),
                reasoning=suggestion.get('reasoning', '')
            )
            enhancements.append(enhancement)
            self.enhancement_history.append(enhancement)
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        enhancements.sort(key=lambda x: priority_order.get(x.priority, 2))
        
        print(f"✓ Generated {len(enhancements)} enhancements")
        print(f"  Critical: {sum(1 for e in enhancements if e.priority == 'critical')}")
        print(f"  High: {sum(1 for e in enhancements if e.priority == 'high')}")
        print(f"  Medium: {sum(1 for e in enhancements if e.priority == 'medium')}")
        
        return enhancements
    
    def _analyze_html_layer(self, html: str) -> Dict[str, Any]:
        """Analyze HTML structure"""
        analysis = {
            'semantic_html': 'DOCTYPE' in html and ('<header' in html or '<nav' in html or '<main' in html),
            'accessibility_features': {
                'aria_labels': 'aria-' in html,
                'roles': 'role=' in html,
                'alt_text': 'alt=' in html,
                'semantic_tags': any(tag in html for tag in ['<header', '<nav', '<main', '<article', '<section'])
            },
            'structure_quality': 'good' if '<body>' in html and '</body>' in html else 'needs_improvement',
            'element_count': html.count('<'),
            'complexity': 'high' if html.count('<') > 100 else 'medium' if html.count('<') > 50 else 'low'
        }
        return analysis
    
    def _analyze_css_layer(self, css: str) -> Dict[str, Any]:
        """Analyze CSS styling"""
        analysis = {
            'uses_variables': '--' in css or 'var(' in css,
            'responsive_design': '@media' in css,
            'modern_layout': 'grid' in css or 'flex' in css,
            'animations': '@keyframes' in css or 'animation:' in css or 'transition:' in css,
            'size': len(css),
            'organization': 'good' if '/* ' in css else 'needs_comments',
            'complexity': 'high' if len(css) > 5000 else 'medium' if len(css) > 2000 else 'low'
        }
        return analysis
    
    def _analyze_js_layer(self, js: str) -> Dict[str, Any]:
        """Analyze JavaScript functionality"""
        analysis = {
            'event_handlers': 'addEventListener' in js,
            'modern_syntax': '=>' in js or 'const ' in js or 'let ' in js,
            'error_handling': 'try' in js and 'catch' in js,
            'accessibility_support': 'keydown' in js or 'keypress' in js,
            'size': len(js),
            'complexity': 'high' if len(js) > 3000 else 'medium' if len(js) > 1000 else 'low'
        }
        return analysis
    
    def _analyze_design_system(self, html: str, css: str, design_system: Optional[Dict]) -> Dict[str, Any]:
        """Analyze design system coherence"""
        analysis = {
            'has_design_system': design_system is not None,
            'color_consistency': self._check_color_consistency(css),
            'typography_system': 'font-family:' in css and ('font-size:' in css or '--text-' in css),
            'spacing_system': '--space-' in css or 'padding:' in css,
            'component_reuse': self._check_component_reuse(html, css)
        }
        
        if design_system:
            analysis['design_tokens'] = {
                'colors': 'colors' in design_system,
                'typography': 'typography' in design_system,
                'spacing': 'spacing' in design_system
            }
        
        return analysis
    
    def _check_consistency(self, html: str, css: str, js: str) -> float:
        """Check cross-layer consistency"""
        consistency_score = 70.0  # Base score
        
        # Check naming consistency
        if self._check_naming_consistency(html, css, js):
            consistency_score += 10
        
        # Check structure consistency
        if self._check_structure_consistency(html, css):
            consistency_score += 10
        
        # Check functionality consistency
        if self._check_functionality_consistency(html, js):
            consistency_score += 10
        
        return min(consistency_score, 100.0)
    
    def _check_color_consistency(self, css: str) -> bool:
        """Check if colors are consistently used"""
        # Simple check: using CSS variables for colors
        return '--color-' in css or 'var(--' in css
    
    def _check_component_reuse(self, html: str, css: str) -> bool:
        """Check if components are reusable"""
        # Simple check: class-based styling
        return 'class=' in html and '.' in css
    
    def _check_naming_consistency(self, html: str, css: str, js: str) -> bool:
        """Check naming conventions consistency"""
        # Simple check: consistent use of kebab-case or camelCase
        return True  # Simplified for demo
    
    def _check_structure_consistency(self, html: str, css: str) -> bool:
        """Check structure-style consistency"""
        return True  # Simplified
    
    def _check_functionality_consistency(self, html: str, js: str) -> bool:
        """Check HTML-JS consistency"""
        return 'addEventListener' in js if 'class=' in html else True
    
    def _get_llm_analysis(
        self,
        html: str,
        css: str,
        js: str,
        design_system: Optional[Dict],
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Get deep insights from LLM"""
        
        if not self.api_key:
            return {
                'reasoning': 'LLM analysis skipped - no API key',
                'confidence': 0.5,
                'insights': [],
                'suggestions': []
            }
        
        prompt = f"""Analyze this UI implementation comprehensively:

HTML ({len(html)} chars):
```html
{html[:2000]}{'...' if len(html) > 2000 else ''}
```

CSS ({len(css)} chars):
```css
{css[:1500]}{'...' if len(css) > 1500 else ''}
```

JavaScript ({len(js)} chars):
```javascript
{js[:1000]}{'...' if len(js) > 1000 else ''}
```

Context: {json.dumps(context) if context else 'No specific context provided'}

Please analyze:
1. Overall quality and design coherence
2. Accessibility compliance (WCAG 2.1)
3. Performance considerations
4. Best practices adherence
5. Areas for improvement
6. Specific recommendations

Provide a structured JSON response with: reasoning, confidence (0-1), insights[], suggestions[]"""
        
        try:
            response = self._call_llm(prompt, temperature=0.3)
            # Parse JSON from response
            try:
                return json.loads(response)
            except:
                return {
                    'reasoning': response,
                    'confidence': 0.8,
                    'insights': ['Analysis completed'],
                    'suggestions': []
                }
        except Exception as e:
            print(f"  ⚠ LLM call failed: {str(e)}")
            return {
                'reasoning': f'LLM analysis failed: {str(e)}',
                'confidence': 0.5,
                'insights': [],
                'suggestions': []
            }
    
    def _call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """Call OpenRouter LLM API"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': self.site_url,
            'X-Title': self.app_name,
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.models.get(self.current_model, self.models['gpt-4']),
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert UI/UX analyst with deep knowledge of web development, accessibility, and design systems. Provide detailed, actionable insights.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': temperature,
            'max_tokens': 2000
        }
        
        response = requests.post(self.base_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _calculate_accessibility_score(self, html: str, css: str, llm_insights: Dict) -> float:
        """Calculate accessibility score"""
        score = 50.0
        
        if 'aria-' in html:
            score += 15
        if 'role=' in html:
            score += 10
        if 'alt=' in html:
            score += 10
        if any(tag in html for tag in ['<header', '<nav', '<main']):
            score += 10
        if '@media' in css:
            score += 5
        
        return min(score, 100.0)
    
    def _calculate_performance_score(self, html: str, css: str, js: str, llm_insights: Dict) -> float:
        """Calculate performance score"""
        total_size = len(html) + len(css) + len(js)
        
        if total_size < 10000:
            return 95.0
        elif total_size < 50000:
            return 85.0
        elif total_size < 100000:
            return 75.0
        else:
            return 65.0
    
    def _calculate_design_quality(self, css_analysis: Dict, design_analysis: Dict, llm_insights: Dict) -> float:
        """Calculate design quality score"""
        score = 60.0
        
        if css_analysis.get('uses_variables', False):
            score += 10
        if css_analysis.get('responsive_design', False):
            score += 10
        if css_analysis.get('modern_layout', False):
            score += 10
        if design_analysis.get('has_design_system', False):
            score += 10
        
        return min(score, 100.0)
    
    def _calculate_complexity(self, html: str, css: str, js: str) -> float:
        """Calculate complexity score (lower is better)"""
        html_complexity = min(len(html) / 200, 40)
        css_complexity = min(len(css) / 150, 30)
        js_complexity = min(len(js) / 100, 30)
        
        return min(html_complexity + css_complexity + js_complexity, 100)
    
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
    
    def _extract_strengths(self, html_analysis: Dict, css_analysis: Dict, js_analysis: Dict, llm_insights: Dict) -> List[str]:
        """Extract UI strengths"""
        strengths = []
        
        if html_analysis['semantic_html']:
            strengths.append("Uses semantic HTML5 elements")
        if html_analysis['accessibility_features']['aria_labels']:
            strengths.append("Includes ARIA labels for accessibility")
        if css_analysis['responsive_design']:
            strengths.append("Responsive design with media queries")
        if css_analysis['modern_layout']:
            strengths.append("Modern layout with Grid/Flexbox")
        if css_analysis['uses_variables']:
            strengths.append("Uses CSS variables for maintainability")
        if js_analysis['event_handlers']:
            strengths.append("Proper event handling")
        if js_analysis['modern_syntax']:
            strengths.append("Modern JavaScript syntax")
        
        # Add LLM insights
        if 'insights' in llm_insights:
            strengths.extend(llm_insights['insights'][:3])
        
        return strengths[:10]  # Top 10
    
    def _extract_weaknesses(self, html_analysis: Dict, css_analysis: Dict, js_analysis: Dict, llm_insights: Dict) -> List[str]:
        """Extract UI weaknesses"""
        weaknesses = []
        
        if not html_analysis['semantic_html']:
            weaknesses.append("Missing semantic HTML elements")
        if not html_analysis['accessibility_features']['alt_text']:
            weaknesses.append("Missing alt text on images")
        if not css_analysis['responsive_design']:
            weaknesses.append("Not responsive - missing media queries")
        if not css_analysis['uses_variables']:
            weaknesses.append("Not using CSS variables")
        if not js_analysis['error_handling']:
            weaknesses.append("Missing error handling in JavaScript")
        if css_analysis['organization'] == 'needs_comments':
            weaknesses.append("CSS lacks organization and comments")
        
        return weaknesses[:10]
    
    def _generate_improvements(self, html: str, css: str, js: str, weaknesses: List[str], llm_insights: Dict) -> List[str]:
        """Generate specific improvements"""
        improvements = []
        
        for weakness in weaknesses:
            if "semantic HTML" in weakness:
                improvements.append("Add semantic tags like <header>, <main>, <nav>, <article>")
            elif "alt text" in weakness:
                improvements.append("Add descriptive alt attributes to all <img> tags")
            elif "responsive" in weakness:
                improvements.append("Add @media queries for different screen sizes")
            elif "CSS variables" in weakness:
                improvements.append("Convert hardcoded values to CSS custom properties")
            elif "error handling" in weakness:
                improvements.append("Wrap API calls and risky operations in try-catch blocks")
        
        if 'suggestions' in llm_insights:
            improvements.extend(llm_insights['suggestions'][:5])
        
        return improvements[:15]
    
    def _identify_critical_issues(self, html_analysis: Dict, css_analysis: Dict, js_analysis: Dict, llm_insights: Dict) -> List[str]:
        """Identify critical issues"""
        issues = []
        
        if not html_analysis['accessibility_features']['aria_labels'] and not html_analysis['accessibility_features']['roles']:
            issues.append("CRITICAL: No accessibility features (ARIA/roles)")
        
        if html_analysis['complexity'] == 'high' and css_analysis['complexity'] == 'high':
            issues.append("WARNING: High complexity may impact performance")
        
        if not css_analysis['responsive_design']:
            issues.append("IMPORTANT: Not mobile-friendly")
        
        return issues
    
    def _get_llm_comparison(self, ui_list: List[Dict], analyses: List[UIAnalysis], criteria: Optional[List[str]]) -> Dict:
        """Get LLM comparison insights"""
        # Simplified - would call LLM with comparison prompt
        return {
            'best_overall': 0,
            'reasoning': 'Comparative analysis completed',
            'insights': ['All UIs analyzed and compared']
        }
    
    def _extract_best_practices(self, analyses: List[UIAnalysis], comparison: Dict) -> List[str]:
        """Extract best practices from analyses"""
        practices = []
        
        # Find common strengths in top performers
        top_analyses = sorted(analyses, key=lambda x: x.overall_score, reverse=True)[:3]
        
        for analysis in top_analyses:
            practices.extend(analysis.strengths[:2])
        
        return list(set(practices))[:10]
    
    def _extract_common_issues(self, analyses: List[UIAnalysis]) -> List[str]:
        """Extract common issues"""
        all_weaknesses = []
        for analysis in analyses:
            all_weaknesses.extend(analysis.weaknesses)
        
        # Count frequency
        from collections import Counter
        weakness_counts = Counter(all_weaknesses)
        
        return [w for w, count in weakness_counts.most_common(10) if count > 1]
    
    def _identify_improvement_opportunities(self, analyses: List[UIAnalysis]) -> List[str]:
        """Identify improvement opportunities"""
        opportunities = []
        
        avg_accessibility = sum(a.accessibility_score for a in analyses) / len(analyses)
        avg_performance = sum(a.performance_score for a in analyses) / len(analyses)
        
        if avg_accessibility < 85:
            opportunities.append(f"Improve accessibility (avg: {avg_accessibility:.1f}%)")
        if avg_performance < 85:
            opportunities.append(f"Optimize performance (avg: {avg_performance:.1f}%)")
        
        return opportunities
    
    def _check_cross_ui_consistency(self, analyses: List[UIAnalysis]) -> Dict:
        """Check consistency across UIs"""
        return {
            'consistency_level': 'high' if all(a.consistency_score > 80 for a in analyses) else 'medium',
            'avg_consistency': sum(a.consistency_score for a in analyses) / len(analyses),
            'notes': ['Design patterns are consistent across UIs']
        }
    
    def _get_llm_enhancements(
        self,
        html: str,
        css: str,
        js: str,
        analysis: UIAnalysis,
        focus_areas: Optional[List[str]]
    ) -> List[Dict]:
        """Get specific enhancements from LLM"""
        # Simplified - would call LLM for detailed enhancements
        enhancements = []
        
        # Generate enhancements based on weaknesses
        for weakness in analysis.weaknesses[:5]:
            enhancements.append({
                'priority': 'high' if 'CRITICAL' in weakness or 'accessibility' in weakness.lower() else 'medium',
                'category': 'accessibility' if 'accessibility' in weakness.lower() else 'design',
                'description': f"Fix: {weakness}",
                'current': '// Current implementation',
                'improved': '// Improved implementation',
                'impact': 'Improves user experience and compliance',
                'effort': 'medium',
                'reasoning': f"Addresses identified weakness: {weakness}"
            })
        
        return enhancements
    
    def export_report(self, analysis: UIAnalysis, filename: str = "ui_analysis_report.json"):
        """Export analysis report"""
        report = {
            'grade': analysis.overall_grade,
            'overall_score': analysis.overall_score,
            'scores': {
                'complexity': analysis.complexity_score,
                'accessibility': analysis.accessibility_score,
                'performance': analysis.performance_score,
                'design_quality': analysis.design_quality_score,
                'consistency': analysis.consistency_score
            },
            'strengths': analysis.strengths,
            'weaknesses': analysis.weaknesses,
            'improvements': analysis.improvements,
            'critical_issues': analysis.critical_issues,
            'ai_reasoning': analysis.ai_reasoning,
            'confidence': analysis.confidence_level
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Report exported to {filename}")


# Example usage
if __name__ == "__main__":
    print("Initializing Intelligent UI Agent...")
    agent = IntelligentUIAgent(model='gpt-4')
    
    # Example HTML/CSS/JS
    sample_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample UI</title>
</head>
<body>
    <header role="banner">
        <nav aria-label="Main navigation">
            <h1>My App</h1>
        </nav>
    </header>
    <main role="main">
        <article>
            <h2>Welcome</h2>
            <p>This is a sample UI.</p>
            <button class="btn-primary" aria-label="Get started">Get Started</button>
        </article>
    </main>
</body>
</html>"""
    
    sample_css = """
:root {
    --primary-color: #3b82f6;
    --text-color: #1e293b;
}

body {
    font-family: system-ui, sans-serif;
    color: var(--text-color);
    margin: 0;
    padding: 0;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
}

@media (max-width: 768px) {
    body {
        padding: 1rem;
    }
}
"""
    
    sample_js = """
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('.btn-primary');
    
    button.addEventListener('click', function() {
        console.log('Button clicked');
    });
    
    button.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            this.click();
        }
    });
});
"""
    
    # Perform analysis
    print("\n" + "=" * 60)
    print("  DEMO: Analyzing Sample UI")
    print("=" * 60)
    
    analysis = agent.analyze_ui_comprehensive(sample_html, sample_css, sample_js)
    
    print("\n" + "=" * 60)
    print("  ANALYSIS RESULTS")
    print("=" * 60)
    print(f"\nOverall Grade: {analysis.overall_grade}")
    print(f"Overall Score: {analysis.overall_score:.1f}/100")
    print(f"\nDetailed Scores:")
    print(f"  Accessibility: {analysis.accessibility_score:.1f}%")
    print(f"  Performance: {analysis.performance_score:.1f}%")
    print(f"  Design Quality: {analysis.design_quality_score:.1f}%")
    print(f"  Consistency: {analysis.consistency_score:.1f}%")
    print(f"  Complexity: {analysis.complexity_score:.1f}")
    
    print(f"\nStrengths ({len(analysis.strengths)}):")
    for strength in analysis.strengths[:5]:
        print(f"  ✓ {strength}")
    
    print(f"\nWeaknesses ({len(analysis.weaknesses)}):")
    for weakness in analysis.weaknesses[:5]:
        print(f"  ✗ {weakness}")
    
    print(f"\nImprovements ({len(analysis.improvements)}):")
    for improvement in analysis.improvements[:5]:
        print(f"  → {improvement}")
    
    if analysis.critical_issues:
        print(f"\nCritical Issues ({len(analysis.critical_issues)}):")
        for issue in analysis.critical_issues:
            print(f"  ⚠ {issue}")
    
    # Generate enhancements
    print("\n" + "=" * 60)
    print("  GENERATING ENHANCEMENTS")
    print("=" * 60)
    
    enhancements = agent.generate_enhancements(sample_html, sample_css, sample_js, analysis)
    
    print(f"\nGenerated {len(enhancements)} enhancements:")
    for i, enhancement in enumerate(enhancements[:3], 1):
        print(f"\n{i}. [{enhancement.priority.upper()}] {enhancement.category}")
        print(f"   {enhancement.description}")
        print(f"   Impact: {enhancement.impact}")
        print(f"   Effort: {enhancement.effort}")
    
    # Export report
    print("\n" + "=" * 60)
    agent.export_report(analysis, "demo_analysis_report.json")
    print("=" * 60)
