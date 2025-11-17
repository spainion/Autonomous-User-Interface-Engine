"""
Playwright UI Previewer
Demonstrates the autonomous UI engine's ability to interpret plain language
and generate beautiful, usable user interfaces with live browser previews.
"""

import os
import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any
from playwright.async_api import async_playwright
from complete_ui_generator import CompleteUIGenerator, CompleteUIRequest
import json


# Plain language UI requests - demonstrating natural language interpretation
PLAIN_LANGUAGE_REQUESTS = [
    {
        "plain_language": "Create a modern SaaS landing page for a cloud storage product with a professional blue theme",
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
        )
    },
    {
        "plain_language": "Build a minimal e-commerce store for tech products with a clean green design",
        "request": CompleteUIRequest(
            project_name="TechMart",
            project_type="ecommerce",
            style="minimal",
            primary_color="#10b981",
            target_audience="consumers",
            key_features=["Products", "Cart", "Wishlist", "Reviews"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        )
    },
    {
        "plain_language": "Design a bold analytics dashboard with data visualization in purple",
        "request": CompleteUIRequest(
            project_name="DataViz Pro",
            project_type="dashboard",
            style="bold",
            primary_color="#8b5cf6",
            target_audience="analysts",
            key_features=["Metrics", "Charts", "Analytics", "Reports"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        )
    },
    {
        "plain_language": "Create a modern creative portfolio website with orange accents and animations",
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
        )
    },
    {
        "plain_language": "Build a classic restaurant website with bold red design and menu showcase",
        "request": CompleteUIRequest(
            project_name="DeliciousEats",
            project_type="landing_page",
            style="classic",
            primary_color="#dc2626",
            target_audience="diners",
            key_features=["Menu", "Reservations", "Gallery", "Delivery"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=False
        )
    },
    {
        "plain_language": "Design a modern fintech app for wealth tracking with professional green theme",
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
        )
    },
    {
        "plain_language": "Create a minimal education platform with orange theme focused on learning",
        "request": CompleteUIRequest(
            project_name="LearnHub",
            project_type="landing_page",
            style="minimal",
            primary_color="#f97316",
            target_audience="students",
            key_features=["Courses", "Progress", "Certificates", "Community"],
            framework="custom",
            responsive=True,
            accessibility=True,
            animations=True
        )
    },
    {
        "plain_language": "Build a modern healthcare portal with cyan theme and patient-focused design",
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
        )
    }
]


