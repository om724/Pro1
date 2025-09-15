# Kolam Design Analysis and Generation System

A comprehensive Python system for analyzing, generating, and recreating traditional Kolam patterns using mathematical principles and computational geometry.

## Overview

Kolams (also known as Rangoli, Muggu, and Rangavalli) are traditional Indian decorative patterns created using rice flour or colored powders. This system implements the underlying mathematical principles to:

1. **Analyze existing Kolam designs** - Identify symmetries, patterns, and geometric properties
2. **Generate new patterns** - Create Kolam designs based on mathematical rules
3. **Visualize and export** - Render patterns and save them in various formats
4. **Interactive exploration** - GUI tool for experimenting with different parameters

## Key Features

### Mathematical Foundations Implemented

- **Grid-based structure** with dots as anchor points
- **Symmetry operations** (rotational, reflectional, translational)
- **Continuous curve generation** following traditional rules
- **Pattern recognition algorithms** for analyzing existing designs
- **Fractal and recursive properties** in complex patterns

### Kolam Types Supported

1. **Pulli Kolam** - Dot-based patterns with simple geometric loops
2. **Sikku Kolam** - Complex interlocking and knot patterns  
3. **Kambi Kolam** - Line-based wireframe patterns
4. **Flower/Petal patterns** - Rose curve based designs
5. **Mandala patterns** - Concentric circular designs
6. **Traditional festival patterns** - Specific cultural designs

### Core Capabilities

- Pattern generation with customizable parameters
- Symmetry detection and analysis
- Multiple export formats (PNG, SVG)
- Interactive GUI for real-time pattern creation
- Detailed analysis reports with mathematical properties
- Traditional pattern library with authentic examples

## Installation and Requirements

### Prerequisites

```bash
pip install numpy matplotlib tkinter dataclasses typing
```

### Required Python Version
- Python 3.7 or higher (for dataclasses support)

### File Structure
```
kolam_system/
├── kolam_geometry.py      # Core geometric classes and mathematical foundations
├── kolam_generator.py     # Pattern generation algorithms  
├── kolam_visualizer.py    # Visualization and export functionality
├── kolam_examples.py      # Traditional patterns and GUI interface
├── main_kolam.py          # Main entry point script
└── README.md              # This documentation
```

## Quick Start

### Basic Usage

```python
from kolam_generator import KolamGenerator
from kolam_visualizer import KolamVisualizer

# Create generator and visualizer
generator = KolamGenerator()
visualizer = KolamVisualizer()

# Generate a basic pattern
pattern = generator.generate_pulli_kolam(5, 5, "basic")

# Visualize the pattern
visualizer.visualize_pattern(pattern)

# Save as image
visualizer.save_pattern(pattern, "my_kolam.png")
```

### Interactive GUI

```python
from kolam_examples import KolamInteractiveGUI

# Start the interactive interface
app = KolamInteractiveGUI()
app.run()
```

### Command Line Interface

```bash
python main_kolam.py
```

## Core Classes and API

### KolamPattern
Represents a complete Kolam pattern with its properties.

```python
pattern = KolamPattern("My Pattern", KolamType.PULLI_KOLAM)
pattern.set_grid(5, 5, spacing=2.0)
pattern.add_curve(curve_points)
pattern.analyze_symmetries()
```

### DotGrid
Manages the fundamental dot grid structure.

```python
grid = DotGrid(rows=5, cols=5, spacing=1.0)
dot = grid.get_dot(row=2, col=2)
neighbors = grid.get_neighbors(row=2, col=2)
```

### CurveGenerator
Generates curves following Kolam design principles.

```python
curve_gen = CurveGenerator(grid)

# Loop around dots
loop = curve_gen.generate_loop_around_dots([(1,1), (1,3), (3,3), (3,1)])

# Spiral pattern
spiral = curve_gen.generate_spiral_pattern(center, radius=2, turns=3)

# Petal pattern (rose curve)
petals = curve_gen.generate_petal_pattern(center, radius=2, num_petals=8)
```

### SymmetryAnalyzer
Detects and applies symmetry operations.

```python
# Detect symmetries
symmetries = SymmetryAnalyzer.detect_symmetries(points)

# Apply symmetry transformation
symmetric_points = SymmetryAnalyzer.apply_symmetry(
    points, center, SymmetryType.ROTATIONAL_4
)
```

### PatternRecognizer
Analyzes existing patterns to identify design principles.

```python
recognizer = PatternRecognizer()

# Analyze grid structure
grid_info = recognizer.analyze_grid_structure(points)

# Detect curve types
curve_types = recognizer.detect_curve_types(curve_points)
# Returns: ['circular', 'spiral', 'petal', 'linear']
```

## Pattern Generation Examples

### Traditional Patterns

```python
from kolam_examples import TraditionalPatterns

traditional = TraditionalPatterns()

# Generate specific traditional patterns
basic_pulli = traditional.create_basic_pulli_kolam()
rangoli_flower = traditional.create_rangoli_flower()
deepavali_special = traditional.create_deepavali_special()
pongal_kolam = traditional.create_pongal_kolam()
geometric_sikku = traditional.create_geometric_sikku()
```

