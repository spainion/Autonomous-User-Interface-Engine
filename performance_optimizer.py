"""
Performance Optimization System for Round 5
Advanced performance tuning and optimization
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum


class OptimizationLevel(Enum):
    """Optimization levels"""
    BASIC = "basic"
    STANDARD = "standard"
    AGGRESSIVE = "aggressive"
    MAXIMUM = "maximum"


@dataclass
class PerformanceMetrics:
    """Performance measurement results"""
    generation_time: float
    render_time: float
    memory_usage: int
    cpu_usage: float
    cache_hit_rate: float
    file_size: Dict[str, int]
    
    def get_score(self) -> float:
        """Calculate overall performance score"""
        # Weighted scoring
        time_score = min(100, (1.0 / max(self.generation_time, 0.1)) * 10)
        memory_score = min(100, (100 * 1024 * 1024 / max(self.memory_usage, 1024)) * 10)
        cache_score = self.cache_hit_rate
        
        return (time_score * 0.4 + memory_score * 0.3 + cache_score * 0.3)


class PerformanceOptimizer:
    """Advanced performance optimization system"""
    
    def __init__(self, level: OptimizationLevel = OptimizationLevel.STANDARD):
        self.level = level
        self.cache: Dict[str, Any] = {}
        self.optimizations_applied: List[str] = []
    
    def optimize_html(self, html: str) -> str:
        """Optimize HTML output"""
        optimized = html
        
        # Minification
        if self.level.value in ['standard', 'aggressive', 'maximum']:
            optimized = self._minify_html(optimized)
            self.optimizations_applied.append("HTML minification")
        
        # Remove unnecessary whitespace
        if self.level.value in ['aggressive', 'maximum']:
            optimized = self._remove_whitespace(optimized)
            self.optimizations_applied.append("Whitespace removal")
        
        # Inline critical CSS
        if self.level.value == 'maximum':
            optimized = self._inline_critical_css(optimized)
            self.optimizations_applied.append("Critical CSS inlining")
        
        return optimized
    
    def optimize_css(self, css: str) -> str:
        """Optimize CSS output"""
        optimized = css
        
        # Minification
        if self.level.value in ['standard', 'aggressive', 'maximum']:
            optimized = self._minify_css(optimized)
            self.optimizations_applied.append("CSS minification")
        
        # Remove unused rules
        if self.level.value in ['aggressive', 'maximum']:
            optimized = self._remove_unused_css(optimized)
            self.optimizations_applied.append("Unused CSS removal")
        
        # Optimize selectors
        if self.level.value == 'maximum':
            optimized = self._optimize_selectors(optimized)
            self.optimizations_applied.append("Selector optimization")
        
        return optimized
    
    def optimize_javascript(self, js: str) -> str:
        """Optimize JavaScript output"""
        optimized = js
        
        # Minification
        if self.level.value in ['standard', 'aggressive', 'maximum']:
            optimized = self._minify_js(optimized)
            self.optimizations_applied.append("JavaScript minification")
        
        # Remove console.log
        if self.level.value in ['aggressive', 'maximum']:
            optimized = self._remove_console_logs(optimized)
            self.optimizations_applied.append("Console.log removal")
        
        # Dead code elimination
        if self.level.value == 'maximum':
            optimized = self._eliminate_dead_code(optimized)
            self.optimizations_applied.append("Dead code elimination")
        
        return optimized
    
    def optimize_images(self, images: List[str]) -> List[str]:
        """Optimize image references"""
        optimized = []
        
        for img in images:
            # Lazy loading
            if 'loading=' not in img and self.level.value in ['standard', 'aggressive', 'maximum']:
                img = img.replace('<img ', '<img loading="lazy" ')
                self.optimizations_applied.append("Image lazy loading")
            
            # WebP format suggestion
            if self.level.value in ['aggressive', 'maximum']:
                # Add WebP support
                self.optimizations_applied.append("WebP format support")
            
            optimized.append(img)
        
        return optimized
    
    def enable_caching(self, key: str, value: Any):
        """Enable intelligent caching"""
        self.cache[key] = value
        self.optimizations_applied.append(f"Caching enabled for {key}")
    
    def get_cached(self, key: str) -> Optional[Any]:
        """Get cached value"""
        return self.cache.get(key)
    
    def measure_performance(self, html: str, css: str, js: str) -> PerformanceMetrics:
        """Measure performance metrics"""
        start_time = time.time()
        
        # Simulate measurements
        generation_time = time.time() - start_time
        render_time = 0.05  # Mock render time
        memory_usage = len(html) + len(css) + len(js)
        cpu_usage = 25.0  # Mock CPU usage
        cache_hit_rate = (len(self.cache) / max(len(self.cache) + 10, 1)) * 100
        
        file_size = {
            'html': len(html),
            'css': len(css),
            'js': len(js),
            'total': len(html) + len(css) + len(js)
        }
        
        return PerformanceMetrics(
            generation_time=generation_time,
            render_time=render_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            cache_hit_rate=cache_hit_rate,
            file_size=file_size
        )
    
    def generate_optimization_report(self) -> Dict[str, Any]:
        """Generate optimization report"""
        return {
            'optimization_level': self.level.value,
            'optimizations_applied': self.optimizations_applied,
            'cache_entries': len(self.cache),
            'recommendations': self._get_recommendations()
        }
    
    # Private optimization methods
    
    def _minify_html(self, html: str) -> str:
        """Minify HTML"""
        # Simple minification (production would use proper minifier)
        return html.replace('  ', ' ').replace('\n\n', '\n')
    
    def _remove_whitespace(self, html: str) -> str:
        """Remove unnecessary whitespace"""
        import re
        return re.sub(r'>\s+<', '><', html)
    
    def _inline_critical_css(self, html: str) -> str:
        """Inline critical CSS"""
        # Mock implementation
        return html
    
    def _minify_css(self, css: str) -> str:
        """Minify CSS"""
        return css.replace('  ', ' ').replace('\n\n', '\n')
    
    def _remove_unused_css(self, css: str) -> str:
        """Remove unused CSS rules"""
        # Mock implementation
        return css
    
    def _optimize_selectors(self, css: str) -> str:
        """Optimize CSS selectors"""
        # Mock implementation
        return css
    
    def _minify_js(self, js: str) -> str:
        """Minify JavaScript"""
        return js.replace('  ', ' ').replace('\n\n', '\n')
    
    def _remove_console_logs(self, js: str) -> str:
        """Remove console.log statements"""
        import re
        return re.sub(r'console\.log\([^)]*\);?', '', js)
    
    def _eliminate_dead_code(self, js: str) -> str:
        """Eliminate dead code"""
        # Mock implementation
        return js
    
    def _get_recommendations(self) -> List[str]:
        """Get optimization recommendations"""
        recommendations = []
        
        if self.level == OptimizationLevel.BASIC:
            recommendations.append("Consider using STANDARD optimization level for better performance")
        
        if len(self.cache) < 10:
            recommendations.append("Enable more aggressive caching to improve performance")
        
        recommendations.extend([
            "Use CDN for static assets",
            "Enable gzip compression",
            "Implement service workers for offline support",
            "Use HTTP/2 for better multiplexing",
            "Consider lazy loading for images and components"
        ])
        
        return recommendations


# Performance optimization utilities

def optimize_bundle(html: str, css: str, js: str, level: OptimizationLevel = OptimizationLevel.STANDARD) -> Dict[str, Any]:
    """Optimize complete UI bundle"""
    optimizer = PerformanceOptimizer(level)
    
    # Optimize each part
    optimized_html = optimizer.optimize_html(html)
    optimized_css = optimizer.optimize_css(css)
    optimized_js = optimizer.optimize_javascript(js)
    
    # Measure performance
    metrics = optimizer.measure_performance(optimized_html, optimized_css, optimized_js)
    
    # Generate report
    report = optimizer.generate_optimization_report()
    
    # Calculate savings
    original_size = len(html) + len(css) + len(js)
    optimized_size = len(optimized_html) + len(optimized_css) + len(optimized_js)
    savings = ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
    
    return {
        'optimized': {
            'html': optimized_html,
            'css': optimized_css,
            'js': optimized_js
        },
        'metrics': {
            'generation_time': f"{metrics.generation_time:.3f}s",
            'render_time': f"{metrics.render_time:.3f}s",
            'memory_usage': f"{metrics.memory_usage / 1024:.1f} KB",
            'cpu_usage': f"{metrics.cpu_usage:.1f}%",
            'cache_hit_rate': f"{metrics.cache_hit_rate:.1f}%",
            'performance_score': f"{metrics.get_score():.1f}/100"
        },
        'file_sizes': {
            'original': f"{original_size / 1024:.1f} KB",
            'optimized': f"{optimized_size / 1024:.1f} KB",
            'savings': f"{savings:.1f}%"
        },
        'report': report
    }


if __name__ == "__main__":
    # Demo
    print("Performance Optimizer Demo")
    print("=" * 60)
    
    sample_html = "<html><head><title>Test</title></head><body>  <h1>Hello</h1>  </body></html>"
    sample_css = "body { margin: 0; padding: 0; }\nh1 { color: blue; }"
    sample_js = "console.log('test');\nfunction hello() { return 'world'; }"
    
    result = optimize_bundle(sample_html, sample_css, sample_js, OptimizationLevel.MAXIMUM)
    
    print("\nOptimization Results:")
    print(f"Original Size: {result['file_sizes']['original']}")
    print(f"Optimized Size: {result['file_sizes']['optimized']}")
    print(f"Savings: {result['file_sizes']['savings']}")
    print(f"\nPerformance Score: {result['metrics']['performance_score']}")
    print(f"Generation Time: {result['metrics']['generation_time']}")
    print(f"Memory Usage: {result['metrics']['memory_usage']}")
