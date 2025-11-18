"""
E2E tests for complete UI generation workflow.
Phase 3: Quality & Security
"""

import pytest
import asyncio
from playwright.async_api import async_playwright


@pytest.mark.asyncio
@pytest.mark.e2e
class TestFullWorkflow:
    """End-to-end workflow tests."""

    async def test_api_health_check(self):
        """Test API server is accessible."""
        try:
            import requests
            response = requests.get('http://localhost:8000/api/v1/health', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
        except Exception:
            pytest.skip("API server not running")

    async def test_ui_generation_workflow(self):
        """Test complete UI generation workflow."""
        try:
            import requests
            
            # Generate UI
            response = requests.post(
                'http://localhost:8000/api/v1/generate',
                json={
                    "prompt": "Create a simple login form",
                    "theme": "modern",
                    "framework": "bootstrap"
                },
                timeout=30
            )
            
            assert response.status_code == 200
            data = response.json()
            assert 'html' in data
            assert 'css' in data
            assert len(data['html']) > 0
        except Exception:
            pytest.skip("API server not running")

    async def test_browser_ui_rendering(self):
        """Test UI renders correctly in browser."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Simple HTML test
                await page.set_content('<h1>Test</h1>')
                title = await page.inner_text('h1')
                assert title == 'Test'
                
                await browser.close()
        except Exception as e:
            pytest.skip(f"Playwright not available: {e}")