### Parametric Generation

```python
generator = KolamGenerator()

# Pulli Kolam variations
basic_pulli = generator.generate_pulli_kolam(5, 5, "basic")
diamond_pulli = generator.generate_pulli_kolam(7, 7, "diamond")

# Complex interlocking patterns
sikku_simple = generator.generate_sikku_kolam(complexity=2)
sikku_complex = generator.generate_sikku_kolam(complexity=5)

# Geometric line patterns  
geometric_lines = generator.generate_kambi_kolam(6, "geometric")
star_pattern = generator.generate_kambi_kolam(8, "star")

# Flower and mandala patterns
flower_8_petals = generator.generate_flower_kolam(num_petals=8, layers=3)
mandala_pattern = generator.generate_mandala_kolam(rings=4, segments=8)
```

## Visualization and Export

### Display Options

```python
visualizer = KolamVisualizer()

# Basic visualization
visualizer.visualize_pattern(pattern)

# With customization options
visualizer.visualize_pattern(
    pattern, 
    show_grid=True, 
    show_dots=True, 
    show_symmetry=True,
    title="My Custom Kolam"
)
```

### Export Formats

```python
# Save as high-resolution PNG
visualizer.save_pattern(pattern, "kolam.png", dpi=300, format='png')

# Export as scalable SVG
visualizer.export_svg(pattern, "kolam.svg")

# Create detailed analysis report
analysis = visualizer.create_analysis_report(pattern, "analysis.png")
```

### Comparison and Gallery

```python
# Compare multiple patterns
patterns = [pattern1, pattern2, pattern3, pattern4]
visualizer.create_comparison_plot(patterns, cols=2)

# Animation (basic progressive reveal)
visualizer.animate_generation(pattern, steps=50)
```

## Mathematical Principles

### Symmetry Types Detected

1. **Rotational Symmetry**
   - 2-fold, 4-fold, 8-fold rotational symmetry
   - Automatic detection with configurable tolerance

2. **Reflectional Symmetry**
   - Vertical, horizontal, diagonal reflection axes
   - Multiple axes supported

3. **Translational Symmetry**
   - Repeating patterns with constant offset
   - Grid-based translation detection

### Curve Generation Mathematics

1. **Loop Generation**
   - Continuous curves around dot sequences
   - Smooth transitions between dots
   - Configurable curve radius

2. **Spiral Patterns**
   - Archimedean spiral: r = a + bθ
   - Customizable turns and growth rate

3. **Rose Curves (Petal Patterns)**
   - Equation: r = a·cos(k·θ)
   - Variable petal count and size

4. **Bézier Connections**
   - Smooth curve connections
   - Quadratic and cubic Bézier curves

### Grid Mathematics

- **Dot Spacing**: Configurable uniform or non-uniform grids
- **Neighbor Calculation**: Distance-based neighbor finding
- **Coordinate Transformations**: Grid to Cartesian conversion
- **Boundary Handling**: Edge and corner case management

## Interactive GUI Features

### Pattern Type Selection
- Radio buttons for different Kolam types
- Dynamic parameter panels based on selection
- Real-time parameter updates

### Parameter Controls
- **Grid Size**: Adjustable rows and columns
- **Complexity**: Slider for pattern complexity
- **Petals/Layers**: Controls for flower patterns  
- **Rings/Segments**: Mandala pattern parameters
- **Style Options**: Basic, diamond, geometric styles

### Traditional Pattern Library
- Pre-defined authentic patterns
- Cultural context and significance
- One-click generation

### Analysis Tools
- **Symmetry Detection**: Automatic symmetry analysis
- **Pattern Properties**: Curve count, point count, dimensions
- **Visual Reports**: Multi-panel analysis views

### Export Options
- **PNG Export**: High-resolution raster images
- **SVG Export**: Vector graphics for scaling
- **Analysis Reports**: Comprehensive pattern documentation

## Advanced Usage

### Custom Pattern Creation

```python
# Create custom pattern from scratch
pattern = KolamPattern("Custom Design", KolamType.MARGAZHI_KOLAM)
pattern.set_grid(7, 7, spacing=1.5)

# Add custom curves
curve_gen = CurveGenerator(pattern.grid)
custom_curve = []

# Manual curve point generation
for angle in range(0, 360, 10):
    rad = math.radians(angle)
    x = center.x + 2 * math.cos(rad)
    y = center.y + 2 * math.sin(rad)
    custom_curve.append(Point2D(x, y))

pattern.add_curve(custom_curve)
pattern.analyze_symmetries()
```

### Pattern Recognition and Analysis

```python
# Analyze existing pattern data
recognizer = PatternRecognizer()

# Load points from external source (e.g., image processing)
points = load_points_from_image("existing_kolam.jpg")

# Analyze the pattern
grid_structure = recognizer.analyze_grid_structure(points)
curve_types = recognizer.detect_curve_types(points)

print(f"Grid: {grid_structure}")
print(f"Curve types: {curve_types}")
```

