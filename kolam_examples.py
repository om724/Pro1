"""
Kolam Examples and Interactive Interface
=======================================

This module provides specific examples of traditional Kolam patterns and
an interactive interface for generating and customizing patterns.
"""

import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from kolam_geometry import Point2D, KolamPattern, KolamType
from kolam_generator import KolamGenerator
from kolam_visualizer import KolamVisualizer


class TraditionalPatterns:
    """Collection of specific traditional Kolam patterns"""
    
    def __init__(self):
        self.generator = KolamGenerator()
    
    def create_basic_pulli_kolam(self) -> KolamPattern:
        """Create a basic 5x5 pulli kolam with square loops"""
        return self.generator.generate_pulli_kolam(5, 5, "basic")
    
    def create_diamond_pulli_kolam(self) -> KolamPattern:
        """Create a diamond-shaped pulli kolam"""
        return self.generator.generate_pulli_kolam(9, 9, "diamond")
    
    def create_rangoli_flower(self) -> KolamPattern:
        """Create a flower-style rangoli pattern"""
        pattern = KolamPattern("Traditional Rangoli Flower", KolamType.MARGAZHI_KOLAM)
        pattern.set_grid(9, 9, spacing=1.0)
        
        from kolam_geometry import CurveGenerator
        curve_gen = CurveGenerator(pattern.grid)
        center = Point2D(4, 4)  # Center of 9x9 grid
        
        # Create multiple concentric flower patterns
        for layer in range(1, 4):
            radius = layer * 1.2
            petals = 8 if layer == 1 else 12
            petal_curve = curve_gen.generate_petal_pattern(center, radius, petals)
            pattern.add_curve(petal_curve)
        
        # Add decorative dots around the flower
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            dot_x = center.x + 3.5 * math.cos(rad)
            dot_y = center.y + 3.5 * math.sin(rad)
            
            # Small circular decoration
            decoration = []
            for i in range(16):
                dec_angle = i * 2 * math.pi / 16
                x = dot_x + 0.3 * math.cos(dec_angle)
                y = dot_y + 0.3 * math.sin(dec_angle)
                decoration.append(Point2D(x, y))
            pattern.add_curve(decoration)
        
        pattern.analyze_symmetries()
        return pattern
    
    def create_deepavali_special(self) -> KolamPattern:
        """Create a special Deepavali kolam with multiple elements"""
        pattern = KolamPattern("Deepavali Special Kolam", KolamType.MARGAZHI_KOLAM)
        pattern.set_grid(11, 11, spacing=1.0)
        
        from kolam_geometry import CurveGenerator, SymmetryAnalyzer, SymmetryType
        curve_gen = CurveGenerator(pattern.grid)
        center = Point2D(5, 5)  # Center of 11x11 grid
        
        # Central star pattern
        star_points = []
        for i in range(16):
            angle = i * 2 * math.pi / 16
            radius = 1.5 if i % 2 == 0 else 0.8  # Alternating radii for star effect
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            star_points.append(Point2D(x, y))
        pattern.add_curve(star_points)
        
        # Surrounding mandala rings
        for ring in range(1, 4):
            ring_radius = 2 + ring * 0.8
            ring_points = []
            segments = 24 + ring * 8
            
            for i in range(segments):
                angle = i * 2 * math.pi / segments
                x = center.x + ring_radius * math.cos(angle)
                y = center.y + ring_radius * math.sin(angle)
                ring_points.append(Point2D(x, y))
            pattern.add_curve(ring_points)
        
        # Corner decorations
        corners = [(2, 2), (2, 8), (8, 2), (8, 8)]
        for corner_r, corner_c in corners:
            corner_center = Point2D(corner_c, corner_r)
            corner_decoration = curve_gen.generate_spiral_pattern(
                corner_center, radius=0.8, turns=1.5
            )
            pattern.add_curve(corner_decoration)
        
        pattern.analyze_symmetries()
        return pattern
    
    def create_pongal_kolam(self) -> KolamPattern:
        """Create a traditional Pongal festival kolam"""
        pattern = KolamPattern("Pongal Festival Kolam", KolamType.MARGAZHI_KOLAM)
        pattern.set_grid(13, 13, spacing=0.8)
        
        from kolam_geometry import CurveGenerator
        curve_gen = CurveGenerator(pattern.grid)
        center = Point2D(6 * 0.8, 6 * 0.8)  # Center adjustment for spacing
        
        # Traditional rice plant motif (stylized)
        for branch in range(8):
            angle = branch * 2 * math.pi / 8
            
            # Main stem
            stem_points = []
            for t in range(20):
                radius = 0.5 + t * 0.15
                stem_angle = angle + t * 0.1  # Slight curve
                x = center.x + radius * math.cos(stem_angle)
                y = center.y + radius * math.sin(stem_angle)
                stem_points.append(Point2D(x, y))
            
            pattern.add_curve(stem_points)
            
            # Rice grain decorations along the stem
            for grain in range(5):
                grain_radius = 1.5 + grain * 0.6
                grain_angle = angle + grain * 0.08
                grain_center = Point2D(
                    center.x + grain_radius * math.cos(grain_angle),
                    center.y + grain_radius * math.sin(grain_angle)
                )
                
                # Small oval for rice grain
                grain_curve = []
                for i in range(12):
                    oval_angle = i * 2 * math.pi / 12
                    x = grain_center.x + 0.2 * math.cos(oval_angle)
                    y = grain_center.y + 0.15 * math.sin(oval_angle)
                    grain_curve.append(Point2D(x, y))
                pattern.add_curve(grain_curve)
        
        # Central prosperity symbol
        prosperity_symbol = curve_gen.generate_spiral_pattern(center, 0.8, 2)
        pattern.add_curve(prosperity_symbol)
        
        pattern.analyze_symmetries()
        return pattern
    
    def create_geometric_sikku(self) -> KolamPattern:
        """Create a geometric sikku kolam with interlocking patterns"""
        pattern = KolamPattern("Geometric Sikku Kolam", KolamType.SIKKU_KOLAM)
        pattern.set_grid(7, 7, spacing=1.5)
        
        # Create interlocking square spirals
        centers = [
            Point2D(2*1.5, 2*1.5),  # Top-left
            Point2D(4*1.5, 2*1.5),  # Top-right
            Point2D(2*1.5, 4*1.5),  # Bottom-left
            Point2D(4*1.5, 4*1.5),  # Bottom-right
        ]
        
        from kolam_geometry import CurveGenerator
        curve_gen = CurveGenerator(pattern.grid)
        
        for i, center in enumerate(centers):
            # Spiral in alternating directions
            turns = 1.5 + i * 0.5
            spiral = curve_gen.generate_spiral_pattern(center, 1.0, turns)
            pattern.add_curve(spiral)
        
        # Connecting paths between spirals
        connections = [
            (centers[0], centers[1]),  # Top horizontal
            (centers[2], centers[3]),  # Bottom horizontal
            (centers[0], centers[2]),  # Left vertical
            (centers[1], centers[3]),  # Right vertical
        ]
        
        for start, end in connections:
            connection_points = []
            for t in range(20):
                t_norm = t / 19
                # Bezier curve for smooth connection
                mid_x = (start.x + end.x) / 2
                mid_y = (start.y + end.y) / 2 + 0.5  # Slight arch
                
                x = (1-t_norm)**2 * start.x + 2*(1-t_norm)*t_norm * mid_x + t_norm**2 * end.x
                y = (1-t_norm)**2 * start.y + 2*(1-t_norm)*t_norm * mid_y + t_norm**2 * end.y
                connection_points.append(Point2D(x, y))
            
            pattern.add_curve(connection_points)
        
        pattern.analyze_symmetries()
        return pattern


