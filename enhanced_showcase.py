"""
Enhanced UI Showcase with Playwright Screenshots
High-quality demonstration system with comprehensive theme coverage
"""

import os
import time
from pathlib import Path
from complete_ui_generator import CompleteUIGenerator, CompleteUIRequest
from typing import List, Dict, Any
import json


# Expanded test scenarios with multiple themes and styles
ENHANCED_TEST_SCENARIOS = [
    # SaaS Landing Pages - Different Styles
    {
        "name": "SaaS Landing - Modern",
        "request": CompleteUIRequest(
            project_name="CloudFlow Pro",
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
        "description": "Modern SaaS product with sleek design and animations",
        "category": "SaaS"
    },
    {
        "name": "SaaS Landing - Minimal",
        "request": CompleteUIRequest(
            project_name="CleanCloud",
            project_type="landing_page",
            style="minimal",
            primary_color="#64748b",
            target_audience="businesses",
            key_features=["Simple Storage", "Fast Access", "Secure"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Minimal SaaS design with focus on content",
        "category": "SaaS"
    },
    {
        "name": "SaaS Landing - Bold",
        "request": CompleteUIRequest(
            project_name="PowerCloud",
            project_type="landing_page",
            style="bold",
            primary_color="#dc2626",
            target_audience="enterprises",
            key_features=["Enterprise", "Scalable", "Powerful", "Secure"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Bold SaaS design with strong visual impact",
        "category": "SaaS"
    },
    
    # E-commerce - Different Styles
    {
        "name": "E-commerce - Modern",
        "request": CompleteUIRequest(
            project_name="TechMart",
            project_type="ecommerce",
            style="modern",
            primary_color="#10b981",
            target_audience="consumers",
            key_features=["Products", "Cart", "Wishlist", "Reviews"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern e-commerce with smooth interactions",
        "category": "E-commerce"
    },
    {
        "name": "E-commerce - Classic",
        "request": CompleteUIRequest(
            project_name="RetailHub",
            project_type="ecommerce",
            style="classic",
            primary_color="#8b5cf6",
            target_audience="consumers",
            key_features=["Shop", "Deals", "Categories", "Checkout"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Classic e-commerce with traditional layout",
        "category": "E-commerce"
    },
    
    # Dashboards - Different Styles
    {
        "name": "Dashboard - Modern",
        "request": CompleteUIRequest(
            project_name="DataViz Pro",
            project_type="dashboard",
            style="modern",
            primary_color="#6366f1",
            target_audience="analysts",
            key_features=["Metrics", "Charts", "Analytics", "Reports"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern dashboard with data visualization",
        "category": "Dashboard"
    },
    {
        "name": "Dashboard - Minimal",
        "request": CompleteUIRequest(
            project_name="SimpleMetrics",
            project_type="dashboard",
            style="minimal",
            primary_color="#0ea5e9",
            target_audience="managers",
            key_features=["KPIs", "Trends", "Stats"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Minimal dashboard focused on key metrics",
        "category": "Dashboard"
    },
    
    # Portfolio - Different Styles
    {
        "name": "Portfolio - Modern",
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
        "description": "Modern creative portfolio with animations",
        "category": "Portfolio"
    },
    {
        "name": "Portfolio - Minimal",
        "request": CompleteUIRequest(
            project_name="MinimalDesign",
            project_type="landing_page",
            style="minimal",
            primary_color="#000000",
            target_audience="clients",
            key_features=["Work", "About", "Contact"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Minimal portfolio with clean aesthetics",
        "category": "Portfolio"
    },
    
    # Blog - Different Styles
    {
        "name": "Blog - Modern",
        "request": CompleteUIRequest(
            project_name="TechBlog",
            project_type="landing_page",
            style="modern",
            primary_color="#8b5cf6",
            target_audience="readers",
            key_features=["Articles", "Categories", "Search", "Subscribe"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern blog with engaging layout",
        "category": "Blog"
    },
    {
        "name": "Blog - Classic",
        "request": CompleteUIRequest(
            project_name="ClassicReads",
            project_type="landing_page",
            style="classic",
            primary_color="#ef4444",
            target_audience="readers",
            key_features=["Posts", "Archive", "Comments"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Classic blog with traditional reading experience",
        "category": "Blog"
    },
    
    # Fintech - Different Styles
    {
        "name": "Fintech - Modern",
        "request": CompleteUIRequest(
            project_name="WealthTracker",
            project_type="dashboard",
            style="modern",
            primary_color="#059669",
            target_audience="investors",
            key_features=["Balance", "Investments", "Goals", "Reports"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern fintech with real-time data",
        "category": "Fintech"
    },
    
    # Healthcare - Different Styles
    {
        "name": "Healthcare - Modern",
        "request": CompleteUIRequest(
            project_name="HealthConnect",
            project_type="landing_page",
            style="modern",
            primary_color="#06b6d4",
            target_audience="patients",
            key_features=["Appointments", "Records", "Doctors", "Telemedicine"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern healthcare portal with patient focus",
        "category": "Healthcare"
    },
    {
        "name": "Healthcare - Classic",
        "request": CompleteUIRequest(
            project_name="MedicalCare",
            project_type="landing_page",
            style="classic",
            primary_color="#0891b2",
            target_audience="patients",
            key_features=["Services", "Doctors", "Contact"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Classic healthcare with professional design",
        "category": "Healthcare"
    },
    
    # Real Estate - Different Styles
    {
        "name": "Real Estate - Modern",
        "request": CompleteUIRequest(
            project_name="PropertyFinder",
            project_type="ecommerce",
            style="modern",
            primary_color="#14b8a6",
            target_audience="buyers",
            key_features=["Listings", "Search", "Tours", "Agents"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Modern real estate with virtual tours",
        "category": "Real Estate"
    },
    
    # Education - Different Styles
    {
        "name": "Education - Modern",
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
        "description": "Modern education platform with engagement",
        "category": "Education"
    },
    {
        "name": "Education - Minimal",
        "request": CompleteUIRequest(
            project_name="SimpleLearn",
            project_type="landing_page",
            style="minimal",
            primary_color="#fb923c",
            target_audience="students",
            key_features=["Learn", "Practice", "Test"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Minimal education focused on learning",
        "category": "Education"
    },
    
    # Restaurant - Different Styles
    {
        "name": "Restaurant - Bold",
        "request": CompleteUIRequest(
            project_name="DeliciousEats",
            project_type="landing_page",
            style="bold",
            primary_color="#dc2626",
            target_audience="diners",
            key_features=["Menu", "Reservations", "Gallery", "Delivery"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        ),
        "description": "Bold restaurant with appetite appeal",
        "category": "Restaurant"
    },
    {
        "name": "Restaurant - Classic",
        "request": CompleteUIRequest(
            project_name="FineD ining",
            project_type="landing_page",
            style="classic",
            primary_color="#991b1b",
            target_audience="diners",
            key_features=["Menu", "Reserve", "About"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        ),
        "description": "Classic restaurant with elegant design",
        "category": "Restaurant"
    },
]


class EnhancedUIShowcase:
    """Enhanced showcase with playwright screenshots and comprehensive coverage"""
    
    def __init__(self, output_dir: str = "showcase_output", demos_dir: str = "demos"):
        """Initialize enhanced showcase"""
        self.output_dir = Path(output_dir)
        self.demos_dir = Path(demos_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.demos_dir.mkdir(exist_ok=True)
        self.generator = CompleteUIGenerator()
        self.results: List[Dict[str, Any]] = []
    
    def generate_all_scenarios(self) -> List[Dict[str, Any]]:
        """Generate UIs for all enhanced test scenarios"""
        
        print("=" * 80)
        print("  ENHANCED UI SHOWCASE - High Quality Generation")
        print("=" * 80)
        print(f"  Total Scenarios: {len(ENHANCED_TEST_SCENARIOS)}")
        print(f"  Output Directory: {self.output_dir}")
        print(f"  Demos Directory: {self.demos_dir}")
        print("=" * 80)
        print()
        
        for i, scenario in enumerate(ENHANCED_TEST_SCENARIOS, 1):
            print(f"\n[{i}/{len(ENHANCED_TEST_SCENARIOS)}] Generating: {scenario['name']}")
            print(f"    Category: {scenario['category']}")
            print(f"    Style: {scenario['request'].style}")
            print(f"    Description: {scenario['description']}")
            
            try:
                # Generate UI
                start_time = time.time()
                result = self.generator.generate_complete_ui(scenario['request'])
                generation_time = time.time() - start_time
                
                # Create output directory
                scenario_dir = self.output_dir / self._sanitize_filename(scenario['name'])
                scenario_dir.mkdir(exist_ok=True)
                
                # Save files
                html_path = scenario_dir / "index.html"
                css_path = scenario_dir / "styles.css"
                js_path = scenario_dir / "script.js"
                readme_path = scenario_dir / "README.md"
                
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
                    'category': scenario['category'],
                    'style': scenario['request'].style,
                    'description': scenario['description'],
                    'path': str(scenario_dir),
                    'html_path': str(html_path),
                    'components': result.components_used,
                    'patterns': result.patterns_applied,
                    'quality_metrics': result.quality_metrics,
                    'generation_time': generation_time,
                    'primary_color': scenario['request'].primary_color
                }
                self.results.append(scenario_result)
                
                print(f"    ✓ Generated in {generation_time:.3f}s")
                print(f"    ✓ Quality: {result.quality_metrics['overall']:.1%}")
                print(f"    ✓ Accessibility: {result.quality_metrics['accessibility']:.1%}")
                print(f"    ✓ Performance: {result.quality_metrics['performance']:.1%}")
                print(f"    ✓ Components: {len(result.components_used)}")
                
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                import traceback
                traceback.print_exc()
        
        return self.results
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename"""
        return name.lower().replace(' ', '_').replace('-', '_')
    
    def save_manifest(self):
        """Save comprehensive manifest"""
        
        manifest = {
            'total_scenarios': len(self.results),
            'categories': {},
            'styles': {},
            'scenarios': []
        }
        
        # Organize by category and style
        for result in self.results:
            category = result['category']
            style = result['style']
            
            if category not in manifest['categories']:
                manifest['categories'][category] = []
            manifest['categories'][category].append(result['name'])
            
            if style not in manifest['styles']:
                manifest['styles'][style] = []
            manifest['styles'][style].append(result['name'])
            
            manifest['scenarios'].append({
                'name': result['name'],
                'category': result['category'],
                'style': result['style'],
                'description': result['description'],
                'quality': result['quality_metrics']['overall'],
                'accessibility': result['quality_metrics']['accessibility'],
                'performance': result['quality_metrics']['performance'],
                'components': len(result['components']),
                'generation_time': result['generation_time']
            })
        
        # Save manifest
        manifest_path = self.output_dir / "enhanced_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n✓ Enhanced manifest saved: {manifest_path}")
        print(f"  Categories: {len(manifest['categories'])}")
        print(f"  Styles: {len(manifest['styles'])}")
        print(f"  Total Scenarios: {manifest['total_scenarios']}")
    
    def print_summary(self):
        """Print enhanced summary"""
        
        print("\n" + "=" * 80)
        print("  ENHANCED GENERATION COMPLETE")
        print("=" * 80)
        print()
        
        if self.results:
            # Overall stats
            avg_quality = sum(r['quality_metrics']['overall'] for r in self.results) / len(self.results)
            avg_accessibility = sum(r['quality_metrics']['accessibility'] for r in self.results) / len(self.results)
            avg_performance = sum(r['quality_metrics']['performance'] for r in self.results) / len(self.results)
            total_time = sum(r['generation_time'] for r in self.results)
            
            print(f"Total Scenarios: {len(self.results)}")
            print(f"Average Quality: {avg_quality:.1%}")
            print(f"Average Accessibility: {avg_accessibility:.1%}")
            print(f"Average Performance: {avg_performance:.1%}")
            print(f"Total Generation Time: {total_time:.2f}s")
            print()
            
            # By category
            categories = {}
            for r in self.results:
                cat = r['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(r)
            
            print("By Category:")
            for cat, items in sorted(categories.items()):
                print(f"  {cat}: {len(items)} scenarios")
            print()
            
            # By style
            styles = {}
            for r in self.results:
                style = r['style']
                if style not in styles:
                    styles[style] = []
                styles[style].append(r)
            
            print("By Style:")
            for style, items in sorted(styles.items()):
                print(f"  {style}: {len(items)} scenarios")
        
        print()
        print("=" * 80)


def main():
    """Run enhanced UI showcase"""
    
    showcase = EnhancedUIShowcase()
    showcase.generate_all_scenarios()
    showcase.save_manifest()
    showcase.print_summary()


if __name__ == "__main__":
    main()
