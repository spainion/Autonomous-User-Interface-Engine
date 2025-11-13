"""
UI Showcase Demo
Generates complete UIs for various niches and displays them in a browser
"""

import os
import time
from pathlib import Path
from complete_ui_generator import CompleteUIGenerator, CompleteUIRequest
from typing import List, Dict, Any


# Define test scenarios for various niches
TEST_SCENARIOS = [
    {
        "name": "SaaS Landing Page",
        "request": CompleteUIRequest(
            project_name="CloudFlow",
            project_type="landing_page",
            style="modern",
            primary_color="#3b82f6",
            target_audience="businesses",
            key_features=["Cloud Storage", "Team Collaboration", "Security", "Analytics"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern SaaS product landing page with hero, features, and pricing"
    },
    {
        "name": "E-commerce Store",
        "request": CompleteUIRequest(
            project_name="TechShop",
            project_type="ecommerce",
            style="modern",
            primary_color="#10b981",
            target_audience="consumers",
            key_features=["Product Grid", "Shopping Cart", "Checkout", "Reviews"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "E-commerce platform with product listings and shopping features"
    },
    {
        "name": "Analytics Dashboard",
        "request": CompleteUIRequest(
            project_name="DataViz Pro",
            project_type="dashboard",
            style="minimal",
            primary_color="#6366f1",
            target_audience="analysts",
            key_features=["Metrics", "Charts", "Tables", "Reports"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Analytics dashboard with data visualization and metrics"
    },
    {
        "name": "Portfolio Website",
        "request": CompleteUIRequest(
            project_name="CreativeStudio",
            project_type="landing_page",
            style="modern",
            primary_color="#f59e0b",
            target_audience="clients",
            key_features=["Portfolio", "About", "Services", "Contact"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Creative portfolio website for designers and developers"
    },
    {
        "name": "Blog Platform",
        "request": CompleteUIRequest(
            project_name="TechBlog",
            project_type="landing_page",
            style="classic",
            primary_color="#ef4444",
            target_audience="readers",
            key_features=["Articles", "Categories", "Comments", "Newsletter"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Blog platform with article listings and reading experience"
    },
    {
        "name": "Fintech App",
        "request": CompleteUIRequest(
            project_name="WealthTracker",
            project_type="dashboard",
            style="minimal",
            primary_color="#8b5cf6",
            target_audience="investors",
            key_features=["Balance", "Transactions", "Investments", "Goals"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Financial dashboard for tracking investments and transactions"
    },
    {
        "name": "Healthcare Portal",
        "request": CompleteUIRequest(
            project_name="HealthConnect",
            project_type="landing_page",
            style="modern",
            primary_color="#06b6d4",
            target_audience="patients",
            key_features=["Appointments", "Records", "Doctors", "Prescriptions"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Healthcare portal for patients and medical professionals"
    },
    {
        "name": "Real Estate Platform",
        "request": CompleteUIRequest(
            project_name="PropertyFinder",
            project_type="ecommerce",
            style="modern",
            primary_color="#14b8a6",
            target_audience="homebuyers",
            key_features=["Listings", "Search", "Map View", "Virtual Tours"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Real estate platform with property listings and search"
    },
    {
        "name": "Education Platform",
        "request": CompleteUIRequest(
            project_name="LearnHub",
            project_type="landing_page",
            style="modern",
            primary_color="#f97316",
            target_audience="students",
            key_features=["Courses", "Progress", "Certificates", "Community"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Online learning platform with courses and progress tracking"
    },
    {
        "name": "Restaurant Website",
        "request": CompleteUIRequest(
            project_name="DeliciousEats",
            project_type="landing_page",
            style="bold",
            primary_color="#dc2626",
            target_audience="diners",
            key_features=["Menu", "Reservations", "Gallery", "Reviews"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Restaurant website with menu and online reservations"
    }
]


class UIShowcaseDemo:
    """Generate and showcase UIs for various niches"""
    
    def __init__(self, output_dir: str = "showcase_output"):
        """Initialize the showcase demo"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.generator = CompleteUIGenerator()
        self.results: List[Dict[str, Any]] = []
    
    def generate_all_scenarios(self) -> List[Dict[str, Any]]:
        """Generate UIs for all test scenarios"""
        
        print("=" * 80)
        print("  UI SHOWCASE DEMO - Generating UIs for Multiple Niches")
        print("=" * 80)
        print()
        
        for i, scenario in enumerate(TEST_SCENARIOS, 1):
            print(f"\n[{i}/{len(TEST_SCENARIOS)}] Generating: {scenario['name']}")
            print(f"    Description: {scenario['description']}")
            
            try:
                # Generate UI
                start_time = time.time()
                result = self.generator.generate_complete_ui(scenario['request'])
                generation_time = time.time() - start_time
                
                # Create output directory for this scenario
                scenario_dir = self.output_dir / self._sanitize_filename(scenario['name'])
                scenario_dir.mkdir(exist_ok=True)
                
                # Save HTML, CSS, JS
                html_path = scenario_dir / "index.html"
                css_path = scenario_dir / "styles.css"
                js_path = scenario_dir / "script.js"
                readme_path = scenario_dir / "README.md"
                
                # Write files
                with open(html_path, 'w') as f:
                    f.write(result.html)
                
                with open(css_path, 'w') as f:
                    f.write(result.css)
                
                with open(js_path, 'w') as f:
                    f.write(result.javascript)
                
                with open(readme_path, 'w') as f:
                    f.write(result.documentation)
                
                # Store results
                scenario_result = {
                    'name': scenario['name'],
                    'description': scenario['description'],
                    'path': str(scenario_dir),
                    'html_path': str(html_path),
                    'components': result.components_used,
                    'patterns': result.patterns_applied,
                    'quality_metrics': result.quality_metrics,
                    'generation_time': generation_time
                }
                self.results.append(scenario_result)
                
                print(f"    ✓ Generated in {generation_time:.2f}s")
                print(f"    ✓ Quality: {result.quality_metrics['overall']:.1%}")
                print(f"    ✓ Components: {len(result.components_used)}")
                print(f"    ✓ Saved to: {scenario_dir}")
                
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                import traceback
                traceback.print_exc()
        
        return self.results
    
    def generate_index_page(self):
        """Generate an index page showcasing all UIs"""
        
        print("\n" + "=" * 80)
        print("  Generating Showcase Index Page")
        print("=" * 80)
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Showcase - Generated Interfaces</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        header {
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 3px solid #667eea;
        }
        
        h1 {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.25rem;
            color: #64748b;
            margin-top: 0.5rem;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .stat-label {
            font-size: 0.875rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .showcase-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .showcase-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .showcase-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .card-description {
            font-size: 0.875rem;
            opacity: 0.95;
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .metric-row:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            font-size: 0.875rem;
            color: #64748b;
            font-weight: 500;
        }
        
        .metric-value {
            font-weight: 600;
            color: #1e293b;
        }
        
        .quality-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .quality-excellent {
            background: #dcfce7;
            color: #166534;
        }
        
        .quality-good {
            background: #dbeafe;
            color: #1e40af;
        }
        
        .card-actions {
            padding: 1rem 1.5rem;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
        }
        
        .btn {
            display: inline-block;
            width: 100%;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .components-list {
            margin-top: 1rem;
        }
        
        .component-tag {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background: #f1f5f9;
            color: #475569;
            border-radius: 6px;
            font-size: 0.75rem;
            margin: 0.25rem;
        }
        
        footer {
            text-align: center;
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 2px solid #e2e8f0;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 UI Showcase</h1>
            <p class="subtitle">Generated Interfaces for Multiple Niches</p>
        </header>
        
        <div class="stats">
"""
        
        # Calculate statistics
        total_scenarios = len(self.results)
        avg_quality = sum(r['quality_metrics']['overall'] for r in self.results) / len(self.results) if self.results else 0
        total_components = sum(len(r['components']) for r in self.results)
        avg_time = sum(r['generation_time'] for r in self.results) / len(self.results) if self.results else 0
        
        html += f"""
            <div class="stat-card">
                <div class="stat-value">{total_scenarios}</div>
                <div class="stat-label">Scenarios</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_quality:.1%}</div>
                <div class="stat-label">Avg Quality</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_components}</div>
                <div class="stat-label">Components</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_time:.2f}s</div>
                <div class="stat-label">Avg Gen Time</div>
            </div>
        </div>
        
        <div class="showcase-grid">
"""
        
        # Add cards for each scenario
        for result in self.results:
            quality = result['quality_metrics']['overall']
            quality_class = 'quality-excellent' if quality >= 0.90 else 'quality-good'
            
            html += f"""
            <div class="showcase-card">
                <div class="card-header">
                    <h2 class="card-title">{result['name']}</h2>
                    <p class="card-description">{result['description']}</p>
                </div>
                
                <div class="card-body">
                    <div class="metric-row">
                        <span class="metric-label">Quality Score</span>
                        <span class="quality-badge {quality_class}">{quality:.1%}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Accessibility</span>
                        <span class="metric-value">{result['quality_metrics']['accessibility']:.1%}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Performance</span>
                        <span class="metric-value">{result['quality_metrics']['performance']:.1%}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Components</span>
                        <span class="metric-value">{len(result['components'])}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Generation Time</span>
                        <span class="metric-value">{result['generation_time']:.2f}s</span>
                    </div>
                    
                    <div class="components-list">
"""
            
            # Add component tags
            for component in result['components'][:5]:  # Show first 5
                html += f'                        <span class="component-tag">{component}</span>\n'
            
            if len(result['components']) > 5:
                html += f'                        <span class="component-tag">+{len(result["components"]) - 5} more</span>\n'
            
            # Get relative path for the link
            rel_path = Path(result['path']).relative_to(self.output_dir)
            
            html += f"""
                    </div>
                </div>
                
                <div class="card-actions">
                    <a href="{rel_path}/index.html" class="btn" target="_blank">View UI →</a>
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <footer>
            <p><strong>Generated by Autonomous User Interface Engine</strong></p>
            <p>All UIs are production-ready, accessible, and responsive</p>
        </footer>
    </div>
</body>
</html>
"""
        
        # Save index page
        index_path = self.output_dir / "index.html"
        with open(index_path, 'w') as f:
            f.write(html)
        
        print(f"✓ Index page saved to: {index_path}")
        return index_path
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename for directory name"""
        return name.lower().replace(' ', '_').replace('-', '_')
    
    def print_summary(self):
        """Print summary of all generated UIs"""
        
        print("\n" + "=" * 80)
        print("  GENERATION COMPLETE - SUMMARY")
        print("=" * 80)
        print()
        
        print(f"Total Scenarios: {len(self.results)}")
        print(f"Output Directory: {self.output_dir.absolute()}")
        print()
        
        if self.results:
            avg_quality = sum(r['quality_metrics']['overall'] for r in self.results) / len(self.results)
            avg_accessibility = sum(r['quality_metrics']['accessibility'] for r in self.results) / len(self.results)
            avg_performance = sum(r['quality_metrics']['performance'] for r in self.results) / len(self.results)
            total_time = sum(r['generation_time'] for r in self.results)
            
            print("Average Metrics:")
            print(f"  Overall Quality: {avg_quality:.1%}")
            print(f"  Accessibility:   {avg_accessibility:.1%}")
            print(f"  Performance:     {avg_performance:.1%}")
            print(f"  Total Time:      {total_time:.2f}s")
            print()
        
        print("Generated UIs:")
        for i, result in enumerate(self.results, 1):
            print(f"  {i}. {result['name']}")
            print(f"     Quality: {result['quality_metrics']['overall']:.1%} | "
                  f"Components: {len(result['components'])} | "
                  f"Time: {result['generation_time']:.2f}s")
        
        print()
        print("=" * 80)
        print(f"  Open {self.output_dir}/index.html in a browser to view all UIs")
        print("=" * 80)


def main():
    """Run the UI showcase demo"""
    
    # Create showcase
    showcase = UIShowcaseDemo(output_dir="showcase_output")
    
    # Generate all scenarios
    showcase.generate_all_scenarios()
    
    # Generate index page
    showcase.generate_index_page()
    
    # Print summary
    showcase.print_summary()


if __name__ == "__main__":
    main()
