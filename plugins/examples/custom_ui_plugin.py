"""
Custom UI Plugin Example for Autonomous UI Engine
Phase 6: Innovation - Plugin System
"""

from typing import Dict, Any
from plugins.plugin_base import UIPlugin, PluginMetadata

class CustomUIPlugin(UIPlugin):
    """Example plugin that adds custom UI components."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            name="custom-ui-plugin",
            version="1.0.0",
            author="UI Engine Team",
            description="Adds custom UI components and enhancements",
            tags=["ui", "components", "customization"]
        )
    
    async def render_component(self, component_type: str, props: Dict[str, Any]) -> str:
        """Render custom UI components."""
        if component_type == "hero-section":
            return self._render_hero_section(props)
        elif component_type == "pricing-table":
            return self._render_pricing_table(props)
        else:
            return f"<div>Unknown component: {component_type}</div>"
    
    def _render_hero_section(self, props: Dict[str, Any]) -> str:
        """Render hero section component."""
        title = props.get("title", "Welcome")
        subtitle = props.get("subtitle", "")
        cta = props.get("cta", "Get Started")
        
        return f"""
        <section class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">{title}</h1>
                <p class="hero-subtitle">{subtitle}</p>
                <button class="hero-cta">{cta}</button>
            </div>
        </section>
        """
    
    def _render_pricing_table(self, props: Dict[str, Any]) -> str:
        """Render pricing table component."""
        plans = props.get("plans", [])
        html = '<div class="pricing-table">'
        
        for plan in plans:
            html += f"""
            <div class="pricing-card">
                <h3>{plan.get('name', 'Plan')}</h3>
                <p class="price">${plan.get('price', 0)}/mo</p>
                <ul class="features">
                    {"".join(f'<li>{f}</li>' for f in plan.get('features', []))}
                </ul>
                <button>Choose Plan</button>
            </div>
            """
        
        html += '</div>'
        return html
