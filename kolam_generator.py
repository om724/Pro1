"""
Kolam Pattern Generator
======================

This module implements algorithms for recognizing and generating various types of Kolam patterns
based on the mathematical principles identified in kolam_geometry.py
"""

import math
import random
from typing import List, Tuple, Dict, Optional, Set
from kolam_geometry import (
    DotGrid, Point2D, CurveGenerator, SymmetryAnalyzer, KolamPattern,
    KolamType, SymmetryType
)


class PatternRecognizer:
    """Recognizes patterns and design principles in existing Kolam designs"""
    
    def __init__(self):
        self.tolerance = 0.1
    
    def analyze_grid_structure(self, points: List[Point2D]) -> Dict:
        """Analyze the underlying grid structure of a Kolam pattern"""
        if len(points) < 4:
            return {"grid_detected": False}
        
        # Sort points to find potential grid structure
        sorted_x = sorted(set(round(p.x, 1) for p in points))
        sorted_y = sorted(set(round(p.y, 1) for p in points))
        
        # Calculate potential spacing
        x_spacings = [sorted_x[i+1] - sorted_x[i] for i in range(len(sorted_x)-1)]
        y_spacings = [sorted_y[i+1] - sorted_y[i] for i in range(len(sorted_y)-1)]
        
        # Find most common spacing
        x_spacing = self._find_common_spacing(x_spacings) if x_spacings else 1.0
        y_spacing = self._find_common_spacing(y_spacings) if y_spacings else 1.0
        
        return {
            "grid_detected": True,
            "rows": len(sorted_y),
            "cols": len(sorted_x),
            "x_spacing": x_spacing,
            "y_spacing": y_spacing,
            "origin": Point2D(min(sorted_x), min(sorted_y))
        }
    
    def _find_common_spacing(self, spacings: List[float]) -> float:
        """Find the most common spacing in a list of spacings"""
        if not spacings:
            return 1.0
        
        # Round spacings to avoid floating point issues
        rounded = [round(s, 2) for s in spacings]
        spacing_counts = {}
        
        for spacing in rounded:
            spacing_counts[spacing] = spacing_counts.get(spacing, 0) + 1
        
        return max(spacing_counts.keys(), key=lambda x: spacing_counts[x])
    
    def detect_curve_types(self, curve_points: List[Point2D]) -> List[str]:
        """Detect the types of curves present in a pattern"""
        if len(curve_points) < 10:
            return ["simple"]
        
        curve_types = []
        
        # Check for circular patterns
        if self._is_circular_pattern(curve_points):
            curve_types.append("circular")
        
        # Check for spiral patterns
        if self._is_spiral_pattern(curve_points):
            curve_types.append("spiral")
        
        # Check for petal/rose patterns
        if self._is_petal_pattern(curve_points):
            curve_types.append("petal")
        
        # Check for straight line segments
        if self._has_linear_segments(curve_points):
            curve_types.append("linear")
        
        return curve_types if curve_types else ["complex"]
    
    def _is_circular_pattern(self, points: List[Point2D]) -> bool:
        """Check if points form circular arcs"""
        if len(points) < 10:
            return False
        
        # Calculate center as centroid
        center = Point2D(
            sum(p.x for p in points) / len(points),
            sum(p.y for p in points) / len(points)
        )
        
        # Calculate distances from center
        distances = [p.distance_to(center) for p in points]
        avg_distance = sum(distances) / len(distances)
        
        # Check if distances are roughly equal (circular)
        variance = sum((d - avg_distance) ** 2 for d in distances) / len(distances)
        return variance < (avg_distance * 0.1) ** 2
    
    def _is_spiral_pattern(self, points: List[Point2D]) -> bool:
        """Check if points form a spiral pattern"""
        if len(points) < 20:
            return False
        
        # Calculate center
        center = Point2D(
            sum(p.x for p in points) / len(points),
            sum(p.y for p in points) / len(points)
        )
        
        # Calculate angles and distances
        angles = []
        distances = []
        
        for p in points:
            dx = p.x - center.x
            dy = p.y - center.y
            angle = math.atan2(dy, dx)
            distance = p.distance_to(center)
            angles.append(angle)
            distances.append(distance)
        
        # Check if distances generally increase with angle progression
        angle_progression = 0
        distance_trend = 0
        
        for i in range(1, len(points)):
            angle_diff = angles[i] - angles[i-1]
            # Handle angle wrapping
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            angle_progression += angle_diff
            
            if distances[i] > distances[i-1]:
                distance_trend += 1
        
        return abs(angle_progression) > 2 * math.pi and distance_trend > len(points) * 0.6
    
    def _is_petal_pattern(self, points: List[Point2D]) -> bool:
        """Check if points form petal/rose patterns"""
        if len(points) < 20:
            return False
        
        # Calculate center
        center = Point2D(
            sum(p.x for p in points) / len(points),
            sum(p.y for p in points) / len(points)
        )
        
        # Calculate polar coordinates
        polar_points = []
        for p in points:
            dx = p.x - center.x
            dy = p.y - center.y
            angle = math.atan2(dy, dx)
            radius = p.distance_to(center)
            polar_points.append((angle, radius))
        
        # Sort by angle
        polar_points.sort()
        
        # Look for periodic patterns in radius
        radii = [r for _, r in polar_points]
        
        # Simple check for multiple local maxima (petals)
        local_maxima = 0
        for i in range(1, len(radii) - 1):
            if radii[i] > radii[i-1] and radii[i] > radii[i+1]:
                local_maxima += 1
        
        return local_maxima >= 4  # At least 4 petals
    
    def _has_linear_segments(self, points: List[Point2D]) -> bool:
        """Check if curve has linear segments"""
        if len(points) < 6:
            return False
        
        linear_segments = 0
        segment_length = 5
        
        for i in range(len(points) - segment_length):
            segment = points[i:i+segment_length]
            if self._is_linear_segment(segment):
                linear_segments += 1
        
        return linear_segments > 0
    
    def _is_linear_segment(self, points: List[Point2D]) -> bool:
        """Check if a small segment of points is approximately linear"""
        if len(points) < 3:
            return True
        
        # Fit a line using least squares
        n = len(points)
        sum_x = sum(p.x for p in points)
        sum_y = sum(p.y for p in points)
        sum_xy = sum(p.x * p.y for p in points)
        sum_x2 = sum(p.x * p.x for p in points)
        
        denom = n * sum_x2 - sum_x * sum_x
        if abs(denom) < 1e-10:
            return True  # Vertical line
        
        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n
        
        # Calculate R-squared
        y_mean = sum_y / n
        ss_tot = sum((p.y - y_mean) ** 2 for p in points)
        ss_res = sum((p.y - (slope * p.x + intercept)) ** 2 for p in points)
        
        if ss_tot < 1e-10:
            return True
        
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared > 0.9


