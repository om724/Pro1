"""
Kolam Visualizer
================

This module provides visualization and export functionality for Kolam patterns.
It can render patterns to screen, save as images (PNG, JPEG), or export as SVG.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import numpy as np
from typing import List, Tuple, Optional, Dict
import os
from kolam_geometry import Point2D, KolamPattern, DotGrid
from kolam_generator import KolamGenerator


class KolamVisualizer:
    """Visualizes Kolam patterns using matplotlib"""
    
    def __init__(self, figsize: Tuple[float, float] = (12, 12)):
        self.figsize = figsize
        self.colors = {
            'dots': '#8B4513',      # Brown
            'curves': '#FF4500',    # Orange-Red
            'grid': '#D3D3D3',      # Light Gray
            'background': '#FFF8DC', # Cornsilk
            'symmetry': '#4169E1'   # Royal Blue
        }
        
    def visualize_pattern(self, pattern: KolamPattern, show_grid: bool = True, 
                         show_dots: bool = True, show_symmetry: bool = False,
                         title: Optional[str] = None) -> None:
        """Visualize a complete Kolam pattern"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Set background color
        fig.patch.set_facecolor(self.colors['background'])
        ax.set_facecolor(self.colors['background'])
        
        # Draw grid if requested
        if show_grid and pattern.grid:
            self._draw_grid(ax, pattern.grid)
        
        # Draw dots if requested
        if show_dots and pattern.grid:
            self._draw_dots(ax, pattern.grid)
        
        # Draw curves
        self._draw_curves(ax, pattern.curves)
        
        # Draw symmetry axes if requested
        if show_symmetry:
            self._draw_symmetry_indicators(ax, pattern)
        
        # Customize appearance
        self._customize_plot(ax, pattern, title or pattern.name)
        
        plt.tight_layout()
        plt.show()
    
    def save_pattern(self, pattern: KolamPattern, filename: str, 
                    show_grid: bool = True, show_dots: bool = True,
                    dpi: int = 300, format: str = 'png') -> None:
        """Save a Kolam pattern to file"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Set background color
        fig.patch.set_facecolor(self.colors['background'])
        ax.set_facecolor(self.colors['background'])
        
        # Draw components
        if show_grid and pattern.grid:
            self._draw_grid(ax, pattern.grid)
        
        if show_dots and pattern.grid:
            self._draw_dots(ax, pattern.grid)
        
        self._draw_curves(ax, pattern.curves)
        
        # Customize appearance
        self._customize_plot(ax, pattern, pattern.name)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, format=format, bbox_inches='tight', 
                   facecolor=self.colors['background'])
        plt.close()
        print(f"Pattern saved as: {filename}")
    
    def export_svg(self, pattern: KolamPattern, filename: str) -> None:
        """Export pattern as SVG"""
        if not filename.endswith('.svg'):
            filename += '.svg'
        
        # Get pattern bounds
        bbox_min, bbox_max = pattern.get_bounding_box()
        width = bbox_max.x - bbox_min.x + 2
        height = bbox_max.y - bbox_min.y + 2
        
        # Create SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{width*50}" height="{height*50}" 
     viewBox="{bbox_min.x-1} {bbox_min.y-1} {width} {height}">
     
  <rect width="100%" height="100%" fill="#FFF8DC"/>
  
  <!-- Grid dots -->
'''
        
        # Add dots
        if pattern.grid:
            for dot in pattern.grid.get_all_dots():
                svg_content += f'  <circle cx="{dot.x}" cy="{dot.y}" r="0.05" fill="#8B4513"/>\n'
        
        svg_content += '\n  <!-- Curves -->\n'
        
        # Add curves
        for i, curve in enumerate(pattern.curves):
            if curve:
                path_data = f'M {curve[0].x},{curve[0].y}'
                for point in curve[1:]:
                    path_data += f' L {point.x},{point.y}'
                
                svg_content += f'''  <path d="{path_data}" 
                    stroke="#FF4500" stroke-width="0.08" 
                    fill="none" stroke-linecap="round"/>\n'''
        
        svg_content += '\n</svg>'
        
        with open(filename, 'w') as f:
            f.write(svg_content)
        print(f"SVG exported as: {filename}")
    
    def create_comparison_plot(self, patterns: List[KolamPattern], 
                              cols: int = 3) -> None:
        """Create a comparison plot of multiple patterns"""
        rows = (len(patterns) + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 4*rows))
        fig.patch.set_facecolor(self.colors['background'])
        
        # Flatten axes array for easier indexing
        if rows == 1:
            axes = [axes] if cols == 1 else axes.flatten()
        else:
            axes = axes.flatten()
        
        for i, pattern in enumerate(patterns):
            ax = axes[i]
            ax.set_facecolor(self.colors['background'])
            
            # Draw dots
            if pattern.grid:
                self._draw_dots(ax, pattern.grid, size=20)
            
            # Draw curves
            self._draw_curves(ax, pattern.curves, linewidth=1.5)
            
            # Customize
            self._customize_plot(ax, pattern, pattern.name, small_plot=True)
        
        # Hide unused subplots
        for i in range(len(patterns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.show()
    
    def animate_generation(self, pattern: KolamPattern, steps: int = 50) -> None:
        """Create an animated visualization of pattern generation"""
        # This is a simplified animation - in practice, you'd use matplotlib.animation
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Collect all curve points
        all_points = []
        curve_boundaries = [0]
        
        for curve in pattern.curves:
            all_points.extend(curve)
            curve_boundaries.append(len(all_points))
        
        # Show progressive revelation
        points_per_step = max(1, len(all_points) // steps)
        
        for step in range(0, len(all_points), points_per_step):
            ax.clear()
            ax.set_facecolor(self.colors['background'])
            
            # Draw grid and dots
            if pattern.grid:
                self._draw_dots(ax, pattern.grid, alpha=0.3)
            
            # Draw curves up to current step
            current_points = all_points[:step + points_per_step]
            if current_points:
                # Split back into curves
                curve_idx = 0
                for i in range(len(curve_boundaries) - 1):
                    start = curve_boundaries[i]
                    end = min(curve_boundaries[i + 1], len(current_points))
                    
                    if start < len(current_points):
                        curve_section = current_points[start:end]
                        if len(curve_section) > 1:
                            self._draw_curves(ax, [curve_section], alpha=0.8)
            
            self._customize_plot(ax, pattern, f"{pattern.name} - Step {step//points_per_step + 1}")
            plt.pause(0.1)
        
        plt.show()
    
    def _draw_grid(self, ax, grid: DotGrid, alpha: float = 0.3) -> None:
        """Draw the underlying grid structure"""
        # Vertical lines
        for col in range(grid.cols):
            x = col * grid.spacing
            ax.axvline(x, color=self.colors['grid'], alpha=alpha, linewidth=0.5)
        
        # Horizontal lines
        for row in range(grid.rows):
            y = row * grid.spacing
            ax.axhline(y, color=self.colors['grid'], alpha=alpha, linewidth=0.5)
    
    def _draw_dots(self, ax, grid: DotGrid, size: int = 30, alpha: float = 1.0) -> None:
        """Draw the grid dots"""
        for dot in grid.get_all_dots():
            ax.scatter(dot.x, dot.y, s=size, c=self.colors['dots'], 
                      alpha=alpha, zorder=5)
    
    def _draw_curves(self, ax, curves: List[List[Point2D]], 
                    linewidth: float = 2.0, alpha: float = 1.0) -> None:
        """Draw the pattern curves"""
        for curve in curves:
            if len(curve) > 1:
                x_coords = [p.x for p in curve]
                y_coords = [p.y for p in curve]
                ax.plot(x_coords, y_coords, color=self.colors['curves'], 
                       linewidth=linewidth, alpha=alpha, zorder=10)
    
    def _draw_symmetry_indicators(self, ax, pattern: KolamPattern) -> None:
        """Draw indicators for detected symmetries"""
        if not pattern.curves:
            return
        
        # Calculate pattern center
        all_points = []
        for curve in pattern.curves:
            all_points.extend(curve)
        
        if not all_points:
            return
        
        center_x = sum(p.x for p in all_points) / len(all_points)
        center_y = sum(p.y for p in all_points) / len(all_points)
        
        # Get bounding box for symmetry lines
        bbox_min, bbox_max = pattern.get_bounding_box()
        max_extent = max(bbox_max.x - bbox_min.x, bbox_max.y - bbox_min.y) / 2
        
        # Draw symmetry axes based on detected symmetries
        for symmetry in pattern.symmetries:
            if 'vertical' in symmetry.value.lower():
                ax.axvline(center_x, color=self.colors['symmetry'], 
                          linestyle='--', alpha=0.7, linewidth=1)
            
            if 'horizontal' in symmetry.value.lower():
                ax.axhline(center_y, color=self.colors['symmetry'], 
                          linestyle='--', alpha=0.7, linewidth=1)
            
            if 'rotational' in symmetry.value.lower():
                # Draw a circle to indicate rotational center
                circle = plt.Circle((center_x, center_y), max_extent * 0.1, 
                                  fill=False, color=self.colors['symmetry'],
                                  linestyle=':', alpha=0.7)
                ax.add_patch(circle)
    
    def _customize_plot(self, ax, pattern: KolamPattern, title: str, 
                       small_plot: bool = False) -> None:
        """Customize plot appearance"""
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=14 if not small_plot else 10, 
                    fontweight='bold', pad=20 if not small_plot else 10)
        
        # Remove axes for cleaner look
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add subtle border
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Set margins
        bbox_min, bbox_max = pattern.get_bounding_box()
        margin = 0.5
        ax.set_xlim(bbox_min.x - margin, bbox_max.x + margin)
        ax.set_ylim(bbox_min.y - margin, bbox_max.y + margin)
    
    def create_analysis_report(self, pattern: KolamPattern, filename: str = None) -> Dict:
        """Create a visual analysis report of the pattern"""
        # Analyze pattern properties
        analysis = {
            'name': pattern.name,
            'type': pattern.kolam_type.value,
            'symmetries': [s.value for s in pattern.symmetries],
            'curves_count': len(pattern.curves),
            'total_points': sum(len(curve) for curve in pattern.curves),
        }
        
        if pattern.grid:
            analysis['grid_size'] = f"{pattern.grid.rows}x{pattern.grid.cols}"
            analysis['grid_spacing'] = pattern.grid.spacing
        
        bbox_min, bbox_max = pattern.get_bounding_box()
        analysis['dimensions'] = {
            'width': bbox_max.x - bbox_min.x,
            'height': bbox_max.y - bbox_min.y
        }
        
        # Create visual report
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor(self.colors['background'])
        fig.suptitle(f"Analysis Report: {pattern.name}", fontsize=16, fontweight='bold')
        
        # Main pattern view
        ax1.set_facecolor(self.colors['background'])
        if pattern.grid:
            self._draw_dots(ax1, pattern.grid)
        self._draw_curves(ax1, pattern.curves)
        self._customize_plot(ax1, pattern, "Complete Pattern")
        
        # Pattern with symmetry indicators
        ax2.set_facecolor(self.colors['background'])
        if pattern.grid:
            self._draw_dots(ax2, pattern.grid, alpha=0.5)
        self._draw_curves(ax2, pattern.curves, alpha=0.7)
        self._draw_symmetry_indicators(ax2, pattern)
        self._customize_plot(ax2, pattern, "Symmetry Analysis")
        
        # Grid structure only
        ax3.set_facecolor(self.colors['background'])
        if pattern.grid:
            self._draw_grid(ax3, pattern.grid, alpha=0.8)
            self._draw_dots(ax3, pattern.grid, size=50)
        self._customize_plot(ax3, pattern, "Grid Structure")
        
        # Curves only
        ax4.set_facecolor(self.colors['background'])
        self._draw_curves(ax4, pattern.curves, linewidth=3)
        self._customize_plot(ax4, pattern, "Curve Patterns")
        
        # Add analysis text
        analysis_text = f"""
