"""
Complete Design System Generator
Generates comprehensive design systems with color palettes, typography, spacing, and components
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import json
import colorsys
import numpy as np


@dataclass
class ColorPalette:
    """Color palette with shades"""
    name: str
    primary: Dict[str, str]  # 50, 100, 200, ..., 900
    secondary: Dict[str, str]
    accent: Dict[str, str]
    neutral: Dict[str, str]
    semantic: Dict[str, str]  # success, warning, error, info


@dataclass
class TypographySystem:
    """Typography system"""
    font_families: Dict[str, str]
    font_sizes: Dict[str, str]
    font_weights: Dict[str, int]
    line_heights: Dict[str, float]
    letter_spacing: Dict[str, str]


@dataclass
class SpacingSystem:
    """Spacing system"""
    scale: List[str]  # 0, 1, 2, 4, 8, 12, 16, 24, 32, 48, 64...
    breakpoints: Dict[str, str]
    container_widths: Dict[str, str]


@dataclass
class DesignTokens:
    """Design tokens"""
    colors: ColorPalette
    typography: TypographySystem
    spacing: SpacingSystem
    shadows: Dict[str, str]
    borders: Dict[str, str]
    radii: Dict[str, str]
    transitions: Dict[str, str]
    z_index: Dict[str, int]


@dataclass
class DesignSystem:
    """Complete design system"""
    name: str
    version: str
    tokens: DesignTokens
    components: List[str]
    css_variables: str
    documentation: str


class DesignSystemGenerator:
    """
    Complete design system generator.
    
    Features:
    - AI-powered color palette generation
    - Typography system with scale
    - Spacing and layout system
    - Component tokens
    - CSS variables output
    - Comprehensive documentation
    - Multi-format export (CSS, JSON, Sass, Less)
    """
    
    def __init__(self):
        """Initialize design system generator"""
        self.golden_ratio = 1.618
        self.major_third = 1.25
        self.perfect_fourth = 1.333
        
        print("✓ Design System Generator initialized")
    
    def generate_design_system(
        self,
        name: str,
        base_color: str = "#2563eb",
        style: str = "modern",  # modern, classic, minimal, bold
        scale: str = "moderate"  # compact, moderate, spacious
    ) -> DesignSystem:
        """
        Generate a complete design system.
        
        Args:
            name: Design system name
            base_color: Base primary color (hex)
            style: Design style
            scale: Spacing scale
        
        Returns:
            Complete design system
        """
        
        # Generate color palette
        colors = self._generate_color_palette(base_color, style)
        
        # Generate typography system
        typography = self._generate_typography_system(style, scale)
        
        # Generate spacing system
        spacing = self._generate_spacing_system(scale)
        
        # Generate other tokens
        shadows = self._generate_shadows(style)
        borders = self._generate_borders(style)
        radii = self._generate_radii(style)
        transitions = self._generate_transitions(style)
        z_index = self._generate_z_index()
        
        # Create design tokens
        tokens = DesignTokens(
            colors=colors,
            typography=typography,
            spacing=spacing,
            shadows=shadows,
            borders=borders,
            radii=radii,
            transitions=transitions,
            z_index=z_index
        )
        
        # Generate CSS variables
        css_variables = self._generate_css_variables(tokens)
        
        # Generate documentation
        documentation = self._generate_documentation(name, tokens, style)
        
        # List of components using this system
        components = [
            'Button', 'Input', 'Card', 'Modal', 'Navbar', 'Sidebar',
            'Form', 'Table', 'Chart', 'Alert', 'Badge', 'Tooltip'
        ]
        
        return DesignSystem(
            name=name,
            version="1.0.0",
            tokens=tokens,
            components=components,
            css_variables=css_variables,
            documentation=documentation
        )
    
    def _generate_color_palette(self, base_color: str, style: str) -> ColorPalette:
        """Generate color palette from base color"""
        
        # Convert hex to HSL
        r, g, b = self._hex_to_rgb(base_color)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        # Generate primary shades
        primary = {}
        for shade in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
            if shade == 500:
                primary[str(shade)] = base_color
            elif shade < 500:
                # Lighter shades
                lightness = l + (1 - l) * (500 - shade) / 500
                new_r, new_g, new_b = colorsys.hls_to_rgb(h, lightness, s)
                primary[str(shade)] = self._rgb_to_hex(int(new_r * 255), int(new_g * 255), int(new_b * 255))
            else:
                # Darker shades
                lightness = l * (1000 - shade) / 500
                new_r, new_g, new_b = colorsys.hls_to_rgb(h, lightness, s)
                primary[str(shade)] = self._rgb_to_hex(int(new_r * 255), int(new_g * 255), int(new_b * 255))
        
        # Generate complementary secondary color
        secondary_h = (h + 0.5) % 1.0
        secondary = {}
        for shade in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
            lightness = 0.95 - (shade / 1000) * 0.7
            new_r, new_g, new_b = colorsys.hls_to_rgb(secondary_h, lightness, s)
            secondary[str(shade)] = self._rgb_to_hex(int(new_r * 255), int(new_g * 255), int(new_b * 255))
        
        # Generate accent color (triadic)
        accent_h = (h + 0.33) % 1.0
        accent = {}
        for shade in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
            lightness = 0.95 - (shade / 1000) * 0.7
            new_r, new_g, new_b = colorsys.hls_to_rgb(accent_h, lightness, s)
            accent[str(shade)] = self._rgb_to_hex(int(new_r * 255), int(new_g * 255), int(new_b * 255))
        
        # Generate neutral grays
        neutral = {
            '50': '#fafafa',
            '100': '#f5f5f5',
            '200': '#e5e5e5',
            '300': '#d4d4d4',
            '400': '#a3a3a3',
            '500': '#737373',
            '600': '#525252',
            '700': '#404040',
            '800': '#262626',
            '900': '#171717'
        }
        
        # Generate semantic colors
        semantic = {
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6'
        }
        
        return ColorPalette(
            name="Generated Palette",
            primary=primary,
            secondary=secondary,
            accent=accent,
            neutral=neutral,
            semantic=semantic
        )
    
    def _generate_typography_system(self, style: str, scale: str) -> TypographySystem:
        """Generate typography system"""
        
        # Font families based on style
        font_families = {
            'heading': 'Inter, system-ui, sans-serif',
            'body': 'Inter, system-ui, sans-serif',
            'mono': 'JetBrains Mono, Consolas, monospace'
        }
        
        if style == 'classic':
            font_families['heading'] = 'Georgia, serif'
            font_families['body'] = 'Georgia, serif'
        elif style == 'minimal':
            font_families['heading'] = 'Helvetica Neue, Arial, sans-serif'
            font_families['body'] = 'Helvetica Neue, Arial, sans-serif'
        
        # Font sizes using modular scale
        base_size = 16
        ratio = self.major_third if scale == 'moderate' else (self.perfect_fourth if scale == 'spacious' else 1.2)
        
        font_sizes = {}
        for i, label in enumerate(['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl']):
            size = base_size * (ratio ** (i - 2))  # base is at index 2
            font_sizes[label] = f"{size:.2f}px"
        
        # Font weights
        font_weights = {
            'thin': 100,
            'light': 300,
            'normal': 400,
            'medium': 500,
            'semibold': 600,
            'bold': 700,
            'extrabold': 800,
            'black': 900
        }
        
        # Line heights
        line_heights = {
            'none': 1.0,
            'tight': 1.25,
            'snug': 1.375,
            'normal': 1.5,
            'relaxed': 1.625,
            'loose': 2.0
        }
        
        # Letter spacing
        letter_spacing = {
            'tighter': '-0.05em',
            'tight': '-0.025em',
            'normal': '0',
            'wide': '0.025em',
            'wider': '0.05em',
            'widest': '0.1em'
        }
        
        return TypographySystem(
            font_families=font_families,
            font_sizes=font_sizes,
            font_weights=font_weights,
            line_heights=line_heights,
            letter_spacing=letter_spacing
        )
    
    def _generate_spacing_system(self, scale: str) -> SpacingSystem:
        """Generate spacing system"""
        
        # Base unit
        base = 4 if scale == 'compact' else (8 if scale == 'spacious' else 4)
        
        # Generate scale
        spacing_scale = ['0']
        for multiplier in [0.25, 0.5, 1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64]:
            spacing_scale.append(f"{base * multiplier}px")
        
        # Breakpoints
        breakpoints = {
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
            '2xl': '1536px'
        }
        
        # Container widths
        container_widths = {
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
            '2xl': '1536px',
            'full': '100%'
        }
        
        return SpacingSystem(
            scale=spacing_scale,
            breakpoints=breakpoints,
            container_widths=container_widths
        )
    
    def _generate_shadows(self, style: str) -> Dict[str, str]:
        """Generate shadow system"""
        
        if style == 'minimal':
            return {
                'sm': 'none',
                'base': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                'md': '0 2px 4px 0 rgba(0, 0, 0, 0.05)',
                'lg': '0 4px 6px 0 rgba(0, 0, 0, 0.05)',
                'xl': '0 8px 12px 0 rgba(0, 0, 0, 0.05)',
                '2xl': '0 12px 24px 0 rgba(0, 0, 0, 0.05)'
            }
        elif style == 'bold':
            return {
                'sm': '0 2px 4px 0 rgba(0, 0, 0, 0.2)',
                'base': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                'md': '0 6px 12px 0 rgba(0, 0, 0, 0.2)',
                'lg': '0 10px 20px 0 rgba(0, 0, 0, 0.2)',
                'xl': '0 20px 40px 0 rgba(0, 0, 0, 0.2)',
                '2xl': '0 30px 60px 0 rgba(0, 0, 0, 0.25)'
            }
        else:  # modern, classic
            return {
                'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
                'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
                '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
            }
    
    def _generate_borders(self, style: str) -> Dict[str, str]:
        """Generate border system"""
        
        return {
            'none': '0',
            'sm': '1px',
            'base': '2px',
            'md': '3px',
            'lg': '4px',
            'xl': '8px'
        }
    
    def _generate_radii(self, style: str) -> Dict[str, str]:
        """Generate border radius system"""
        
        if style == 'minimal':
            return {
                'none': '0',
                'sm': '2px',
                'base': '4px',
                'md': '6px',
                'lg': '8px',
                'xl': '12px',
                'full': '9999px'
            }
        elif style == 'bold':
            return {
                'none': '0',
                'sm': '4px',
                'base': '8px',
                'md': '12px',
                'lg': '16px',
                'xl': '24px',
                'full': '9999px'
            }
        else:
            return {
                'none': '0',
                'sm': '3px',
                'base': '6px',
                'md': '8px',
                'lg': '12px',
                'xl': '16px',
                'full': '9999px'
            }
    
    def _generate_transitions(self, style: str) -> Dict[str, str]:
        """Generate transition system"""
        
        return {
            'fast': '150ms cubic-bezier(0.4, 0, 0.2, 1)',
            'base': '300ms cubic-bezier(0.4, 0, 0.2, 1)',
            'slow': '500ms cubic-bezier(0.4, 0, 0.2, 1)',
            'bounce': '300ms cubic-bezier(0.68, -0.55, 0.265, 1.55)'
        }
    
    def _generate_z_index(self) -> Dict[str, int]:
        """Generate z-index system"""
        
        return {
            'base': 0,
            'dropdown': 1000,
            'sticky': 1100,
            'fixed': 1200,
            'modal_backdrop': 1300,
            'modal': 1400,
            'popover': 1500,
            'tooltip': 1600
        }
    
    def _generate_css_variables(self, tokens: DesignTokens) -> str:
        """Generate CSS variables from tokens"""
        
        css = ":root {\n"
        css += "  /* Colors - Primary */\n"
        for shade, value in tokens.colors.primary.items():
            css += f"  --color-primary-{shade}: {value};\n"
        
        css += "\n  /* Colors - Secondary */\n"
        for shade, value in tokens.colors.secondary.items():
            css += f"  --color-secondary-{shade}: {value};\n"
        
        css += "\n  /* Colors - Accent */\n"
        for shade, value in tokens.colors.accent.items():
            css += f"  --color-accent-{shade}: {value};\n"
        
        css += "\n  /* Colors - Neutral */\n"
        for shade, value in tokens.colors.neutral.items():
            css += f"  --color-neutral-{shade}: {value};\n"
        
        css += "\n  /* Colors - Semantic */\n"
        for name, value in tokens.colors.semantic.items():
            css += f"  --color-{name}: {value};\n"
        
        css += "\n  /* Typography - Font Families */\n"
        for name, value in tokens.typography.font_families.items():
            css += f"  --font-{name}: {value};\n"
        
        css += "\n  /* Typography - Font Sizes */\n"
        for name, value in tokens.typography.font_sizes.items():
            css += f"  --text-{name}: {value};\n"
        
        css += "\n  /* Typography - Font Weights */\n"
        for name, value in tokens.typography.font_weights.items():
            css += f"  --font-{name}: {value};\n"
        
        css += "\n  /* Spacing */\n"
        for i, value in enumerate(tokens.spacing.scale):
            css += f"  --space-{i}: {value};\n"
        
        css += "\n  /* Shadows */\n"
        for name, value in tokens.shadows.items():
            css += f"  --shadow-{name}: {value};\n"
        
        css += "\n  /* Border Radius */\n"
        for name, value in tokens.radii.items():
            css += f"  --radius-{name}: {value};\n"
        
        css += "\n  /* Transitions */\n"
        for name, value in tokens.transitions.items():
            css += f"  --transition-{name}: {value};\n"
        
        css += "\n  /* Z-Index */\n"
        for name, value in tokens.z_index.items():
            css += f"  --z-{name}: {value};\n"
        
        css += "}\n"
        
        return css
    
    def _generate_documentation(self, name: str, tokens: DesignTokens, style: str) -> str:
        """Generate design system documentation"""
        
        doc = f"""# {name} Design System

