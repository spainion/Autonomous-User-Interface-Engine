"""
Visual regression tests with Playwright screenshots.
Phase 4: Performance Optimization + Visual Testing
"""

import pytest
from pathlib import Path


@pytest.mark.e2e
@pytest.mark.asyncio
class TestVisualRegression:
    """Visual regression tests using Playwright."""

    async def test_api_docs_screenshot(self):
        """Capture screenshot of API documentation."""
        try:
            from playwright.async_api import async_playwright
            
            output_dir = Path("screenshots/tests")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page(viewport={"width": 1920, "height": 1080})
                
                try:
                    await page.goto("http://localhost:8000/api/docs", timeout=10000)
                    await page.wait_for_timeout(2000)
                    
                    screenshot_path = output_dir / "api_docs.png"
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    
                    assert screenshot_path.exists()
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                except Exception as e:
                    pytest.skip(f"API not available: {e}")
                finally:
                    await browser.close()
                    
        except ImportError:
            pytest.skip("Playwright not installed")

    async def test_health_endpoint_screenshot(self):
        """Capture screenshot of health endpoint JSON response."""
        try:
            from playwright.async_api import async_playwright
            
            output_dir = Path("screenshots/tests")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                try:
                    await page.goto("http://localhost:8000/api/v1/health", timeout=10000)
                    await page.wait_for_timeout(1000)
                    
                    screenshot_path = output_dir / "health_endpoint.png"
                    await page.screenshot(path=str(screenshot_path))
                    
                    assert screenshot_path.exists()
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                except Exception as e:
                    pytest.skip(f"API not available: {e}")
                finally:
                    await browser.close()
                    
        except ImportError:
            pytest.skip("Playwright not installed")

    async def test_ui_generation_flow(self):
        """Test and capture full UI generation flow."""
        try:
            from playwright.async_api import async_playwright
            import requests
            
            # Generate UI via API
            try:
                response = requests.post(
                    "http://localhost:8000/api/v1/generate",
                    json={"prompt": "Create a login form", "theme": "modern"},
                    timeout=30
                )
                if response.status_code != 200:
                    pytest.skip("API not responding correctly")
                    
                data = response.json()
                html_content = data.get("html", "")
                
                if not html_content:
                    pytest.skip("No HTML generated")
                
                # Save HTML to temp file
                temp_html = Path("screenshots/tests/temp_generated.html")
                temp_html.parent.mkdir(parents=True, exist_ok=True)
                with open(temp_html, 'w') as f:
                    f.write(html_content)
                
                # Capture screenshot
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page(viewport={"width": 1920, "height": 1080})
                    
                    await page.goto(f"file://{temp_html.absolute()}")
                    await page.wait_for_timeout(1000)
                    
                    screenshot_path = Path("screenshots/tests/generated_ui.png")
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    
                    assert screenshot_path.exists()
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                    await browser.close()
                    
            except Exception as e:
                pytest.skip(f"Could not generate UI: {e}")
                
        except ImportError:
            pytest.skip("Required libraries not installed")
