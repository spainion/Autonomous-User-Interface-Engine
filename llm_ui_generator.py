"""
LLM-Enhanced UI Generator
Uses OpenRouter for intelligent UI generation with reasoning
"""

import os
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class LLMUIResult:
    """Result from LLM UI generation"""
    html: str
    css: str
    js: str
    reasoning: str
    quality_score: float
    improvements: List[str]


class LLMUIGenerator:
    """Generate and enhance UI using LLM reasoning"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        self.models = {
            'gpt-4': 'openai/gpt-4-turbo-preview',
            'claude': 'anthropic/claude-3-opus',
            'gemini': 'google/gemini-pro',
            'mixtral': 'mistralai/mixtral-8x7b-instruct',
            'llama': 'meta-llama/llama-3-70b-instruct'
        }
    
    def generate_with_reasoning(
        self,
        prompt: str,
        model: str = 'gpt-4',
        enhance_prompt: bool = True,
        research_enabled: bool = True,
        variants: int = 1,
        framework: str = 'bootstrap'
    ) -> LLMUIResult:
        """Generate UI with LLM reasoning"""
        
        # Enhance prompt if requested
        if enhance_prompt:
            prompt = self._enhance_prompt(prompt, framework, research_enabled)
        
        # Call LLM API
        response = self._call_llm(prompt, model)
        
        # Parse response
        html, css, js = self._parse_llm_response(response)
        
        # Extract reasoning
        reasoning = self._extract_reasoning(response)
        
        # Calculate quality score
        quality_score = self._calculate_quality(html, css, js)
        
        # Generate improvements
        improvements = self._generate_improvements(html, css, js)
        
        return LLMUIResult(
            html=html,
            css=css,
            js=js,
            reasoning=reasoning,
            quality_score=quality_score,
            improvements=improvements
        )
    
    def critique_and_improve(
        self,
        html_code: str,
        css_code: str = "",
        js_code: str = "",
        focus: str = "usability",
        iterations: int = 1,
        model: str = 'gpt-4'
    ) -> LLMUIResult:
        """Critique existing UI and generate improvements"""
        
        critique_prompt = f"""Analyze this HTML/CSS/JS code and provide improvements focused on {focus}:

HTML:
```html
{html_code}
```

CSS:
```css
{css_code}
```

JS:
```javascript
{js_code}
```

Provide:
1. Detailed critique
2. Specific improvements
3. Improved code
4. Reasoning for changes

Focus on: {focus}
Standards: WCAG 2.1 AA, responsive design, performance, usability"""
        
        response = self._call_llm(critique_prompt, model)
        
        # Parse improved code
        improved_html, improved_css, improved_js = self._parse_llm_response(response)
        
        # If multiple iterations requested
        if iterations > 1:
            for i in range(iterations - 1):
                result = self.critique_and_improve(
                    improved_html,
                    improved_css,
                    improved_js,
                    focus,
                    1,
                    model
                )
                improved_html = result.html
                improved_css = result.css
                improved_js = result.js
        
        return LLMUIResult(
            html=improved_html,
            css=improved_css,
            js=improved_js,
            reasoning=self._extract_reasoning(response),
            quality_score=self._calculate_quality(improved_html, improved_css, improved_js),
            improvements=[]
        )
    
    def generate_variants(
        self,
        prompt: str,
        count: int = 3,
        model: str = 'gpt-4',
        framework: str = 'bootstrap'
    ) -> List[LLMUIResult]:
        """Generate multiple UI variants"""
        
        variants = []
        
        for i in range(count):
            variant_prompt = f"{prompt}\n\nGenerate variant #{i+1} with a different approach/style."
            result = self.generate_with_reasoning(
                variant_prompt,
                model=model,
                enhance_prompt=True,
                framework=framework
            )
            variants.append(result)
        
        return variants
    
    def _enhance_prompt(self, prompt: str, framework: str, research: bool) -> str:
        """Enhance prompt with context and best practices"""
        
        enhanced = f"""Create a high-quality, production-ready UI component/page based on this description:
{prompt}

Requirements:
- Framework: {framework}
- Responsive design (mobile-first)
- WCAG 2.1 AA accessibility compliance
- Modern design principles
- Clean, semantic HTML
- Optimized CSS (no unnecessary code)
- Performance-focused
- Cross-browser compatible

Include:
1. Complete HTML structure
2. CSS styling (inline in <style> tag or as separate CSS)
3. Any necessary JavaScript (if needed)
4. ARIA labels and accessibility features
5. Responsive breakpoints
6. Smooth animations/transitions

Follow best practices for:
- Typography (readable, hierarchy)
- Color (sufficient contrast, accessible)
- Spacing (consistent, whitespace)
- Layout (clear structure, visual hierarchy)
- Interactivity (clear affordances, feedback)

Provide the code in this format:
HTML:
```html
[html code here]
```

CSS:
```css
[css code here]
```

JavaScript:
```javascript
[js code if needed]
```

Reasoning:
[Explain design decisions and why they work]"""
        
        return enhanced
    
    def _call_llm(self, prompt: str, model: str) -> str:
        """Call OpenRouter API"""
        
        if not self.api_key:
            # Return simulated response for demo
            return self._get_simulated_response(prompt)
        
        try:
            model_id = self.models.get(model, self.models['gpt-4'])
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model_id,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except Exception as e:
            print(f"LLM API error: {e}")
            return self._get_simulated_response(prompt)
    
    def _get_simulated_response(self, prompt: str) -> str:
        """Get simulated LLM response for demo"""
        
        return """HTML:
