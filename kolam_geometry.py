"""
Kolam Geometry Module
====================

This module implements the core geometric principles and mathematical foundations
for analyzing and generating Kolam designs.

Key Design Principles Identified:
1. Grid-based structure with dots as anchor points
2. Symmetrical patterns (rotational, reflectional, translational)
3. Continuous curves that loop around dots
4. Mathematical relationships between dot spacing and curve patterns
5. Recursive and fractal-like properties in complex designs
"""

import numpy as np
import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class SymmetryType(Enum):
    """Types of symmetry found in Kolam designs"""
    ROTATIONAL_2 = "2-fold rotational"
    ROTATIONAL_4 = "4-fold rotational"
    ROTATIONAL_8 = "8-fold rotational"
    REFLECTIONAL_VERTICAL = "vertical reflection"
    REFLECTIONAL_HORIZONTAL = "horizontal reflection"
    REFLECTIONAL_DIAGONAL = "diagonal reflection"
    TRANSLATIONAL = "translational"
    POINT = "point symmetry"


class KolamType(Enum):
    """Different types of Kolam patterns"""
    PULLI_KOLAM = "dot kolam"  # Simple dot patterns
    KAMBI_KOLAM = "line kolam"  # Wire-frame like patterns
    SIKKU_KOLAM = "knot kolam"  # Complex interlocking patterns
    CHIKKU_KOLAM = "small kolam"  # Minimal patterns
    MARGAZHI_KOLAM = "festival kolam"  # Complex ceremonial patterns


