"""
Playwright Screenshot Utility for UI Testing and Documentation.
Phase 4: Performance Optimization + Visual Testing
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import json


class ScreenshotManager:
    """Manage screenshots and snapshots using Playwright."""

    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.metadata = []

    async def capture_page(
        self,
        url: str,
        name: str,
        full_page: bool = False,
        wait_time: int = 1000
    ) -> Dict[str, Any]:
        """Capture screenshot of a web page."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("Playwright not installed. Install with: pip install playwright && playwright install")
            return {"error": "Playwright not available"}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.output_dir / filename

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(wait_time)
                
                await page.screenshot(
                    path=str(filepath),
                    full_page=full_page,
                    type="png"
                )
                
                # Get page info
                title = await page.title()
                url_loaded = page.url
                
                metadata = {
                    "name": name,
                    "url": url,
                    "url_loaded": url_loaded,
                    "title": title,
                    "filename": filename,
                    "filepath": str(filepath),
                    "timestamp": timestamp,
                    "full_page": full_page,
                    "success": True
                }
                
                self.metadata.append(metadata)
                print(f"✓ Screenshot saved: {filepath}")
                return metadata
                
            except Exception as e:
                print(f"✗ Failed to capture {url}: {e}")
                return {"error": str(e), "success": False}
            finally:
                await browser.close()

    async def capture_multiple(
        self,
        urls: List[Dict[str, str]],
        full_page: bool = False
    ) -> List[Dict[str, Any]]:
        """Capture multiple screenshots."""
        results = []
        for item in urls:
            url = item.get("url")
            name = item.get("name", "screenshot")
            result = await self.capture_page(url, name, full_page)
            results.append(result)
            await asyncio.sleep(1)  # Rate limiting
        return results

    async def capture_api_docs(
        self,
        base_url: str = "http://localhost:8000"
    ) -> List[Dict[str, Any]]:
        """Capture screenshots of API documentation."""
        urls = [
            {"url": f"{base_url}/", "name": "api_root"},
            {"url": f"{base_url}/api/docs", "name": "api_swagger_ui"},
            {"url": f"{base_url}/api/redoc", "name": "api_redoc"},
            {"url": f"{base_url}/api/v1/health", "name": "api_health_json"},
        ]
        return await self.capture_multiple(urls, full_page=True)

    async def capture_ui_samples(
        self,
        generated_html_files: List[str]
    ) -> List[Dict[str, Any]]:
        """Capture screenshots of generated UI samples."""
        results = []
        for html_file in generated_html_files:
            if os.path.exists(html_file):
                file_url = f"file://{os.path.abspath(html_file)}"
                name = Path(html_file).stem
                result = await self.capture_page(file_url, name, full_page=True)
                results.append(result)
        return results

    def save_metadata(self, filename: str = "screenshot_metadata.json"):
        """Save screenshot metadata to JSON file."""
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"✓ Metadata saved: {filepath}")

    def generate_gallery_html(self, output_file: str = "gallery.html"):
        """Generate HTML gallery of screenshots."""
        filepath = self.output_dir / output_file
        
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screenshot Gallery</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .screenshot {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s;
        }
        .screenshot:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .screenshot img {
            width: 100%;
            height: auto;
            display: block;
        }
        .info {
            padding: 15px;
        }
        .info h3 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .info p {
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }
        .url {
            color: #0066cc;
            text-decoration: none;
            word-break: break-all;
        }
        .timestamp {
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>📸 Screenshot Gallery</h1>
    <div class="gallery">
"""
        
        for item in self.metadata:
            if item.get("success"):
                html_content += f"""
        <div class="screenshot">
            <img src="{item['filename']}" alt="{item['name']}">
            <div class="info">
                <h3>{item['name']}</h3>
                <p><strong>Title:</strong> {item.get('title', 'N/A')}</p>
                <p><strong>URL:</strong> <a class="url" href="{item['url']}" target="_blank">{item['url']}</a></p>
                <p class="timestamp">Captured: {item['timestamp']}</p>
            </div>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        print(f"✓ Gallery HTML generated: {filepath}")


async def main():
    """Main function to run screenshot examples."""
    manager = ScreenshotManager()
    
    print("\n=== Capturing API Documentation Screenshots ===\n")
    await manager.capture_api_docs()
    
    print("\n=== Saving Metadata ===\n")
    manager.save_metadata()
    
    print("\n=== Generating Gallery ===\n")
    manager.generate_gallery_html()
    
    print(f"\n✓ All screenshots saved to: {manager.output_dir}")
    print(f"✓ Open {manager.output_dir}/gallery.html to view gallery")


if __name__ == "__main__":
    asyncio.run(main())