class KolamGenerator:
    """Generates various types of Kolam patterns based on mathematical principles"""
    
    def __init__(self):
        self.patterns = {}
    
    def generate_pulli_kolam(self, rows: int, cols: int, dot_pattern: str = "basic") -> KolamPattern:
        """Generate a Pulli Kolam (dot-based pattern)"""
        pattern = KolamPattern(f"Pulli Kolam {rows}x{cols}", KolamType.PULLI_KOLAM)
        pattern.set_grid(rows, cols, spacing=2.0)
        
        curve_gen = CurveGenerator(pattern.grid)
        
        if dot_pattern == "basic":
            # Simple rectangular loops
            for r in range(1, rows-1, 2):
                for c in range(1, cols-1, 2):
                    if r < rows-1 and c < cols-1:
                        square_dots = [
                            (r, c), (r, c+1), (r+1, c+1), (r+1, c), (r, c)
                        ]
                        curve = curve_gen.generate_loop_around_dots(square_dots, 0.4)
                        pattern.add_curve(curve)
        
        elif dot_pattern == "diamond":
            # Diamond shaped loops
            center_r, center_c = rows // 2, cols // 2
            for size in range(1, min(rows, cols) // 2):
                diamond_dots = []
                # Top
                if center_r - size >= 0:
                    diamond_dots.append((center_r - size, center_c))
                # Right
                if center_c + size < cols:
                    diamond_dots.append((center_r, center_c + size))
                # Bottom
                if center_r + size < rows:
                    diamond_dots.append((center_r + size, center_c))
                # Left
                if center_c - size >= 0:
                    diamond_dots.append((center_r, center_c - size))
                # Close the diamond
                if diamond_dots:
                    diamond_dots.append(diamond_dots[0])
                    curve = curve_gen.generate_loop_around_dots(diamond_dots, 0.3)
                    pattern.add_curve(curve)
        
        pattern.analyze_symmetries()
        return pattern
    
    def generate_sikku_kolam(self, complexity: int = 3) -> KolamPattern:
        """Generate a Sikku Kolam (knot pattern) with interlocking curves"""
        pattern = KolamPattern(f"Sikku Kolam Level {complexity}", KolamType.SIKKU_KOLAM)
        size = 2 * complexity + 3
        pattern.set_grid(size, size, spacing=1.5)
        
        curve_gen = CurveGenerator(pattern.grid)
        center = Point2D((size-1) * 1.5 / 2, (size-1) * 1.5 / 2)
        
        # Generate interlocking spiral patterns
        for i in range(complexity):
            angle_offset = i * 2 * math.pi / complexity
            spiral_center = Point2D(
                center.x + (i + 1) * 0.5 * math.cos(angle_offset),
                center.y + (i + 1) * 0.5 * math.sin(angle_offset)
            )
            
            spiral_curve = curve_gen.generate_spiral_pattern(
                spiral_center, 
                radius=1.0 + i * 0.3, 
                turns=2 + i * 0.5
            )
            pattern.add_curve(spiral_curve)
        
        # Add connecting curves for the knot effect
        for i in range(complexity):
            angle1 = i * 2 * math.pi / complexity
            angle2 = (i + 1) * 2 * math.pi / complexity
            
            start = Point2D(
                center.x + 2 * math.cos(angle1),
                center.y + 2 * math.sin(angle1)
            )
            end = Point2D(
                center.x + 2 * math.cos(angle2),
                center.y + 2 * math.sin(angle2)
            )
            
            # Simple connecting curve
            connecting_curve = self._generate_connecting_curve(start, end)
            pattern.add_curve(connecting_curve)
        
        pattern.analyze_symmetries()
        return pattern
    
    def generate_kambi_kolam(self, grid_size: int, line_style: str = "geometric") -> KolamPattern:
        """Generate a Kambi Kolam (line-based wireframe pattern)"""
        pattern = KolamPattern(f"Kambi Kolam {grid_size}x{grid_size}", KolamType.KAMBI_KOLAM)
        pattern.set_grid(grid_size, grid_size, spacing=1.0)
        
        curve_gen = CurveGenerator(pattern.grid)
        
        if line_style == "geometric":
            # Create geometric line patterns
            # Horizontal lines
            for r in range(0, grid_size, 2):
                line_points = []
                for c in range(grid_size):
                    dot = pattern.grid.get_dot(r, c)
                    if dot:
                        line_points.append(dot)
                if line_points:
                    pattern.add_curve(line_points)
            
            # Vertical lines
            for c in range(0, grid_size, 2):
                line_points = []
                for r in range(grid_size):
                    dot = pattern.grid.get_dot(r, c)
                    if dot:
                        line_points.append(dot)
                if line_points:
                    pattern.add_curve(line_points)
            
            # Diagonal lines
            for offset in range(-(grid_size-1), grid_size):
                line_points = []
                for r in range(grid_size):
                    c = r + offset
                    if 0 <= c < grid_size:
                        dot = pattern.grid.get_dot(r, c)
                        if dot:
                            line_points.append(dot)
                if len(line_points) > 1:
                    pattern.add_curve(line_points)
        
        elif line_style == "star":
            # Star pattern emanating from center
            center_r, center_c = grid_size // 2, grid_size // 2
            center_dot = pattern.grid.get_dot(center_r, center_c)
            
            if center_dot:
                # Rays in 8 directions
                directions = [
                    (-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)
                ]
                
                for dr, dc in directions:
                    line_points = [center_dot]
                    r, c = center_r, center_c
                    
                    while True:
                        r += dr
                        c += dc
                        dot = pattern.grid.get_dot(r, c)
                        if dot:
                            line_points.append(dot)
                        else:
                            break
                    
                    if len(line_points) > 1:
                        pattern.add_curve(line_points)
        
        pattern.analyze_symmetries()
        return pattern
    
    def generate_flower_kolam(self, num_petals: int = 8, layers: int = 3) -> KolamPattern:
        """Generate a flower-like Kolam pattern with petal structures"""
        pattern = KolamPattern(f"Flower Kolam {num_petals} petals", KolamType.MARGAZHI_KOLAM)
        grid_size = 2 * layers + 5
        pattern.set_grid(grid_size, grid_size, spacing=1.0)
        
        curve_gen = CurveGenerator(pattern.grid)
        center = Point2D((grid_size-1) * 0.5, (grid_size-1) * 0.5)
        
        # Generate multiple layers of petals
        for layer in range(layers):
            radius = 1.0 + layer * 0.8
            petal_curve = curve_gen.generate_petal_pattern(center, radius, num_petals)
            pattern.add_curve(petal_curve)
        
        # Add center spiral
        center_spiral = curve_gen.generate_spiral_pattern(center, 0.5, 1.5)
        pattern.add_curve(center_spiral)
        
        # Apply symmetry for traditional appearance
        all_points = []
        for curve in pattern.curves:
            all_points.extend(curve)
        
        # For now, keep the original curves until we implement the symmetry application properly
        # symmetric_points = SymmetryAnalyzer.apply_symmetry(
        #     all_points, center, SymmetryType.ROTATIONAL_4
        # )
        
        pattern.analyze_symmetries()
        return pattern
    
    def generate_mandala_kolam(self, rings: int = 4, segments: int = 8) -> KolamPattern:
        """Generate a mandala-style Kolam with concentric patterns"""
        pattern = KolamPattern(f"Mandala Kolam {rings} rings", KolamType.MARGAZHI_KOLAM)
        grid_size = 2 * rings + 3
        pattern.set_grid(grid_size, grid_size, spacing=1.2)
        
        curve_gen = CurveGenerator(pattern.grid)
        center = Point2D((grid_size-1) * 0.6, (grid_size-1) * 0.6)
        
        # Generate concentric rings
        for ring in range(1, rings + 1):
            radius = ring * 0.8
            
            # Circular ring
            ring_points = []
            for i in range(segments * 8):
                angle = i * 2 * math.pi / (segments * 8)
                x = center.x + radius * math.cos(angle)
                y = center.y + radius * math.sin(angle)
                ring_points.append(Point2D(x, y))
            
            pattern.add_curve(ring_points)
            
            # Add radial spokes for this ring
            for spoke in range(segments):
                angle = spoke * 2 * math.pi / segments
                spoke_points = []
                
                # From center to ring
                for t in range(10):
                    r = (t / 9) * radius
                    x = center.x + r * math.cos(angle)
                    y = center.y + r * math.sin(angle)
                    spoke_points.append(Point2D(x, y))
                
                pattern.add_curve(spoke_points)
        
        pattern.analyze_symmetries()
        return pattern
    
    def _generate_connecting_curve(self, start: Point2D, end: Point2D) -> List[Point2D]:
        """Generate a smooth connecting curve between two points"""
        points = []
        num_points = 20
        
        # Simple bezier-like curve
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # Add some curvature
            mid_x = (start.x + end.x) / 2
            mid_y = (start.y + end.y) / 2
            curve_height = 0.5
            
            # Quadratic bezier curve
            x = (1-t)**2 * start.x + 2*(1-t)*t * mid_x + t**2 * end.x
            y = (1-t)**2 * start.y + 2*(1-t)*t * (mid_y + curve_height) + t**2 * end.y
            
            points.append(Point2D(x, y))
        
        return points


def main():
    """Demonstrate the pattern recognition and generation capabilities"""
    print("Kolam Pattern Generator")
    print("=" * 30)
    
    generator = KolamGenerator()
    
    # Generate different types of Kolam patterns
    patterns = [
        generator.generate_pulli_kolam(5, 5, "basic"),
        generator.generate_pulli_kolam(7, 7, "diamond"),
        generator.generate_sikku_kolam(3),
        generator.generate_kambi_kolam(6, "geometric"),
        generator.generate_kambi_kolam(8, "star"),
        generator.generate_flower_kolam(8, 3),
        generator.generate_mandala_kolam(4, 8)
    ]
    
    # Analyze each pattern
    for pattern in patterns:
        print(f"\nPattern: {pattern.name}")
        print(f"Type: {pattern.kolam_type.value}")
        print(f"Curves: {len(pattern.curves)}")
        print(f"Symmetries: {[s.value for s in pattern.symmetries]}")
        
        bbox_min, bbox_max = pattern.get_bounding_box()
        print(f"Size: {bbox_max.x - bbox_min.x:.1f} x {bbox_max.y - bbox_min.y:.1f}")
    
    # Test pattern recognition
    recognizer = PatternRecognizer()
    test_pattern = patterns[0]
    
    if test_pattern.curves:
        curve_types = recognizer.detect_curve_types(test_pattern.curves[0])
        print(f"\nCurve analysis for {test_pattern.name}: {curve_types}")


if __name__ == "__main__":
    main()
