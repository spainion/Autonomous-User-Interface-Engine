"""
Real-Time UI Analysis with OpenRouter API
Live testing and verification with actual network requests
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Import our intelligent agent
from intelligent_ui_agent import IntelligentUIAgent, UIAnalysis


class LiveUITester:
    """Real-time UI testing with OpenRouter API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
        
        print("=" * 80)
        print("  LIVE UI ANALYSIS SYSTEM")
        print("=" * 80)
        print(f"✓ API Key loaded: {self.api_key[:20]}...")
        print(f"✓ App: {os.getenv('OPENROUTER_APP_NAME', 'UI-Engine')}")
        print("=" * 80)
        print()
        
        self.agent = IntelligentUIAgent(api_key=self.api_key, model='gpt-4')
        self.test_results = []
    
    def test_api_connection(self) -> bool:
        """Test OpenRouter API connection"""
        print("🔗 Testing OpenRouter API connection...")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'HTTP-Referer': os.getenv('OPENROUTER_SITE_URL', ''),
                'X-Title': os.getenv('OPENROUTER_APP_NAME', ''),
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'openai/gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'user',
                        'content': 'Respond with "API Connected" if you receive this message.'
                    }
                ],
                'max_tokens': 50
            }
            
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"  Response: {message}")
                print("  ✓ API Connection successful!")
                return True
            else:
                print(f"  ✗ API Error: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ✗ Connection failed: {str(e)}")
            return False
    
    def analyze_sample_ui_live(self):
        """Analyze a sample UI with live API calls"""
        
        print("\n" + "=" * 80)
        print("  TEST 1: Analyzing Modern SaaS Landing Page")
        print("=" * 80)
        
        # Sample HTML
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudFlow - Modern Cloud Storage</title>
    <meta name="description" content="Secure cloud storage for businesses">
</head>
<body>
    <header role="banner">
        <nav aria-label="Main navigation" class="navbar">
            <div class="logo">
                <h1>CloudFlow</h1>
            </div>
            <ul role="list">
                <li><a href="#features">Features</a></li>
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#about">About</a></li>
            </ul>
        </nav>
    </header>
    
    <main role="main">
        <section class="hero" aria-labelledby="hero-title">
            <h2 id="hero-title">Secure Cloud Storage for Your Business</h2>
            <p>Store, share, and collaborate with enterprise-grade security.</p>
            <button class="btn-primary" aria-label="Get started with CloudFlow">
                Get Started Free
            </button>
        </section>
        
        <section class="features" aria-labelledby="features-title">
            <h2 id="features-title">Key Features</h2>
            <div class="feature-grid">
                <article class="feature-card">
                    <h3>Secure Storage</h3>
                    <p>Bank-level encryption for all your files.</p>
                </article>
                <article class="feature-card">
                    <h3>Team Collaboration</h3>
                    <p>Share and collaborate in real-time.</p>
                </article>
                <article class="feature-card">
                    <h3>24/7 Support</h3>
                    <p>Get help whenever you need it.</p>
                </article>
            </div>
        </section>
    </main>
    
    <footer role="contentinfo">
        <p>&copy; 2024 CloudFlow. All rights reserved.</p>
    </footer>
</body>
</html>"""
        
        # Sample CSS
        css = """:root {
    --primary-color: #3b82f6;
    --secondary-color: #1e40af;
    --text-color: #1e293b;
    --background-color: #ffffff;
    --border-radius: 0.5rem;
    --spacing-unit: 1rem;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--text-color);
    background-color: var(--background-color);
    line-height: 1.6;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar ul {
    display: flex;
    gap: calc(var(--spacing-unit) * 2);
    list-style: none;
}

.navbar a {
    color: var(--text-color);
    text-decoration: none;
    transition: color 0.3s ease;
}

.navbar a:hover,
.navbar a:focus {
    color: var(--primary-color);
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
}

.hero {
    text-align: center;
    padding: calc(var(--spacing-unit) * 6) calc(var(--spacing-unit) * 2);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-unit);
}