@dataclass
class Point2D:
    """Represents a 2D point"""
    x: float
    y: float
    
    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Point2D(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def rotate(self, angle_rad, center=None):
        """Rotate point around center (or origin if None)"""
        if center is None:
            center = Point2D(0, 0)
        
        # Translate to origin
        translated = self - center
        
        # Rotate
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotated = Point2D(
            translated.x * cos_a - translated.y * sin_a,
            translated.x * sin_a + translated.y * cos_a
        )
        
        # Translate back
        return rotated + center


class DotGrid:
    """Represents the fundamental dot grid structure of Kolam designs"""
    
    def __init__(self, rows: int, cols: int, spacing: float = 1.0):
        self.rows = rows
        self.cols = cols
        self.spacing = spacing
        self.dots = self._generate_grid()
        
    def _generate_grid(self) -> List[List[Point2D]]:
        """Generate the grid of dots"""
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                x = j * self.spacing
                y = i * self.spacing
                row.append(Point2D(x, y))
            grid.append(row)
        return grid
    
    def get_dot(self, row: int, col: int) -> Optional[Point2D]:
        """Get dot at specific grid position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.dots[row][col]
        return None
    
    def get_neighbors(self, row: int, col: int, radius: int = 1) -> List[Point2D]:
        """Get neighboring dots within radius"""
        neighbors = []
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                if dr == 0 and dc == 0:
                    continue
                dot = self.get_dot(row + dr, col + dc)
                if dot:
                    neighbors.append(dot)
        return neighbors
    
    def get_all_dots(self) -> List[Point2D]:
        """Get all dots as a flat list"""
        all_dots = []
        for row in self.dots:
            all_dots.extend(row)
        return all_dots


class CurveGenerator:
    """Generates curves that follow Kolam design principles"""
    
    def __init__(self, grid: DotGrid):
        self.grid = grid
    
    def generate_loop_around_dots(self, dot_positions: List[Tuple[int, int]], 
                                 curve_radius: float = 0.3) -> List[Point2D]:
        """
        Generate a continuous curve that loops around specified dots
        This follows the traditional Kolam principle of unbroken lines
        """
        if not dot_positions:
            return []
        
        curve_points = []
        
        for i, (row, col) in enumerate(dot_positions):
            dot = self.grid.get_dot(row, col)
            if not dot:
                continue
                
            # Generate circular arc around each dot
            num_points = 20
            start_angle = 0
            end_angle = 2 * math.pi
            
            if i < len(dot_positions) - 1:
                # Connect to next dot
                next_dot = self.grid.get_dot(dot_positions[i + 1][0], dot_positions[i + 1][1])
                if next_dot:
                    # Calculate angle towards next dot
                    dx = next_dot.x - dot.x
                    dy = next_dot.y - dot.y
                    angle_to_next = math.atan2(dy, dx)
                    start_angle = angle_to_next + math.pi/2
                    end_angle = start_angle + 3*math.pi/2
            
            for j in range(num_points):
                angle = start_angle + (end_angle - start_angle) * j / (num_points - 1)
                x = dot.x + curve_radius * math.cos(angle)
                y = dot.y + curve_radius * math.sin(angle)
                curve_points.append(Point2D(x, y))
        
        return curve_points
    
    def generate_spiral_pattern(self, center: Point2D, radius: float, 
                               turns: float = 3) -> List[Point2D]:
        """Generate spiral patterns common in Kolam designs"""
        points = []
        num_points = int(100 * turns)
        
        for i in range(num_points):
            t = i / num_points
            angle = t * turns * 2 * math.pi
            r = radius * t
            
            x = center.x + r * math.cos(angle)
            y = center.y + r * math.sin(angle)
            points.append(Point2D(x, y))
        
        return points
    
    def generate_petal_pattern(self, center: Point2D, radius: float, 
                              num_petals: int = 8) -> List[Point2D]:
        """Generate petal patterns using rose curves"""
        points = []
        num_points = 200
        
        for i in range(num_points):
            t = i / num_points * 2 * math.pi
            # Rose curve equation: r = radius * cos(k*t) where k = num_petals/2
            k = num_petals / 2
            r = radius * abs(math.cos(k * t))
            
            x = center.x + r * math.cos(t)
            y = center.y + r * math.sin(t)
            points.append(Point2D(x, y))
        
        return points


class SymmetryAnalyzer:
    """Analyzes and applies symmetry operations to Kolam patterns"""
    
    @staticmethod
    def detect_symmetries(points: List[Point2D]) -> List[SymmetryType]:
        """Detect symmetries in a given set of points"""
        symmetries = []
        
        if not points:
            return symmetries
        
        # Calculate centroid
        centroid = Point2D(
            sum(p.x for p in points) / len(points),
            sum(p.y for p in points) / len(points)
        )
        
        # Test for rotational symmetry
        for fold in [2, 4, 8]:
            if SymmetryAnalyzer._test_rotational_symmetry(points, centroid, fold):
                symmetries.append(getattr(SymmetryType, f"ROTATIONAL_{fold}"))
        
        # Test for reflectional symmetry
        if SymmetryAnalyzer._test_reflection_symmetry(points, centroid, "vertical"):
            symmetries.append(SymmetryType.REFLECTIONAL_VERTICAL)
        if SymmetryAnalyzer._test_reflection_symmetry(points, centroid, "horizontal"):
            symmetries.append(SymmetryType.REFLECTIONAL_HORIZONTAL)
        
        return symmetries
    
    @staticmethod
    def _test_rotational_symmetry(points: List[Point2D], center: Point2D, 
                                 fold: int, tolerance: float = 0.1) -> bool:
        """Test if points have n-fold rotational symmetry"""
        angle = 2 * math.pi / fold
        rotated_points = [p.rotate(angle, center) for p in points]
        
        # Check if rotated points match original points (within tolerance)
        for rp in rotated_points:
            found_match = False
            for op in points:
                if rp.distance_to(op) < tolerance:
                    found_match = True
                    break
            if not found_match:
                return False
        return True
    
    @staticmethod
    def _test_reflection_symmetry(points: List[Point2D], center: Point2D, 
                                 axis: str, tolerance: float = 0.1) -> bool:
        """Test if points have reflection symmetry along specified axis"""
        if axis == "vertical":
            reflected_points = [Point2D(2*center.x - p.x, p.y) for p in points]
        elif axis == "horizontal":
            reflected_points = [Point2D(p.x, 2*center.y - p.y) for p in points]
        else:
            return False
        
        # Check if reflected points match original points (within tolerance)
        for rp in reflected_points:
            found_match = False
            for op in points:
                if rp.distance_to(op) < tolerance:
                    found_match = True
                    break
            if not found_match:
                return False
        return True
    
    @staticmethod
    def apply_symmetry(points: List[Point2D], center: Point2D, 
                      symmetry_type: SymmetryType) -> List[Point2D]:
        """Apply symmetry transformation to create symmetric patterns"""
        if symmetry_type == SymmetryType.ROTATIONAL_4:
            all_points = list(points)
            for i in range(1, 4):
                angle = i * math.pi / 2
                rotated = [p.rotate(angle, center) for p in points]
                all_points.extend(rotated)
            return all_points
        elif symmetry_type == SymmetryType.REFLECTIONAL_VERTICAL:
            reflected = [Point2D(2*center.x - p.x, p.y) for p in points]
            return points + reflected
        elif symmetry_type == SymmetryType.REFLECTIONAL_HORIZONTAL:
            reflected = [Point2D(p.x, 2*center.y - p.y) for p in points]
            return points + reflected
        
        return points


class KolamPattern:
    """Represents a complete Kolam pattern with its properties"""
    
    def __init__(self, name: str, kolam_type: KolamType):
        self.name = name
        self.kolam_type = kolam_type
        self.grid = None
        self.curves = []
        self.symmetries = []
        self.properties = {}
    
    def set_grid(self, rows: int, cols: int, spacing: float = 1.0):
        """Set the underlying dot grid"""
        self.grid = DotGrid(rows, cols, spacing)
    
    def add_curve(self, curve_points: List[Point2D]):
        """Add a curve to the pattern"""
        self.curves.append(curve_points)
    
    def analyze_symmetries(self):
        """Analyze symmetries in the pattern"""
        all_points = []
        for curve in self.curves:
            all_points.extend(curve)
        
        if all_points:
            self.symmetries = SymmetryAnalyzer.detect_symmetries(all_points)
    
    def get_bounding_box(self) -> Tuple[Point2D, Point2D]:
        """Get bounding box of the pattern"""
        if not self.curves:
            return Point2D(0, 0), Point2D(0, 0)
        
        all_points = []
        for curve in self.curves:
            all_points.extend(curve)
        
        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)
        
        return Point2D(min_x, min_y), Point2D(max_x, max_y)


def main():
    """Demonstrate the core geometry classes"""
    print("Kolam Geometry Analysis System")
    print("=" * 40)
    
    # Create a sample grid
    grid = DotGrid(5, 5, spacing=2.0)
    print(f"Created {grid.rows}x{grid.cols} dot grid")
    
    # Generate a curve pattern
    curve_gen = CurveGenerator(grid)
    
    # Create a simple square loop pattern
    square_dots = [(1, 1), (1, 3), (3, 3), (3, 1), (1, 1)]
    loop_curve = curve_gen.generate_loop_around_dots(square_dots)
    print(f"Generated loop curve with {len(loop_curve)} points")
    
    # Create a spiral pattern
    center = Point2D(5, 5)
    spiral_curve = curve_gen.generate_spiral_pattern(center, radius=3, turns=2)
    print(f"Generated spiral curve with {len(spiral_curve)} points")
    
    # Create a pattern and analyze it
    pattern = KolamPattern("Sample Square Loop", KolamType.PULLI_KOLAM)
    pattern.set_grid(5, 5, 2.0)
    pattern.add_curve(loop_curve)
    pattern.analyze_symmetries()
    
    print(f"Pattern symmetries: {[s.value for s in pattern.symmetries]}")
    
    bbox_min, bbox_max = pattern.get_bounding_box()
    print(f"Bounding box: ({bbox_min.x:.2f}, {bbox_min.y:.2f}) to ({bbox_max.x:.2f}, {bbox_max.y:.2f})")


if __name__ == "__main__":
    main()