### Symmetry Manipulation

```python
# Apply specific symmetries to create variations
base_points = generate_basic_pattern()

# Create 4-fold rotational symmetry
rotated = SymmetryAnalyzer.apply_symmetry(
    base_points, center, SymmetryType.ROTATIONAL_4
)

# Create reflection symmetry
reflected = SymmetryAnalyzer.apply_symmetry(
    base_points, center, SymmetryType.REFLECTIONAL_VERTICAL
)

# Combine symmetries
combined_pattern = rotated + reflected
```

## Cultural and Mathematical Context

### Traditional Significance

Kolams serve multiple purposes in Indian culture:
- **Spiritual**: Sacred geometry and meditation
- **Social**: Community participation and artistic expression  
- **Mathematical**: Complex geometric relationships and patterns
- **Seasonal**: Festival-specific designs and celebrations

### Mathematical Connections

The system implements several mathematical concepts:
- **Group Theory**: Symmetry groups and transformations
- **Topology**: Continuous curves and connectivity
- **Fractal Geometry**: Self-similar and recursive patterns
- **Computational Geometry**: Point-in-polygon, curve fitting
- **Graph Theory**: Dot connectivity and path finding

### Design Principles Identified

1. **Grid Foundation**: All patterns based on underlying dot grids
2. **Continuous Lines**: Unbroken curves following specific rules
3. **Symmetry**: Multiple types of symmetry for aesthetic balance
4. **Recursion**: Patterns within patterns at multiple scales
5. **Cultural Motifs**: Traditional symbols and seasonal themes

## Performance and Scalability

### Optimization Features
- **Efficient point storage** using dataclasses
- **Vectorized operations** with NumPy where possible
- **Lazy evaluation** for large pattern generation
- **Configurable precision** for symmetry detection

### Memory Usage
- Patterns scale approximately O(n²) with grid size
- Curve complexity affects memory linearly
- SVG export more memory efficient than raster

### Computational Complexity
- **Grid generation**: O(rows × cols)
- **Symmetry detection**: O(n² × k) where k is symmetry types
- **Curve generation**: O(points × curves)
- **Visualization**: O(n) for point plotting

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   Solution: Ensure all dependencies are installed
   pip install numpy matplotlib tkinter
   ```

2. **GUI Not Opening**
   ```
   Solution: Check tkinter installation
   python -m tkinter  # Should open test window
   ```

3. **Empty Pattern Display**
   ```
   Solution: Check pattern has curves added
   print(f"Curves: {len(pattern.curves)}")
   ```

4. **Symmetry Not Detected**
   ```
   Solution: Adjust tolerance in SymmetryAnalyzer
   SymmetryAnalyzer._test_rotational_symmetry(..., tolerance=0.2)
   ```

### Debug Mode

```python
# Enable verbose output
import logging
logging.basicConfig(level=logging.DEBUG)

# Check pattern properties
print(f"Pattern: {pattern.name}")
print(f"Grid: {pattern.grid.rows}x{pattern.grid.cols}")
print(f"Curves: {len(pattern.curves)}")
print(f"Total points: {sum(len(c) for c in pattern.curves)}")
```

## Future Enhancements

### Planned Features
- **3D Kolam patterns** with depth and perspective
- **Animation sequences** showing pattern creation process
- **Machine learning** pattern classification and generation
- **Image import** for analyzing photographed Kolams
- **Color and texture** support for realistic rendering
- **Mobile app** version for touch-based interaction

### Research Opportunities
- **Pattern grammar** formal language for Kolam description
- **Cultural variations** regional differences in style
- **Algorithmic composition** AI-generated traditional patterns
- **Mathematical optimization** most efficient pattern generation
- **Cognitive studies** pattern recognition and human perception

## Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest tests/`
4. Follow PEP 8 style guidelines

### Code Structure
- Keep mathematical logic in `kolam_geometry.py`
- Pattern algorithms in `kolam_generator.py`  
- Visualization separate in `kolam_visualizer.py`
- GUI and examples in `kolam_examples.py`

### Testing
- Unit tests for all mathematical functions
- Visual regression tests for pattern generation
- Performance benchmarks for large patterns
- Cross-platform compatibility testing

## License and Credits

### Acknowledgments
- Traditional Kolam artists and cultural heritage
- Mathematical foundations from computational geometry
- Open source visualization libraries (matplotlib)
- Indian cultural and artistic traditions

### References
- Siromoney, G. et al. "Kolam Patterns and Array Grammars"
- Nagarajan, K. "Threshold Kolam: A Mathematical Perspective"  
- Various ethnomathematical studies on South Indian patterns
- Computational geometry and symmetry group literature

---

*This system respectfully implements traditional Kolam patterns using modern computational methods, preserving the mathematical beauty and cultural significance of this ancient art form.*
#   P r o 1  
 