Analysis Summary:
• Type: {analysis['type']}
• Grid: {analysis.get('grid_size', 'N/A')}
• Curves: {analysis['curves_count']}
• Points: {analysis['total_points']}
• Symmetries: {', '.join(analysis['symmetries']) if analysis['symmetries'] else 'None detected'}
• Dimensions: {analysis['dimensions']['width']:.1f} × {analysis['dimensions']['height']:.1f}
        """
        
        plt.figtext(0.02, 0.02, analysis_text.strip(), fontsize=10, 
                   verticalalignment='bottom', fontfamily='monospace',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight', 
                       facecolor=self.colors['background'])
            print(f"Analysis report saved as: {filename}")
        
        plt.show()
        
        return analysis


def main():
    """Demonstrate the visualization capabilities"""
    print("Kolam Visualizer Demo")
    print("=" * 25)
    
    # Create visualizer
    visualizer = KolamVisualizer(figsize=(10, 10))
    
    # Generate sample patterns
    generator = KolamGenerator()
    patterns = [
        generator.generate_pulli_kolam(5, 5, "basic"),
        generator.generate_flower_kolam(8, 2),
        generator.generate_mandala_kolam(3, 6),
        generator.generate_sikku_kolam(2)
    ]
    
    # Create output directory
    output_dir = "kolam_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Demonstrate different visualization methods
    for i, pattern in enumerate(patterns):
        print(f"\nProcessing: {pattern.name}")
        
        # Save as PNG
        png_filename = os.path.join(output_dir, f"pattern_{i+1}.png")
        visualizer.save_pattern(pattern, png_filename, format='png')
        
        # Export as SVG
        svg_filename = os.path.join(output_dir, f"pattern_{i+1}.svg")
        visualizer.export_svg(pattern, svg_filename)
        
        # Create analysis report for first pattern
        if i == 0:
            analysis_filename = os.path.join(output_dir, f"analysis_report_{i+1}.png")
            analysis = visualizer.create_analysis_report(pattern, analysis_filename)
            print(f"Analysis: {analysis}")
    
    # Create comparison plot
    print("\nCreating comparison plot...")
    visualizer.create_comparison_plot(patterns[:4], cols=2)
    
    print(f"\nAll outputs saved to: {output_dir}")


if __name__ == "__main__":
    main()