.btn-primary {
    background: var(--primary-color);
    color: white;
    padding: 0.75rem 2rem;
    border: none;
    border-radius: var(--border-radius);
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary:hover,
.btn-primary:focus {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.features {
    padding: calc(var(--spacing-unit) * 4) calc(var(--spacing-unit) * 2);
    max-width: 1200px;
    margin: 0 auto;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: calc(var(--spacing-unit) * 2);
    margin-top: calc(var(--spacing-unit) * 2);
}

.feature-card {
    padding: calc(var(--spacing-unit) * 2);
    border: 1px solid #e5e7eb;
    border-radius: var(--border-radius);
    transition: box-shadow 0.3s ease;
}

.feature-card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

footer {
    text-align: center;
    padding: calc(var(--spacing-unit) * 2);
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
}

@media (max-width: 768px) {
    .hero h2 {
        font-size: 1.75rem;
    }
    
    .navbar {
        flex-direction: column;
        gap: var(--spacing-unit);
    }
    
    .navbar ul {
        flex-direction: column;
        gap: var(--spacing-unit);
    }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}"""
        
        # Sample JavaScript
        js = """document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.navbar a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Keyboard navigation support
    const buttons = document.querySelectorAll('button, a');
    
    buttons.forEach(element => {
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // CTA button analytics
    const ctaButton = document.querySelector('.btn-primary');
    
    if (ctaButton) {
        ctaButton.addEventListener('click', function() {
            console.log('CTA clicked: Get Started');
            // Would send analytics event here
        });
    }
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });
});"""
        
        # Perform live analysis
        print("\n📊 Running comprehensive analysis with OpenRouter LLM...")
        start_time = time.time()
        
        try:
            analysis = self.agent.analyze_ui_comprehensive(
                html=html,
                css=css,
                js=js,
                design_system={
                    'colors': {'primary': '#3b82f6', 'secondary': '#1e40af'},
                    'typography': {'base': 'system-ui'},
                    'spacing': {'unit': '1rem'}
                },
                project_context={
                    'type': 'SaaS Landing Page',
                    'target_audience': 'Business users',
                    'goals': ['Lead generation', 'Brand awareness']
                }
            )
            
            analysis_time = time.time() - start_time
            
            # Display results
            self._display_analysis_results(analysis, analysis_time)
            
            # Store results
            self.test_results.append({
                'test': 'SaaS Landing Page',
                'analysis': analysis,
                'time': analysis_time
            })
            
            return analysis
            
        except Exception as e:
            print(f"\n✗ Analysis failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_ui_comparison_live(self):
        """Test comparing multiple UIs with live API"""
        
        print("\n" + "=" * 80)
        print("  TEST 2: Comparing Multiple UI Implementations")
        print("=" * 80)
        
        # Two UI variations to compare
        ui1 = {
            'name': 'Modern Approach',
            'html': '<div class="container"><button class="btn-modern">Click Me</button></div>',
            'css': '.container { display: flex; } .btn-modern { padding: 1rem; background: #3b82f6; color: white; border: none; border-radius: 0.5rem; }',
            'js': 'document.querySelector(".btn-modern").addEventListener("click", () => console.log("clicked"));'
        }
        
        ui2 = {
            'name': 'Classic Approach',
            'html': '<div class="wrapper"><button class="btn-classic" onclick="handleClick()">Click Me</button></div>',
            'css': '.wrapper { text-align: center; } .btn-classic { padding: 10px 20px; background: blue; color: white; }',
            'js': 'function handleClick() { alert("clicked"); }'
        }
        
        print(f"\nComparing 2 UI implementations...")
        
        try:
            comparison = self.agent.compare_uis(
                ui_list=[ui1, ui2],
                criteria=['modern syntax', 'accessibility', 'performance']
            )
            
            print(f"\n✓ Comparison complete!")
            print(f"\nRankings:")
            for rank in comparison['rankings']:
                print(f"  {rank['rank']}. {['UI 1', 'UI 2'][rank['ui_index']]} - Grade: {rank['grade']} ({rank['score']:.1f})")
            
            print(f"\nBest Practices Identified:")
            for practice in comparison['best_practices'][:5]:
                print(f"  ✓ {practice}")
            
            if comparison['common_issues']:
                print(f"\nCommon Issues:")
                for issue in comparison['common_issues'][:3]:
                    print(f"  ⚠ {issue}")
            
            return comparison
            
        except Exception as e:
            print(f"\n✗ Comparison failed: {str(e)}")
            return None
    
    def test_enhancement_generation_live(self, analysis: UIAnalysis):
        """Test generating enhancements with live API"""
        
        print("\n" + "=" * 80)
        print("  TEST 3: Generating AI-Powered Enhancements")
        print("=" * 80)
        
        if not analysis:
            print("⚠ No analysis available, skipping enhancement test")
            return
        
        print("\n💡 Generating enhancements based on analysis...")
        
        try:
            # Use sample code for enhancement
            html = '<div><button>Click</button></div>'
            css = 'button { background: blue; }'
            js = 'document.querySelector("button").onclick = function() { alert("hi"); }'
            
            enhancements = self.agent.generate_enhancements(
                html=html,
                css=css,
                js=js,
                analysis=analysis,
                focus_areas=['accessibility', 'modern practices']
            )
            
            print(f"\n✓ Generated {len(enhancements)} enhancements")
            
            print(f"\nTop Priority Enhancements:")
            for i, enhancement in enumerate(enhancements[:5], 1):
                print(f"\n{i}. [{enhancement.priority.upper()}] {enhancement.category}")
                print(f"   Description: {enhancement.description}")
                print(f"   Impact: {enhancement.impact}")
                print(f"   Effort: {enhancement.effort}")
                if enhancement.reasoning:
                    print(f"   Reasoning: {enhancement.reasoning[:100]}...")
            
            return enhancements
            
        except Exception as e:
            print(f"\n✗ Enhancement generation failed: {str(e)}")
            return None
    
    def test_real_world_ui(self):
        """Test with a more complex real-world UI"""
        
        print("\n" + "=" * 80)
        print("  TEST 4: Analyzing Complex Dashboard UI")
        print("=" * 80)
        
        # More complex dashboard example
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard</title>
</head>
<body>
    <div class="dashboard-container">
        <aside class="sidebar" role="navigation" aria-label="Dashboard navigation">
            <nav>
                <h2>Dashboard</h2>
                <ul>
                    <li><a href="#overview" aria-current="page">Overview</a></li>
                    <li><a href="#analytics">Analytics</a></li>
                    <li><a href="#reports">Reports</a></li>
                    <li><a href="#settings">Settings</a></li>
                </ul>
            </nav>
        </aside>
        
        <main class="dashboard-main" role="main">
            <header>
                <h1>Analytics Overview</h1>
                <p>Last updated: <time datetime="2024-01-15">January 15, 2024</time></p>
            </header>
            
            <section class="metrics-grid" aria-label="Key metrics">
                <article class="metric-card">
                    <h3>Total Users</h3>
                    <p class="metric-value">12,345</p>
                    <p class="metric-change positive">+15% from last month</p>
                </article>
                <article class="metric-card">
                    <h3>Revenue</h3>
                    <p class="metric-value">$54,321</p>
                    <p class="metric-change positive">+8% from last month</p>
                </article>
                <article class="metric-card">
                    <h3>Active Sessions</h3>
                    <p class="metric-value">1,234</p>
                    <p class="metric-change negative">-3% from last hour</p>
                </article>
            </section>
            
            <section class="charts" aria-label="Analytics charts">
                <div class="chart-container">
                    <h2>User Growth</h2>
                    <div id="user-chart" role="img" aria-label="Line chart showing user growth over time"></div>
                </div>
            </section>
        </main>
    </div>
</body>
</html>"""
        
        css = """:root {
    --sidebar-width: 250px;
    --primary-color: #6366f1;
    --success-color: #10b981;
    --danger-color: #ef4444;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --border-color: #e2e8f0;
}

.dashboard-container {
    display: grid;
    grid-template-columns: var(--sidebar-width) 1fr;
    min-height: 100vh;
}

.sidebar {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    padding: 2rem 1rem;
}

.sidebar nav ul {
    list-style: none;
    padding: 0;
}

.sidebar nav a {
    display: block;
    padding: 0.75rem 1rem;
    color: var(--text-primary);
    text-decoration: none;
    border-radius: 0.5rem;
    transition: background-color 0.2s;
}

.sidebar nav a:hover,
.sidebar nav a:focus {
    background: white;
}

.sidebar nav a[aria-current="page"] {
    background: var(--primary-color);
    color: white;
}

.dashboard-main {
    padding: 2rem;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid var(--border-color);
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
}

.metric-change {
    font-size: 0.875rem;
}

.metric-change.positive {
    color: var(--success-color);
}

.metric-change.negative {
    color: var(--danger-color);
}

.chart-container {
    background: white;
    padding: 2rem;
    border-radius: 0.75rem;
    border: 1px solid var(--border-color);
}

@media (max-width: 768px) {
    .dashboard-container {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        border-right: none;
        border-bottom: 1px solid var(--border-color);
    }
}"""
        
        js = """const dashboard = {
    init() {
        this.setupNavigation();
        this.loadMetrics();
        this.setupCharts();
        this.startAutoRefresh();
    },
    
    setupNavigation() {
        const navLinks = document.querySelectorAll('.sidebar nav a');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateTo(link.getAttribute('href'));
            });
        });
    },
    
    loadMetrics() {
        // Simulate loading metrics
        console.log('Loading metrics...');
    },
    
    setupCharts() {
        // Initialize chart library
        const chartEl = document.getElementById('user-chart');
        if (chartEl) {
            // Chart rendering code
        }
    },
    
    navigateTo(section) {
        document.querySelectorAll('.sidebar nav a').forEach(a => {
            a.removeAttribute('aria-current');
        });
        document.querySelector(`[href="${section}"]`).setAttribute('aria-current', 'page');
    },
    
    startAutoRefresh() {
        setInterval(() => {
            this.loadMetrics();
        }, 30000); // Refresh every 30 seconds
    }
};

document.addEventListener('DOMContentLoaded', () => {
    dashboard.init();
});"""
        
        print("\n📊 Analyzing complex dashboard UI...")
        
        try:
            analysis = self.agent.analyze_ui_comprehensive(
                html=html,
                css=css,
                js=js,
                design_system={
                    'colors': {
                        'primary': '#6366f1',
                        'success': '#10b981',
                        'danger': '#ef4444'
                    },
                    'typography': {'base': 'system-ui'},
                    'spacing': {'sidebar_width': '250px'}
                },
                project_context={
                    'type': 'Analytics Dashboard',
                    'target_audience': 'Business analysts',
                    'goals': ['Data visualization', 'Real-time monitoring']
                }
            )
            
            self._display_analysis_results(analysis, 0)
            return analysis
            
        except Exception as e:
            print(f"\n✗ Analysis failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _display_analysis_results(self, analysis: UIAnalysis, time_taken: float):
        """Display analysis results in a formatted way"""
        
        print("\n" + "=" * 80)
        print("  ANALYSIS RESULTS")
        print("=" * 80)
        
        print(f"\n🎯 Overall Assessment")
        print(f"  Grade: {analysis.overall_grade}")
        print(f"  Score: {analysis.overall_score:.1f}/100")
        print(f"  Analysis Time: {time_taken:.2f}s")
        print(f"  AI Confidence: {analysis.confidence_level:.1%}")
        
        print(f"\n📊 Detailed Scores")
        print(f"  Accessibility:  {analysis.accessibility_score:.1f}%")
        print(f"  Performance:    {analysis.performance_score:.1f}%")
        print(f"  Design Quality: {analysis.design_quality_score:.1f}%")
        print(f"  Consistency:    {analysis.consistency_score:.1f}%")
        print(f"  Complexity:     {analysis.complexity_score:.1f}")
        
        if analysis.strengths:
            print(f"\n✓ Strengths ({len(analysis.strengths)})")
            for i, strength in enumerate(analysis.strengths[:5], 1):
                print(f"  {i}. {strength}")
        
        if analysis.weaknesses:
            print(f"\n✗ Weaknesses ({len(analysis.weaknesses)})")
            for i, weakness in enumerate(analysis.weaknesses[:5], 1):
                print(f"  {i}. {weakness}")
        
        if analysis.improvements:
            print(f"\n→ Recommended Improvements ({len(analysis.improvements)})")
            for i, improvement in enumerate(analysis.improvements[:5], 1):
                print(f"  {i}. {improvement}")
        
        if analysis.critical_issues:
            print(f"\n⚠ Critical Issues ({len(analysis.critical_issues)})")
            for i, issue in enumerate(analysis.critical_issues, 1):
                print(f"  {i}. {issue}")
        
        if analysis.ai_reasoning:
            print(f"\n🤖 AI Reasoning")
            reasoning_preview = analysis.ai_reasoning[:300]
            if len(analysis.ai_reasoning) > 300:
                reasoning_preview += "..."
            print(f"  {reasoning_preview}")
    
    def run_all_tests(self):
        """Run all live tests"""
        
        print("\n" + "=" * 80)
        print("  STARTING LIVE UI ANALYSIS TESTS")
        print("=" * 80)
        
        # Test 1: API Connection
        if not self.test_api_connection():
            print("\n✗ API connection test failed. Aborting further tests.")
            return False
        
        # Test 2: Sample UI Analysis
        analysis = self.analyze_sample_ui_live()
        
        # Test 3: UI Comparison
        self.test_ui_comparison_live()
        
        # Test 4: Enhancement Generation
        if analysis:
            self.test_enhancement_generation_live(analysis)
        
        # Test 5: Complex Dashboard
        self.test_real_world_ui()
        
        # Summary
        print("\n" + "=" * 80)
        print("  TEST SUITE COMPLETE")
        print("=" * 80)
        print(f"\n✓ All tests completed successfully!")
        print(f"  Total tests run: 5")
        print(f"  Analysis performed: {len(self.test_results)}")
        
        return True


def main():
    """Run live UI analysis tests"""
    
    try:
        tester = LiveUITester()
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ All systems operational!")
        else:
            print("\n⚠ Some tests failed. Check output above.")
            
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