class KolamInteractiveGUI:
    """Interactive GUI for creating and customizing Kolam patterns"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kolam Pattern Generator & Analyzer")
        self.root.geometry("1200x800")
        
        self.generator = KolamGenerator()
        self.visualizer = KolamVisualizer(figsize=(8, 8))
        self.traditional = TraditionalPatterns()
        self.current_pattern = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frames
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pattern type selection
        pattern_frame = ttk.LabelFrame(control_frame, text="Pattern Type", padding=10)
        pattern_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pattern_type = tk.StringVar(value="pulli")
        pattern_types = [
            ("Pulli Kolam", "pulli"),
            ("Sikku Kolam", "sikku"),
            ("Kambi Kolam", "kambi"),
            ("Flower Pattern", "flower"),
            ("Mandala", "mandala"),
            ("Traditional Examples", "traditional")
        ]
        
        for text, value in pattern_types:
            ttk.Radiobutton(pattern_frame, text=text, variable=self.pattern_type, 
                          value=value, command=self.update_parameters).pack(anchor=tk.W)
        
        # Parameters frame
        self.params_frame = ttk.LabelFrame(control_frame, text="Parameters", padding=10)
        self.params_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.setup_parameter_controls()
        
        # Traditional patterns selection
        self.trad_frame = ttk.LabelFrame(control_frame, text="Traditional Patterns", padding=10)
        self.trad_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.traditional_pattern = tk.StringVar(value="basic_pulli")
        trad_patterns = [
            ("Basic Pulli", "basic_pulli"),
            ("Diamond Pulli", "diamond_pulli"),
            ("Rangoli Flower", "rangoli_flower"),
            ("Deepavali Special", "deepavali_special"),
            ("Pongal Kolam", "pongal_kolam"),
            ("Geometric Sikku", "geometric_sikku")
        ]
        
        for text, value in trad_patterns:
            ttk.Radiobutton(self.trad_frame, text=text, variable=self.traditional_pattern, 
                          value=value).pack(anchor=tk.W)
        
        # Initially hide traditional frame
        self.trad_frame.pack_forget()
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Generate Pattern", 
                  command=self.generate_pattern).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Analyze Symmetries", 
                  command=self.analyze_pattern).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Save as PNG", 
                  command=self.save_png).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Export as SVG", 
                  command=self.export_svg).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Analysis Report", 
                  command=self.create_report).pack(fill=tk.X, pady=(0, 5))
        
        # Canvas for matplotlib
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to generate patterns")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_parameter_controls(self):
        """Setup parameter control widgets"""
        # Clear existing widgets
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        # Grid size controls
        ttk.Label(self.params_frame, text="Grid Size:").pack(anchor=tk.W)
        size_frame = ttk.Frame(self.params_frame)
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(size_frame, text="Rows:").pack(side=tk.LEFT)
        self.rows_var = tk.IntVar(value=5)
        ttk.Spinbox(size_frame, from_=3, to=15, textvariable=self.rows_var, 
                   width=5).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(size_frame, text="Cols:").pack(side=tk.LEFT)
        self.cols_var = tk.IntVar(value=5)
        ttk.Spinbox(size_frame, from_=3, to=15, textvariable=self.cols_var, 
                   width=5).pack(side=tk.LEFT, padx=(5, 0))
        
        # Pattern-specific controls
        self.complexity_var = tk.IntVar(value=3)
        self.petals_var = tk.IntVar(value=8)
        self.layers_var = tk.IntVar(value=3)
        self.rings_var = tk.IntVar(value=4)
        
        # These will be shown/hidden based on pattern type
        self.complexity_frame = ttk.Frame(self.params_frame)
        ttk.Label(self.complexity_frame, text="Complexity:").pack(anchor=tk.W)
        ttk.Scale(self.complexity_frame, from_=1, to=5, orient=tk.HORIZONTAL,
                 variable=self.complexity_var).pack(fill=tk.X)
        
        self.petals_frame = ttk.Frame(self.params_frame)
        ttk.Label(self.petals_frame, text="Petals:").pack(anchor=tk.W)
        ttk.Scale(self.petals_frame, from_=4, to=16, orient=tk.HORIZONTAL,
                 variable=self.petals_var).pack(fill=tk.X)
        
        self.layers_frame = ttk.Frame(self.params_frame)
        ttk.Label(self.layers_frame, text="Layers:").pack(anchor=tk.W)
        ttk.Scale(self.layers_frame, from_=1, to=5, orient=tk.HORIZONTAL,
                 variable=self.layers_var).pack(fill=tk.X)
        
        self.rings_frame = ttk.Frame(self.params_frame)
        ttk.Label(self.rings_frame, text="Rings:").pack(anchor=tk.W)
        ttk.Scale(self.rings_frame, from_=2, to=8, orient=tk.HORIZONTAL,
                 variable=self.rings_var).pack(fill=tk.X)
        
        # Pattern style for pulli kolam
        self.style_frame = ttk.Frame(self.params_frame)
        ttk.Label(self.style_frame, text="Style:").pack(anchor=tk.W)
        self.pulli_style = tk.StringVar(value="basic")
        ttk.Radiobutton(self.style_frame, text="Basic", variable=self.pulli_style, 
                       value="basic").pack(anchor=tk.W)
        ttk.Radiobutton(self.style_frame, text="Diamond", variable=self.pulli_style, 
                       value="diamond").pack(anchor=tk.W)
        
        self.update_parameters()
        
    def update_parameters(self):
        """Update visible parameters based on pattern type"""
        # Hide all parameter frames
        for frame in [self.complexity_frame, self.petals_frame, 
                     self.layers_frame, self.rings_frame, self.style_frame]:
            frame.pack_forget()
        
        # Hide/show traditional patterns frame
        if self.pattern_type.get() == "traditional":
            self.trad_frame.pack(fill=tk.X, pady=(0, 10))
            self.params_frame.pack_forget()
        else:
            self.trad_frame.pack_forget()
            self.params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Show relevant parameters
        pattern_type = self.pattern_type.get()
        
        if pattern_type == "pulli":
            self.style_frame.pack(fill=tk.X, pady=(0, 5))
        elif pattern_type == "sikku":
            self.complexity_frame.pack(fill=tk.X, pady=(0, 5))
        elif pattern_type == "flower":
            self.petals_frame.pack(fill=tk.X, pady=(0, 5))
            self.layers_frame.pack(fill=tk.X, pady=(0, 5))
        elif pattern_type == "mandala":
            self.rings_frame.pack(fill=tk.X, pady=(0, 5))
        
    def generate_pattern(self):
        """Generate pattern based on current settings"""
        try:
            self.status_var.set("Generating pattern...")
            self.root.update()
            
            pattern_type = self.pattern_type.get()
            
            if pattern_type == "traditional":
                self.current_pattern = self.generate_traditional_pattern()
            else:
                self.current_pattern = self.generate_parametric_pattern()
            
            self.display_pattern()
            self.status_var.set(f"Generated: {self.current_pattern.name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate pattern: {str(e)}")
            self.status_var.set("Error occurred")
    
    def generate_traditional_pattern(self) -> KolamPattern:
        """Generate a traditional pattern"""
        trad_type = self.traditional_pattern.get()
        
        pattern_map = {
            "basic_pulli": self.traditional.create_basic_pulli_kolam,
            "diamond_pulli": self.traditional.create_diamond_pulli_kolam,
            "rangoli_flower": self.traditional.create_rangoli_flower,
            "deepavali_special": self.traditional.create_deepavali_special,
            "pongal_kolam": self.traditional.create_pongal_kolam,
            "geometric_sikku": self.traditional.create_geometric_sikku
        }
        
        return pattern_map[trad_type]()
    
    def generate_parametric_pattern(self) -> KolamPattern:
        """Generate a parametric pattern"""
        pattern_type = self.pattern_type.get()
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        
        if pattern_type == "pulli":
            style = self.pulli_style.get()
            return self.generator.generate_pulli_kolam(rows, cols, style)
        elif pattern_type == "sikku":
            complexity = self.complexity_var.get()
            return self.generator.generate_sikku_kolam(complexity)
        elif pattern_type == "kambi":
            return self.generator.generate_kambi_kolam(max(rows, cols), "geometric")
        elif pattern_type == "flower":
            petals = self.petals_var.get()
            layers = self.layers_var.get()
            return self.generator.generate_flower_kolam(petals, layers)
        elif pattern_type == "mandala":
            rings = self.rings_var.get()
            return self.generator.generate_mandala_kolam(rings, 8)
        
        # Fallback
        return self.generator.generate_pulli_kolam(5, 5, "basic")
    
    def display_pattern(self):
        """Display the current pattern on canvas"""
        if not self.current_pattern:
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#FFF8DC')
        
        # Draw pattern using visualizer methods
        if self.current_pattern.grid:
            self.visualizer._draw_dots(ax, self.current_pattern.grid)
        
        self.visualizer._draw_curves(ax, self.current_pattern.curves)
        self.visualizer._customize_plot(ax, self.current_pattern, self.current_pattern.name)
        
        self.canvas.draw()
    
    def analyze_pattern(self):
        """Analyze and display pattern symmetries"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "Please generate a pattern first")
            return
        
        # Re-analyze symmetries
        self.current_pattern.analyze_symmetries()
        
        # Display analysis
        analysis_text = f"""Pattern Analysis: {self.current_pattern.name}

Type: {self.current_pattern.kolam_type.value}
Curves: {len(self.current_pattern.curves)}
Total Points: {sum(len(curve) for curve in self.current_pattern.curves)}

Detected Symmetries:
"""
        
        if self.current_pattern.symmetries:
            for sym in self.current_pattern.symmetries:
                analysis_text += f"• {sym.value}\n"
        else:
            analysis_text += "• No clear symmetries detected\n"
        
        bbox_min, bbox_max = self.current_pattern.get_bounding_box()
        analysis_text += f"\nDimensions: {bbox_max.x - bbox_min.x:.1f} × {bbox_max.y - bbox_min.y:.1f}"
        
        messagebox.showinfo("Pattern Analysis", analysis_text)
    
    def save_png(self):
        """Save current pattern as PNG"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "Please generate a pattern first")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            self.visualizer.save_pattern(self.current_pattern, filename, format='png')
            messagebox.showinfo("Success", f"Pattern saved as {filename}")
    
    def export_svg(self):
        """Export current pattern as SVG"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "Please generate a pattern first")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        
        if filename:
            self.visualizer.export_svg(self.current_pattern, filename)
            messagebox.showinfo("Success", f"Pattern exported as {filename}")
    
    def create_report(self):
        """Create detailed analysis report"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "Please generate a pattern first")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            analysis = self.visualizer.create_analysis_report(self.current_pattern, filename)
            messagebox.showinfo("Report Created", f"Analysis report saved as {filename}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Run examples and start interactive GUI"""
    print("Kolam Examples and Interactive Interface")
    print("=" * 45)
    
    # Create traditional patterns
    traditional = TraditionalPatterns()
    visualizer = KolamVisualizer(figsize=(6, 6))
    
    # Generate and display traditional patterns
    patterns = [
        ("Basic Pulli Kolam", traditional.create_basic_pulli_kolam()),
        ("Rangoli Flower", traditional.create_rangoli_flower()),
        ("Deepavali Special", traditional.create_deepavali_special()),
        ("Pongal Festival Kolam", traditional.create_pongal_kolam()),
        ("Geometric Sikku", traditional.create_geometric_sikku())
    ]
    
    print("\nGenerated Traditional Patterns:")
    for name, pattern in patterns:
        print(f"- {name}: {len(pattern.curves)} curves, {[s.value for s in pattern.symmetries]}")
    
    # Ask user if they want to see visualizations or start GUI
    try:
        choice = input("\nChoose an option:\n1. View pattern gallery\n2. Start interactive GUI\n3. Exit\nChoice (1-3): ")
        
        if choice == "1":
            print("\nDisplaying pattern gallery...")
            visualizer.create_comparison_plot([p[1] for p in patterns], cols=3)
        elif choice == "2":
            print("\nStarting interactive GUI...")
            app = KolamInteractiveGUI()
            app.run()
        else:
            print("Exiting...")
    
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
