import logging
#!/usr/bin/env python3
"""
Practical Design Tools & Calculators
Interactive tools for applying design theory
"""

import math
from typing import Tuple, List, Dict

class GoldenRatioCalculator:
    """Calculate golden ratio proportions for design"""
    
    PHI = 1.618033988749895  # Golden Ratio
    
    @classmethod
    def divide(cls, total: float) -> Tuple[float, float]:
        """Divide a dimension using golden ratio"""
        larger = total / cls.PHI
        smaller = total - larger
        return (larger, smaller)
    
    @classmethod
    def scale_up(cls, base: float) -> float:
        """Scale up by golden ratio"""
        return base * cls.PHI
    
    @classmethod
    def scale_down(cls, base: float) -> float:
        """Scale down by golden ratio"""
        return base / cls.PHI
    
    @classmethod
    def modular_scale(cls, base: float, steps: int = 7) -> List[float]:
        """Generate modular scale based on golden ratio"""
        scale = []
        current = base
        
        # Scale down
        for i in range(steps // 2, 0, -1):
            current = cls.scale_down(current)
            scale.append(current)
        
        # Base
        scale.append(base)
        
        # Scale up
        current = base
        for i in range(steps // 2):
            current = cls.scale_up(current)
            scale.append(current)
        
        return scale


class ColorTheoryTools:
    """Color theory calculations and harmonies"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def luminance(r: int, g: int, b: int) -> float:
        """Calculate relative luminance (WCAG formula)"""
        def adjust(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r_adj = adjust(r)
        g_adj = adjust(g)
        b_adj = adjust(b)
        
        return 0.2126 * r_adj + 0.7152 * g_adj + 0.0722 * b_adj
    
    @classmethod
    def contrast_ratio(cls, color1: str, color2: str) -> float:
        """Calculate WCAG contrast ratio between two colors"""
        rgb1 = cls.hex_to_rgb(color1)
        rgb2 = cls.hex_to_rgb(color2)
        
        lum1 = cls.luminance(*rgb1)
        lum2 = cls.luminance(*rgb2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @classmethod
    def wcag_level(cls, ratio: float, text_size: str = 'normal') -> str:
        """Determine WCAG compliance level"""
        if text_size == 'large':  # 18pt+ or 14pt+ bold
            if ratio >= 4.5:
                return 'AAA'
            elif ratio >= 3.0:
                return 'AA'
        else:  # Normal text
            if ratio >= 7.0:
                return 'AAA'
            elif ratio >= 4.5:
                return 'AA'
        
        return 'FAIL'
    
    @staticmethod
    def complementary(hue: int) -> int:
        """Get complementary color (opposite on color wheel)"""
        return (hue + 180) % 360
    
    @staticmethod
    def triadic(hue: int) -> Tuple[int, int, int]:
        """Get triadic color harmony"""
        return (hue, (hue + 120) % 360, (hue + 240) % 360)
    
    @staticmethod
    def analogous(hue: int, angle: int = 30) -> Tuple[int, int, int]:
        """Get analogous color harmony"""
        return ((hue - angle) % 360, hue, (hue + angle) % 360)


class TypographyCalculator:
    """Typography calculations and pairing"""
    
    @staticmethod
    def line_height(font_size: float, ratio: float = 1.5) -> float:
        """Calculate optimal line height"""
        return font_size * ratio
    
    @staticmethod
    def line_length(font_size: float, cpl: int = 66) -> float:
        """
        Calculate optimal line length
        cpl = characters per line (optimal: 45-75, ideal: 66)
        """
        # Average character width ≈ 0.5em
        return font_size * 0.5 * cpl
    
    @staticmethod
    def modular_scale_type(base: float, ratio: float = 1.618) -> Dict[str, float]:
        """Generate typographic modular scale"""
        return {
            'h1': base * (ratio ** 3),
            'h2': base * (ratio ** 2),
            'h3': base * ratio,
            'h4': base,
            'body': base,
            'small': base / ratio,
            'tiny': base / (ratio ** 2)
        }


class GridSystemCalculator:
    """Grid system calculations"""
    
    @staticmethod
    def column_width(container_width: float, columns: int = 12, gutter: float = 20) -> float:
        """Calculate column width in a grid system"""
        total_gutter = gutter * (columns - 1)
        available_width = container_width - total_gutter
        return available_width / columns
    
    @staticmethod
    def span_width(column_width: float, columns: int, gutter: float = 20) -> float:
        """Calculate width of spanning multiple columns"""
        return (column_width * columns) + (gutter * (columns - 1))
    
    @staticmethod
    def eight_point_grid(base: int = 8) -> List[int]:
        """Generate 8-point grid scale"""
        return [base * i for i in range(1, 13)]


class DesignToolkit:
    """Complete design toolkit with all tools"""
    
    def __init__(self):
        self.golden = GoldenRatioCalculator()
        self.color = ColorTheoryTools()
        self.type = TypographyCalculator()
        self.grid = GridSystemCalculator()
    
    def analyze_design(self, config: Dict) -> Dict:
        """Analyze a design configuration"""
        results = {}
        
        # Golden ratio analysis
        if 'width' in config:
            width = config['width']
            larger, smaller = self.golden.divide(width)
            results['golden_ratio'] = {
                'total': width,
                'larger_section': larger,
                'smaller_section': smaller,
                'ratio': larger / smaller
            }
        
        # Color contrast analysis
        if 'colors' in config:
            contrasts = []
            colors = config['colors']
            for i, color1 in enumerate(colors):
                for color2 in colors[i+1:]:
                    ratio = self.color.contrast_ratio(color1, color2)
                    level = self.color.wcag_level(ratio)
                    contrasts.append({
                        'color1': color1,
                        'color2': color2,
                        'ratio': ratio,
                        'wcag': level
                    })
            results['color_contrasts'] = contrasts
        
        # Typography analysis
        if 'font_size' in config:
            font_size = config['font_size']
            scale = self.type.modular_scale_type(font_size)
            results['type_scale'] = scale
            results['line_height'] = self.type.line_height(font_size)
            results['optimal_line_length'] = self.type.line_length(font_size)
        
        return results


def demo_tools():
    """Demonstrate all design tools"""
    print("=" * 80)
    print("DESIGN TOOLS DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Golden Ratio
    print("1. GOLDEN RATIO CALCULATOR")
    print("-" * 80)
    width = 1200
    larger, smaller = GoldenRatioCalculator.divide(width)
    print(f"Container width: {width}px")
    print(f"  Larger section: {larger:.2f}px ({larger/width*100:.1f}%)")
    print(f"  Smaller section: {smaller:.2f}px ({smaller/width*100:.1f}%)")
    print(f"  Ratio: {larger/smaller:.6f} (Golden Ratio: 1.618034)")
    print()
    
    # Modular Scale
    print("Modular Scale (base: 16px):")
    scale = GoldenRatioCalculator.modular_scale(16, 7)
    for i, size in enumerate(scale):
        print(f"  Level {i-3}: {size:.2f}px")
    print()
    
    # Color Contrast
    print("2. COLOR CONTRAST ANALYZER")
    print("-" * 80)
    colors = [
        ("#1E3A8A", "#FFFFFF", "Deep Blue on White"),
        ("#059669", "#FFFFFF", "Emerald Green on White"),
        ("#F59E0B", "#FFFFFF", "Warm Gold on White"),
        ("#000000", "#FFFFFF", "Black on White"),
    ]
    
    for color1, color2, desc in colors:
        ratio = ColorTheoryTools.contrast_ratio(color1, color2)
        level = ColorTheoryTools.wcag_level(ratio)
        print(f"{desc}:")
        print(f"  Contrast Ratio: {ratio:.2f}:1")
        print(f"  WCAG Level: {level}")
        print()
    
    # Typography
    print("3. TYPOGRAPHY CALCULATOR")
    print("-" * 80)
    base_size = 16
    scale = TypographyCalculator.modular_scale_type(base_size)
    print(f"Base font size: {base_size}px")
    print("Modular scale:")
    for level, size in scale.items():
        line_height = TypographyCalculator.line_height(size)
        print(f"  {level:6s}: {size:6.2f}px  (line-height: {line_height:.2f}px)")
    print()
    
    # Grid System
    print("4. GRID SYSTEM CALCULATOR")
    print("-" * 80)
    container = 1200
    columns = 12
    gutter = 20
    col_width = GridSystemCalculator.column_width(container, columns, gutter)
    print(f"Container: {container}px")
    print(f"Columns: {columns}")
    print(f"Gutter: {gutter}px")
    print(f"Column width: {col_width:.2f}px")
    print()
    print("Common spans:")
    for span in [1, 2, 3, 4, 6, 8, 12]:
        width = GridSystemCalculator.span_width(col_width, span, gutter)
        print(f"  {span:2d} columns: {width:7.2f}px ({width/container*100:5.1f}%)")
    print()
    
    # 8-point grid
    print("5. 8-POINT GRID SCALE")
    print("-" * 80)
    grid = GridSystemCalculator.eight_point_grid()
    print("Spacing scale:", ", ".join(f"{x}px" for x in grid))
    print()
    
    print("=" * 80)


if __name__ == "__main__":
    demo_tools()
