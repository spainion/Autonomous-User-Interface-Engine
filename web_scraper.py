"""
Web Scraping System for UI Design Research
Extracts CSS, HTML, components, and design patterns from live websites
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
import re
import json
from urllib.parse import urljoin, urlparse

class WebScraper:
    """Web scraper for design pattern extraction"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_site(self, url: str, extract_css: bool = True, 
                   extract_components: bool = True, 
                   analyze_layout: bool = True) -> Dict:
        """
        Scrape and analyze a website
        
        Args:
            url: Website URL
            extract_css: Extract CSS styles
            extract_components: Extract UI components
            analyze_layout: Analyze page layout
            
        Returns:
            Dictionary with extracted data
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            result = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'success': True
            }
            
            if extract_css:
                result['css'] = self._extract_css(soup, url)
            
            if extract_components:
                result['components'] = self._extract_components(soup)
            
            if analyze_layout:
                result['layout'] = self._analyze_layout(soup)
            
            result['responsive'] = self._detect_responsive(soup)
            result['frameworks'] = self._detect_frameworks(soup)
            
            return result
            
        except Exception as e:
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }
    
    def _extract_css(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extract CSS from page"""
        css_data = {
            'inline_styles': [],
            'stylesheets': [],
            'computed_styles': {}
        }
        
        # Extract inline styles
        for tag in soup.find_all(style=True):
            css_data['inline_styles'].append({
                'tag': tag.name,
                'style': tag['style']
            })
        
        # Extract stylesheet links
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_data['stylesheets'].append(urljoin(base_url, href))
        
        # Extract style tags
        for style_tag in soup.find_all('style'):
            css_data['inline_styles'].append({
                'tag': 'style',
                'content': style_tag.string
            })
        
        return css_data
    
    def _extract_components(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract UI components"""
        components = []
        
        # Buttons
        for btn in soup.find_all(['button', 'a'], class_=re.compile(r'btn|button', re.I)):
            components.append({
                'type': 'button',
                'classes': btn.get('class', []),
                'text': btn.get_text(strip=True)
            })
        
        # Forms
        for form in soup.find_all('form'):
            components.append({
                'type': 'form',
                'action': form.get('action'),
                'method': form.get('method'),
                'inputs': len(form.find_all(['input', 'textarea', 'select']))
            })
        
        # Navigation
        for nav in soup.find_all('nav'):
            components.append({
                'type': 'navigation',
                'classes': nav.get('class', []),
                'links': len(nav.find_all('a'))
            })
        
        # Cards
        for card in soup.find_all(class_=re.compile(r'card', re.I)):
            components.append({
                'type': 'card',
                'classes': card.get('class', [])
            })
        
        return components
    
    def _analyze_layout(self, soup: BeautifulSoup) -> Dict:
        """Analyze page layout"""
        layout = {
            'structure': 'unknown',
            'grid_detected': False,
            'flexbox_detected': False,
            'sections': []
        }
        
        # Detect main sections
        for section in soup.find_all(['section', 'div'], class_=re.compile(r'container|section|main', re.I)):
            layout['sections'].append({
                'tag': section.name,
                'classes': section.get('class', [])
            })
        
        # Detect grid/flexbox
        style_text = str(soup)
        if 'display: grid' in style_text or 'grid-template' in style_text:
            layout['grid_detected'] = True
        if 'display: flex' in style_text or 'flexbox' in style_text:
            layout['flexbox_detected'] = True
        
        return layout
    
    def _detect_responsive(self, soup: BeautifulSoup) -> Dict:
        """Detect responsive design features"""
        responsive = {
            'viewport_meta': False,
            'media_queries': False,
            'breakpoints': []
        }
        
        # Check viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            responsive['viewport_meta'] = True
        
        # Check for media queries in style tags
        for style in soup.find_all('style'):
            if style.string and '@media' in style.string:
                responsive['media_queries'] = True
                # Extract breakpoints
                breakpoints = re.findall(r'@media.*?(\d+)px', style.string)
                responsive['breakpoints'].extend(breakpoints)
        
        return responsive
    
    def _detect_frameworks(self, soup: BeautifulSoup) -> List[str]:
        """Detect CSS/JS frameworks"""
        frameworks = []
        
        # Check for Bootstrap
        if soup.find('link', href=re.compile(r'bootstrap', re.I)):
            frameworks.append('bootstrap')
        if soup.find(class_=re.compile(r'btn-primary|container|row|col-', re.I)):
            frameworks.append('bootstrap')
        
        # Check for Tailwind
        if 'tailwindcss' in str(soup):
            frameworks.append('tailwind')
        
        # Check for Material-UI
        if soup.find(class_=re.compile(r'MuiButton|MuiPaper', re.I)):
            frameworks.append('material-ui')
        
        return list(set(frameworks))
    
    def scrape_multiple(self, urls: List[str], parallel: bool = True) -> List[Dict]:
        """Scrape multiple sites"""
        results = []
        for url in urls:
            result = self.scrape_site(url)
            results.append(result)
        return results
    
    def extract_color_palette(self, url: str) -> List[str]:
        """Extract color palette from site"""
        try:
            result = self.scrape_site(url, extract_css=True)
            colors = []
            
            # Extract colors from CSS
            if 'css' in result:
                for style_item in result['css'].get('inline_styles', []):
                    style = str(style_item.get('style', ''))
                    # Find hex colors
                    hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', style)
                    colors.extend(hex_colors)
                    # Find rgb colors
                    rgb_colors = re.findall(r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', style)
                    colors.extend(rgb_colors)
            
            return list(set(colors))[:10]  # Return top 10 unique colors
            
        except Exception:
            return []
    
    def extract_typography(self, url: str) -> Dict:
        """Extract typography information"""
        try:
            result = self.scrape_site(url, extract_css=True)
            typography = {
                'fonts': [],
                'sizes': [],
                'weights': []
            }
            
            if 'css' in result:
                for style_item in result['css'].get('inline_styles', []):
                    style = str(style_item.get('style', ''))
                    # Extract font families
                    fonts = re.findall(r'font-family:\s*([^;]+)', style)
                    typography['fonts'].extend(fonts)
                    # Extract font sizes
                    sizes = re.findall(r'font-size:\s*(\d+(?:\.\d+)?(?:px|em|rem))', style)
                    typography['sizes'].extend(sizes)
                    # Extract font weights
                    weights = re.findall(r'font-weight:\s*(\d+|bold|normal)', style)
                    typography['weights'].extend(weights)
            
            # Deduplicate
            typography['fonts'] = list(set(typography['fonts']))[:5]
            typography['sizes'] = list(set(typography['sizes']))[:10]
            typography['weights'] = list(set(typography['weights']))
            
            return typography
            
        except Exception:
            return {'fonts': [], 'sizes': [], 'weights': []}