class PlaywrightUIPreviewer:
    """Preview and capture screenshots of generated UIs using Playwright"""
    
    def __init__(self, output_dir: str = "playwright_previews"):
        """Initialize the previewer"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots_dir = self.output_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        self.html_dir = self.output_dir / "generated_html"
        self.html_dir.mkdir(exist_ok=True)
        self.generator = CompleteUIGenerator()
        self.results: List[Dict[str, Any]] = []
    
    def generate_ui_from_plain_language(self, plain_language: str, request: CompleteUIRequest) -> Dict[str, Any]:
        """Generate UI from plain language description"""
        print(f"\n{'='*80}")
        print(f"Plain Language: {plain_language}")
        print(f"{'='*80}")
        
        start_time = time.time()
        result = self.generator.generate_complete_ui(request)
        generation_time = time.time() - start_time
        
        # Save HTML file
        safe_name = self._sanitize_filename(request.project_name)
        html_path = self.html_dir / f"{safe_name}.html"
        
        # Create complete HTML with embedded CSS and JS
        complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{request.project_name}</title>
    <style>
{result.css}
    </style>
</head>
<body>
{result.html}
    <script>
{result.javascript}
    </script>
</body>
</html>"""
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(complete_html)
        
        print(f"✓ Generated in {generation_time:.3f}s")
        print(f"✓ Quality: {result.quality_metrics['overall']:.1%}")
        print(f"✓ Components: {len(result.components_used)}")
        print(f"✓ Saved to: {html_path}")
        
        return {
            'plain_language': plain_language,
            'project_name': request.project_name,
            'html_path': str(html_path),
            'generation_time': generation_time,
            'quality_metrics': result.quality_metrics,
            'components': result.components_used,
            'style': request.style,
            'type': request.project_type
        }
    
    async def capture_screenshot(self, html_path: str, screenshot_path: str, width: int = 1920, height: int = 1080):
        """Capture screenshot of generated UI using Playwright"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': width, 'height': height})
            
            # Load the HTML file
            await page.goto(f'file://{os.path.abspath(html_path)}')
            
            # Wait for any animations or dynamic content
            await page.wait_for_timeout(1000)
            
            # Take screenshot
            await page.screenshot(path=screenshot_path, full_page=True)
            
            await browser.close()
    
    async def preview_and_capture_all(self):
        """Generate UIs and capture screenshots for all plain language requests"""
        print("\n" + "="*80)
        print("  PLAYWRIGHT UI PREVIEWER")
        print("  Demonstrating Plain Language to Beautiful UI")
        print("="*80)
        print(f"Total Requests: {len(PLAIN_LANGUAGE_REQUESTS)}")
        print(f"Output Directory: {self.output_dir}")
        print("="*80)
        
        for i, item in enumerate(PLAIN_LANGUAGE_REQUESTS, 1):
            print(f"\n[{i}/{len(PLAIN_LANGUAGE_REQUESTS)}] Processing...")
            
            # Generate UI
            result = self.generate_ui_from_plain_language(
                item['plain_language'],
                item['request']
            )
            
            # Capture screenshot
            safe_name = self._sanitize_filename(result['project_name'])
            screenshot_path = self.screenshots_dir / f"{safe_name}.png"
            
            print(f"📸 Capturing screenshot...")
            await self.capture_screenshot(result['html_path'], str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            result['screenshot_path'] = str(screenshot_path)
            self.results.append(result)
        
        # Generate gallery
        self.generate_gallery()
        
        # Save manifest
        self.save_manifest()
        
        # Print summary
        self.print_summary()
    
    def generate_gallery(self):
        """Generate an interactive gallery HTML page"""
        gallery_items = []
        
        for result in self.results:
            safe_name = self._sanitize_filename(result['project_name'])
            gallery_items.append(f"""
                <div class="gallery-item">
                    <div class="gallery-item-header">
                        <h3>{result['project_name']}</h3>
                        <span class="badge badge-{result['style']}">{result['style']}</span>
                        <span class="badge badge-{result['type']}">{result['type']}</span>
                    </div>
                    <div class="plain-language">
                        <strong>Plain Language Input:</strong>
                        <p>"{result['plain_language']}"</p>
                    </div>
                    <div class="screenshot-container">
                        <img src="screenshots/{safe_name}.png" alt="{result['project_name']}" loading="lazy">
                    </div>
                    <div class="gallery-item-footer">
                        <div class="metrics">
                            <span class="metric">Quality: {result['quality_metrics']['overall']:.1%}</span>
                            <span class="metric">Generated in: {result['generation_time']:.3f}s</span>
                            <span class="metric">Components: {len(result['components'])}</span>
                        </div>
                        <div class="actions">
                            <a href="generated_html/{safe_name}.html" target="_blank" class="btn">View Live</a>
                        </div>
                    </div>
                </div>
            """)
        
        gallery_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autonomous UI Engine - Playwright Preview Gallery</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }}
        
        header h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }}
        
        .stat {{
            background: white;
            padding: 1.5rem 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(600px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        .gallery-item {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .gallery-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .gallery-item-header {{
            padding: 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .gallery-item-header h3 {{
            flex: 1;
            font-size: 1.5rem;
        }}
        
        .badge {{
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(255,255,255,0.2);
        }}
        
        .plain-language {{
            padding: 1.5rem;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
        }}
        
        .plain-language strong {{
            color: #667eea;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .plain-language p {{
            font-style: italic;
            color: #555;
            line-height: 1.6;
        }}
        
        .screenshot-container {{
            width: 100%;
            overflow: hidden;
            background: #f0f0f0;
        }}
        
        .screenshot-container img {{
            width: 100%;
            display: block;
            transition: transform 0.3s ease;
        }}
        
        .gallery-item:hover .screenshot-container img {{
            transform: scale(1.05);
        }}
        
        .gallery-item-footer {{
            padding: 1.5rem;
        }}
        
        .metrics {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }}
        
        .metric {{
            padding: 0.5rem 1rem;
            background: #e9ecef;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .actions {{
            display: flex;
            gap: 1rem;
        }}
        
        .btn {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }}
        
        .btn:hover {{
            transform: scale(1.05);
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 4rem;
            padding: 2rem;
            opacity: 0.9;
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 Autonomous UI Engine</h1>
            <p>Plain Language → Beautiful User Interfaces</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem;">Demonstrating AI-powered UI generation with Playwright previews</p>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(self.results)}</div>
                <div class="stat-label">Generated UIs</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(r['generation_time'] for r in self.results):.2f}s</div>
                <div class="stat-label">Total Generation Time</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(r['quality_metrics']['overall'] for r in self.results) / len(self.results):.1%}</div>
                <div class="stat-label">Average Quality</div>
            </div>
        </div>
        
        <div class="gallery">
            {''.join(gallery_items)}
        </div>
        
        <footer>
            <p>Generated by the Autonomous User Interface Engine</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                All UIs were generated from plain language descriptions using AI and Playwright for previews
            </p>
        </footer>
    </div>
</body>
</html>"""
        
        gallery_path = self.output_dir / "index.html"
        with open(gallery_path, 'w', encoding='utf-8') as f:
            f.write(gallery_html)
        
        print(f"\n✓ Gallery created: {gallery_path}")
    
    def save_manifest(self):
        """Save manifest with all results"""
        manifest = {
            'total_uis': len(self.results),
            'generation_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'average_quality': sum(r['quality_metrics']['overall'] for r in self.results) / len(self.results),
            'total_time': sum(r['generation_time'] for r in self.results),
            'uis': self.results
        }
        
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✓ Manifest saved: {manifest_path}")
    
    def print_summary(self):
        """Print summary of results"""
        print("\n" + "="*80)
        print("  GENERATION COMPLETE")
        print("="*80)
        print(f"\nTotal UIs Generated: {len(self.results)}")
        print(f"Average Quality: {sum(r['quality_metrics']['overall'] for r in self.results) / len(self.results):.1%}")
        print(f"Total Generation Time: {sum(r['generation_time'] for r in self.results):.2f}s")
        print(f"\nOutput Directory: {self.output_dir}")
        print(f"Gallery: {self.output_dir / 'index.html'}")
        print("\n" + "="*80)
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename"""
        return name.lower().replace(' ', '_').replace('-', '_')


async def main():
    """Main function"""
    previewer = PlaywrightUIPreviewer()
    await previewer.preview_and_capture_all()
    
    print("\n🎉 Done! Open the gallery in your browser:")
    print(f"   file://{os.path.abspath(previewer.output_dir / 'index.html')}")


if __name__ == "__main__":
    asyncio.run(main())
