"""
AI UI Enhancer with OpenRouter Integration
Uses multiple AI models to analyze, critique, and enhance generated UIs
Demonstrates reasoning and multi-model collaboration for UI improvement
"""

import os
import asyncio
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import requests
from playwright.async_api import async_playwright

load_dotenv()


class OpenRouterAIEnhancer:
    """
    AI-powered UI enhancement using OpenRouter API
    Leverages multiple models for reasoning and suggestions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenRouter API key"""
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment or parameters")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.app_name = os.getenv('OPENROUTER_APP_NAME', 'Autonomous-UI-Engine')
        self.site_url = os.getenv('OPENROUTER_SITE_URL', 'https://github.com/spainion/Autonomous-User-Interface-Engine')
        
        # Multiple models for different aspects of analysis
        self.models = {
            'reasoning': 'openai/gpt-4-turbo-preview',  # Deep reasoning and analysis
            'creativity': 'anthropic/claude-3-opus',     # Creative suggestions
            'practical': 'google/gemini-pro',            # Practical improvements
            'fast': 'openai/gpt-3.5-turbo'              # Quick feedback
        }
        
        print("🤖 AI UI Enhancer initialized")
        print(f"   API Key: {self.api_key[:20]}...")
        print(f"   App: {self.app_name}")
        print(f"   Models: {len(self.models)} specialized models")
    
    def call_openrouter(self, prompt: str, model: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Make API call to OpenRouter"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': self.site_url,
            'X-Title': self.app_name,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': temperature
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': True,
                'content': result['choices'][0]['message']['content'],
                'model': model,
                'usage': result.get('usage', {})
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': model
            }
    
    def analyze_ui_structure(self, html_content: str, plain_language: str) -> Dict[str, Any]:
        """Use reasoning model to analyze UI structure"""
        prompt = f"""As an expert UI/UX analyst, analyze this generated user interface.

Original Request: "{plain_language}"

HTML Structure:
{html_content[:2000]}...

Provide a detailed analysis covering:
1. How well it matches the original request
2. Structural strengths and weaknesses
3. Missing elements or opportunities
4. Navigation and flow assessment
5. Overall architecture rating (1-10)

Be specific and actionable."""

        print(f"🧠 Analyzing structure with {self.models['reasoning']}...")
        result = self.call_openrouter(prompt, self.models['reasoning'])
        
        return {
            'type': 'structure_analysis',
            'model': self.models['reasoning'],
            'analysis': result.get('content', 'Analysis failed'),
            'success': result['success']
        }
    
    def get_creative_enhancements(self, html_content: str, project_name: str, style: str) -> Dict[str, Any]:
        """Use creative model to suggest innovative improvements"""
        prompt = f"""As a creative UI designer, suggest innovative enhancements for this {style} style interface for {project_name}.

Current HTML (truncated):
{html_content[:1500]}...

Provide creative suggestions for:
1. Visual enhancements (colors, typography, spacing)
2. Interactive elements and micro-interactions
3. Unique features that would make this stand out
4. Modern design trends that would fit
5. User engagement improvements

Format as a JSON object with categories."""

        print(f"🎨 Getting creative ideas with {self.models['creativity']}...")
        result = self.call_openrouter(prompt, self.models['creativity'], temperature=0.9)
        
        return {
            'type': 'creative_enhancements',
            'model': self.models['creativity'],
            'suggestions': result.get('content', 'No suggestions available'),
            'success': result['success']
        }
    
    def get_practical_improvements(self, html_content: str, ui_type: str) -> Dict[str, Any]:
        """Use practical model for UX and usability improvements"""
        prompt = f"""As a UX engineer, provide practical improvements for this {ui_type} interface.

HTML Structure:
{html_content[:1500]}...

Focus on:
1. Usability issues and fixes
2. Accessibility improvements (ARIA, semantic HTML)
3. Performance optimizations
4. Mobile responsiveness enhancements
5. SEO considerations

Provide concrete, implementable suggestions."""

        print(f"⚙️ Getting practical improvements with {self.models['practical']}...")
        result = self.call_openrouter(prompt, self.models['practical'])
        
        return {
            'type': 'practical_improvements',
            'model': self.models['practical'],
            'improvements': result.get('content', 'No improvements available'),
            'success': result['success']
        }
    
    def get_menu_enhancements(self, html_content: str, project_type: str) -> Dict[str, Any]:
        """Specialized analysis for navigation and menu improvements"""
        prompt = f"""As a navigation specialist, analyze and enhance the menu/navigation system for this {project_type}.

HTML Content:
{html_content[:1500]}...

Provide specific recommendations for:
1. Menu structure and hierarchy
2. Navigation patterns (primary, secondary, mobile)
3. Call-to-action placement
4. User journey optimization
5. Menu items and labels

Include before/after suggestions."""

        print(f"📋 Analyzing menu with {self.models['fast']}...")
        result = self.call_openrouter(prompt, self.models['fast'])
        
        return {
            'type': 'menu_enhancements',
            'model': self.models['fast'],
            'menu_suggestions': result.get('content', 'No menu suggestions available'),
            'success': result['success']
        }
    
    def synthesize_enhancements(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize all analyses into a coherent enhancement plan"""
        # Combine all suggestions
        all_content = "\n\n".join([
            f"=== {a['type'].upper()} ===\n{a.get('analysis') or a.get('suggestions') or a.get('improvements') or a.get('menu_suggestions', '')}"
            for a in analyses if a['success']
        ])
        
        prompt = f"""As a senior product designer, synthesize these AI analyses into a prioritized enhancement plan:

{all_content}

Create a cohesive enhancement strategy with:
1. Top 5 Priority Improvements (highest impact)
2. Quick Wins (easy to implement, high value)
3. Long-term Enhancements (strategic improvements)
4. Implementation Roadmap

Be specific and actionable."""

        print(f"🎯 Synthesizing with {self.models['reasoning']}...")
        result = self.call_openrouter(prompt, self.models['reasoning'])
        
        return {
            'type': 'synthesis',
            'model': self.models['reasoning'],
            'enhancement_plan': result.get('content', 'Synthesis failed'),
            'success': result['success']
        }
    
    def enhance_ui(self, ui_info: Dict[str, Any]) -> Dict[str, Any]:
        """Complete enhancement workflow for a UI"""
        print(f"\n{'='*80}")
        print(f"🚀 ENHANCING UI: {ui_info['project_name']}")
        print(f"{'='*80}")
        
        # Read HTML content
        with open(ui_info['html_path'], 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        start_time = time.time()
        analyses = []
        
        # Run multiple AI analyses in sequence
        analyses.append(self.analyze_ui_structure(
            html_content, 
            ui_info['plain_language']
        ))
        
        analyses.append(self.get_creative_enhancements(
            html_content,
            ui_info['project_name'],
            ui_info['style']
        ))
        
        analyses.append(self.get_practical_improvements(
            html_content,
            ui_info['type']
        ))
        
        analyses.append(self.get_menu_enhancements(
            html_content,
            ui_info['type']
        ))
        
        # Synthesize all analyses
        synthesis = self.synthesize_enhancements(analyses)
        analyses.append(synthesis)
        
        enhancement_time = time.time() - start_time
        
        print(f"\n✅ Enhancement complete in {enhancement_time:.2f}s")
        print(f"   Models used: {len(set(a['model'] for a in analyses))}")
        print(f"   Successful analyses: {sum(1 for a in analyses if a['success'])}/{len(analyses)}")
        
        return {
            'project_name': ui_info['project_name'],
            'plain_language': ui_info['plain_language'],
            'analyses': analyses,
            'enhancement_time': enhancement_time,
            'models_used': list(set(a['model'] for a in analyses))
        }


class PlaywrightAIEnhancerDemo:
    """Demonstrate AI enhancement with Playwright visualization"""
    
    def __init__(self, preview_dir: str = "playwright_previews", output_dir: str = "ai_enhanced"):
        """Initialize demo"""
        self.preview_dir = Path(preview_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.enhancer = OpenRouterAIEnhancer()
        
        # Load existing manifest
        manifest_path = self.preview_dir / "manifest.json"
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
    
    async def enhance_and_visualize(self, num_uis: int = 3):
        """Enhance UIs and create visualization"""
        print("\n" + "="*80)
        print("  AI UI ENHANCEMENT DEMO")
        print("  Using OpenRouter API with Multiple Models")
        print("="*80)
        print(f"Enhancing {num_uis} UIs from gallery")
        print("="*80)
        
        enhancements = []
        
        # Enhance selected UIs
        for ui_info in self.manifest['uis'][:num_uis]:
            enhancement = self.enhancer.enhance_ui(ui_info)
            enhancements.append(enhancement)
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(2)
        
        # Save enhancement results
        self.save_enhancements(enhancements)
        
        # Create visualization page
        await self.create_enhancement_visualization(enhancements)
        
        return enhancements
    
    def save_enhancements(self, enhancements: List[Dict[str, Any]]):
        """Save enhancement results to file"""
        output_path = self.output_dir / "enhancements.json"
        with open(output_path, 'w') as f:
            json.dump(enhancements, f, indent=2)
        
        print(f"\n💾 Enhancements saved to: {output_path}")
    
    async def create_enhancement_visualization(self, enhancements: List[Dict[str, Any]]):
        """Create HTML page showing enhancements"""
        
        enhancement_cards = []
        for enhancement in enhancements:
            # Get synthesis for display
            synthesis = next((a for a in enhancement['analyses'] if a['type'] == 'synthesis'), None)
            synthesis_content = synthesis.get('enhancement_plan', 'No synthesis available') if synthesis else 'No synthesis available'
            
            # Create cards for each analysis
            analysis_sections = []
            for analysis in enhancement['analyses']:
                if analysis['type'] != 'synthesis' and analysis['success']:
                    content = (analysis.get('analysis') or 
                             analysis.get('suggestions') or 
                             analysis.get('improvements') or 
                             analysis.get('menu_suggestions', ''))
                    
                    analysis_sections.append(f"""
                        <div class="analysis-section">
                            <h4>{analysis['type'].replace('_', ' ').title()}</h4>
                            <p class="model-badge">Model: {analysis['model'].split('/')[-1]}</p>
                            <div class="analysis-content">{self._format_markdown(content[:1000])}</div>
                        </div>
                    """)
            
            enhancement_cards.append(f"""
                <div class="enhancement-card">
                    <div class="card-header">
                        <h2>{enhancement['project_name']}</h2>
                        <span class="time-badge">{enhancement['enhancement_time']:.2f}s</span>
                    </div>
                    <div class="plain-language">
                        <strong>Original Request:</strong>
                        <p>"{enhancement['plain_language']}"</p>
                    </div>
                    <div class="models-used">
                        <strong>AI Models Used:</strong>
                        <div class="model-tags">
                            {''.join(f'<span class="model-tag">{m.split("/")[-1]}</span>' for m in enhancement['models_used'])}
                        </div>
                    </div>
                    <div class="synthesis-section">
                        <h3>🎯 Enhancement Plan (AI Synthesis)</h3>
                        <div class="synthesis-content">{self._format_markdown(synthesis_content[:2000])}</div>
                    </div>
                    <details class="analysis-details">
                        <summary>View Detailed Analyses ({len(analysis_sections)} analyses)</summary>
                        <div class="analyses-grid">
                            {''.join(analysis_sections)}
                        </div>
                    </details>
                </div>
            """)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI UI Enhancement Results</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            line-height: 1.6;
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }}
        
        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .stats {{
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            margin: 2rem 0;
            flex-wrap: wrap;
        }}
        
        .stat {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .enhancement-card {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .card-header h2 {{
            color: #333;
            font-size: 1.8rem;
        }}
        
        .time-badge {{
            background: #667eea;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        .plain-language {{
            background: #f8f9fa;
            padding: 1rem;
            border-left: 4px solid #667eea;
            margin-bottom: 1.5rem;
            border-radius: 4px;
        }}
        
        .plain-language strong {{
            color: #667eea;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .models-used {{
            margin-bottom: 1.5rem;
        }}
        
        .models-used strong {{
            color: #333;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .model-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .model-tag {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .synthesis-section {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }}
        
        .synthesis-section h3 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .synthesis-content {{
            color: #444;
            white-space: pre-wrap;
            line-height: 1.8;
        }}
        
        .analysis-details {{
            margin-top: 1.5rem;
        }}
        
        .analysis-details summary {{
            cursor: pointer;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 6px;
            font-weight: 600;
            color: #667eea;
            user-select: none;
        }}
        
        .analysis-details summary:hover {{
            background: #e9ecef;
        }}
        
        .analyses-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .analysis-section {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .analysis-section h4 {{
            color: #333;
            margin-bottom: 0.5rem;
        }}
        
        .model-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 10px;
            font-size: 0.75rem;
            margin-bottom: 0.5rem;
        }}
        
        .analysis-content {{
            color: #555;
            font-size: 0.9rem;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 3rem;
            padding: 2rem;
            opacity: 0.9;
        }}
        
        @media (max-width: 768px) {{
            .analyses-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI UI Enhancement Results</h1>
            <p>Multi-Model Analysis & Enhancement Recommendations</p>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(enhancements)}</div>
                <div class="stat-label">UIs Enhanced</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(len(e['models_used']) for e in enhancements)}</div>
                <div class="stat-label">Total AI Analyses</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(e['enhancement_time'] for e in enhancements):.1f}s</div>
                <div class="stat-label">Processing Time</div>
            </div>
        </div>
        
        {''.join(enhancement_cards)}
        
        <footer>
            <p>Powered by OpenRouter AI with Multiple Models</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                GPT-4, Claude-3, Gemini Pro, GPT-3.5 working together
            </p>
        </footer>
    </div>
</body>
</html>"""
        
        output_path = self.output_dir / "enhancement_results.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"📄 Visualization created: {output_path}")
        print(f"\n🌐 Open in browser: file://{output_path.absolute()}")
    
    def _format_markdown(self, text: str) -> str:
        """Simple markdown-like formatting"""
        # Replace newlines with HTML breaks for readability
        return text.replace('\n\n', '<br><br>').replace('\n', '<br>')


async def main():
    """Main demo function"""
    demo = PlaywrightAIEnhancerDemo()
    await demo.enhance_and_visualize(num_uis=3)
    
    print("\n" + "="*80)
    print("✅ AI Enhancement Demo Complete!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