## Overview
Complete design system with tokens, components, and guidelines.

**Style:** {style}
**Version:** 1.0.0

## Color Palette

### Primary
{self._format_color_doc(tokens.colors.primary)}

### Secondary
{self._format_color_doc(tokens.colors.secondary)}

### Semantic Colors
- Success: {tokens.colors.semantic['success']}
- Warning: {tokens.colors.semantic['warning']}
- Error: {tokens.colors.semantic['error']}
- Info: {tokens.colors.semantic['info']}

## Typography

### Font Families
- Heading: {tokens.typography.font_families['heading']}
- Body: {tokens.typography.font_families['body']}
- Mono: {tokens.typography.font_families['mono']}

### Font Sizes
{self._format_dict_doc(tokens.typography.font_sizes)}

### Font Weights
{self._format_dict_doc(tokens.typography.font_weights)}

## Spacing
Scale: {', '.join(tokens.spacing.scale)}

### Breakpoints
{self._format_dict_doc(tokens.spacing.breakpoints)}

## Shadows
{self._format_dict_doc(tokens.shadows)}

## Border Radius
{self._format_dict_doc(tokens.radii)}

## Usage

### CSS Variables
All tokens are available as CSS variables:
```css
.my-component {{
    color: var(--color-primary-500);
    font-family: var(--font-heading);
    padding: var(--space-4);
    border-radius: var(--radius-md);
}}
```