```html
<div class="container">
    <div class="card shadow-sm">
        <div class="card-body">
            <h2 class="card-title">Modern UI Component</h2>
            <p class="card-text">This is a well-designed, accessible component following best practices.</p>
            <button class="btn btn-primary" aria-label="Take action">Get Started</button>
        </div>
    </div>
</div>
```

CSS:
```css
.container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 1rem;
}
.card {
    border-radius: 12px;
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
.card-title {
    color: #333;
    margin-bottom: 1rem;
}
.btn-primary {
    background: #007bff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    transition: all 0.3s;
}
.btn-primary:hover {
    background: #0056b3;
    transform: scale(1.05);
}
```

JavaScript:
```javascript
// Add smooth scroll behavior
document.querySelector('.btn-primary').addEventListener('click', function() {
    console.log('Action triggered');
});
```

Reasoning:
The design uses a card-based layout for clear content separation. The hover effects provide visual feedback. Colors meet WCAG AA contrast requirements. The component is fully responsive and keyboard-accessible with proper ARIA labels. CSS transitions create smooth interactions without JavaScript dependency."""
    
    def _parse_llm_response(self, response: str) -> tuple:
        """Parse HTML, CSS, JS from LLM response"""
        
        html = ""
        css = ""
        js = ""
        
        # Extract HTML
        if "```html" in response:
            start = response.find("```html") + 7
            end = response.find("```", start)
            html = response[start:end].strip()
        
        # Extract CSS
        if "```css" in response:
            start = response.find("```css") + 6
            end = response.find("```", start)
            css = response[start:end].strip()
        
        # Extract JavaScript
        if "```javascript" in response or "```js" in response:
            marker = "```javascript" if "```javascript" in response else "```js"
            start = response.find(marker) + len(marker)
            end = response.find("```", start)
            js = response[start:end].strip()
        
        return html, css, js
    
    def _extract_reasoning(self, response: str) -> str:
        """Extract reasoning from LLM response"""
        
        if "Reasoning:" in response:
            start = response.find("Reasoning:") + 10
            reasoning = response[start:].strip()
            return reasoning
        
        return "Design follows modern best practices with focus on usability and accessibility."
    
    def _calculate_quality(self, html: str, css: str, js: str) -> float:
        """Calculate quality score"""
        
        score = 70.0  # Base score
        
        # Check for accessibility features
        if 'aria-label' in html:
            score += 5
        if 'alt=' in html:
            score += 5
        if 'role=' in html:
            score += 3
        
        # Check for responsive design
        if '@media' in css or 'responsive' in css.lower():
            score += 7
        
        # Check for semantic HTML
        semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        if any(tag in html for tag in semantic_tags):
            score += 5
        
        # Check for transitions/animations
        if 'transition' in css or 'animation' in css:
            score += 5
        
        return min(100.0, score)
    
    def _generate_improvements(self, html: str, css: str, js: str) -> List[str]:
        """Generate list of possible improvements"""
        
        improvements = []
        
        if 'alt=' not in html and '<img' in html:
            improvements.append("Add alt text to all images for accessibility")
        
        if 'aria-label' not in html and '<button' in html:
            improvements.append("Add ARIA labels to interactive elements")
        
        if '@media' not in css:
            improvements.append("Add responsive breakpoints for mobile devices")
        
        if 'transition' not in css and ':hover' in css:
            improvements.append("Add smooth transitions for hover effects")
        
        if '<form' in html and 'required' not in html:
            improvements.append("Add validation attributes to form fields")
        
        return improvements
    
    def analyze_design_trends(self, niche: str) -> Dict[str, Any]:
        """Analyze design trends for a niche using LLM"""
        
        prompt = f"""Analyze current design trends for {niche} websites/applications.

Provide:
1. Top 5 design trends
2. Common color schemes
3. Popular typography choices
4. Layout patterns
5. Interactive elements
6. Best practices specific to {niche}

Format as JSON."""
        
        response = self._call_llm(prompt, 'gpt-4')
        
        # Try to parse as JSON, or return structured dict
        try:
            return json.loads(response)
        except:
            return {
                'niche': niche,
                'trends': ['Modern', 'Minimal', 'Bold typography'],
                'colors': ['Blue', 'White', 'Accent colors'],
                'typography': ['Sans-serif', 'Large headings'],
                'layouts': ['Card-based', 'Grid layouts'],
                'interactions': ['Smooth transitions', 'Micro-interactions']
            }


if __name__ == "__main__":
    generator = LLMUIGenerator()
    
    # Generate UI with reasoning
    result = generator.generate_with_reasoning(
        "Create a pricing table with 3 tiers",
        model='gpt-4',
        framework='bootstrap'
    )
    
    print("Generated UI:")
    print(f"Quality Score: {result.quality_score}")
    print(f"Reasoning: {result.reasoning[:200]}...")
    print(f"\nHTML Preview:")
    print(result.html[:300] + "...")
    
    # Analyze trends
    trends = generator.analyze_design_trends("fintech")
    print(f"\nFintech Design Trends:")
    print(json.dumps(trends, indent=2))