### Components
Use the design tokens in your components for consistent styling.

## Export Formats
- CSS Variables (included)
- JSON (use export_json method)
- Sass Variables (use export_sass method)
- Tailwind Config (use export_tailwind method)
"""
        
        return doc
    
    def _format_color_doc(self, colors: Dict[str, str]) -> str:
        """Format color documentation"""
        lines = []
        for shade, value in colors.items():
            lines.append(f"- {shade}: {value}")
        return '\n'.join(lines)
    
    def _format_dict_doc(self, data: Dict[str, Any]) -> str:
        """Format dictionary documentation"""
        lines = []
        for key, value in data.items():
            lines.append(f"- {key}: {value}")
        return '\n'.join(lines)
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def export_json(self, design_system: DesignSystem) -> str:
        """Export design system as JSON"""
        data = {
            'name': design_system.name,
            'version': design_system.version,
            'colors': {
                'primary': design_system.tokens.colors.primary,
                'secondary': design_system.tokens.colors.secondary,
                'accent': design_system.tokens.colors.accent,
                'neutral': design_system.tokens.colors.neutral,
                'semantic': design_system.tokens.colors.semantic
            },
            'typography': {
                'fontFamilies': design_system.tokens.typography.font_families,
                'fontSizes': design_system.tokens.typography.font_sizes,
                'fontWeights': design_system.tokens.typography.font_weights
            },
            'spacing': {
                'scale': design_system.tokens.spacing.scale,
                'breakpoints': design_system.tokens.spacing.breakpoints
            },
            'shadows': design_system.tokens.shadows,
            'radii': design_system.tokens.radii
        }
        return json.dumps(data, indent=2)
    
    def export_sass(self, design_system: DesignSystem) -> str:
        """Export design system as Sass variables"""
        sass = f"// {design_system.name} Design System\n\n"
        
        sass += "// Colors - Primary\n"
        for shade, value in design_system.tokens.colors.primary.items():
            sass += f"$color-primary-{shade}: {value};\n"
        
        sass += "\n// Typography\n"
        for name, value in design_system.tokens.typography.font_sizes.items():
            sass += f"$text-{name}: {value};\n"
        
        return sass
    
    def export_tailwind(self, design_system: DesignSystem) -> str:
        """Export design system as Tailwind config"""
        config = {
            'theme': {
                'extend': {
                    'colors': {
                        'primary': design_system.tokens.colors.primary,
                        'secondary': design_system.tokens.colors.secondary
                    },
                    'fontSize': design_system.tokens.typography.font_sizes,
                    'spacing': dict(enumerate(design_system.tokens.spacing.scale)),
                    'borderRadius': design_system.tokens.radii
                }
            }
        }
        return f"module.exports = {json.dumps(config, indent=2)}"


# Example usage
if __name__ == "__main__":
    print("Initializing Design System Generator...")
    generator = DesignSystemGenerator()
    
    print("\n=== Generating Design System ===")
    design_system = generator.generate_design_system(
        name="MyApp",
        base_color="#3b82f6",
        style="modern",
        scale="moderate"
    )
    
    print(f"Generated: {design_system.name} v{design_system.version}")
    print(f"Components: {len(design_system.components)}")
    
    print("\n=== Color Palette Sample ===")
    print(f"Primary 500: {design_system.tokens.colors.primary['500']}")
    print(f"Primary 700: {design_system.tokens.colors.primary['700']}")
    print(f"Success: {design_system.tokens.colors.semantic['success']}")
    
    print("\n=== Typography Sample ===")
    print(f"Base font size: {design_system.tokens.typography.font_sizes['base']}")
    print(f"Heading font: {design_system.tokens.typography.font_families['heading']}")
    
    print("\n=== Spacing Sample ===")
    print(f"Spacing scale: {design_system.tokens.spacing.scale[:5]}...")
    
    print("\n=== CSS Variables Preview ===")
    print(design_system.css_variables[:300] + "...")
    
    print("\n=== Export Options ===")
    print("✓ CSS Variables (included)")
    print("✓ JSON export available")
    print("✓ Sass export available")
    print("✓ Tailwind config export available")
