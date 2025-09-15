"""
Kolam Pattern Generator - Web Application
=========================================

Flask-based web application for generating and analyzing traditional Kolam patterns.
Provides an interactive web interface for pattern creation, visualization, and export.
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import base64
import io
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for web
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

# Import our Kolam modules
from kolam_geometry import Point2D, KolamPattern, KolamType
from kolam_generator import KolamGenerator
from kolam_visualizer import KolamVisualizer
from kolam_examples import TraditionalPatterns

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kolam_patterns_2024'

# Initialize our generators
generator = KolamGenerator()
visualizer = KolamVisualizer(figsize=(10, 10))
traditional = TraditionalPatterns()

# Global storage for current pattern (in production, use proper session management)
current_patterns = {}

@app.route('/')
def index():
    """Main page with pattern generator interface"""
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    """Gallery page showing traditional patterns"""
    return render_template('gallery.html')

@app.route('/about')
def about():
    """About page with information on Kolam patterns"""
    return render_template('about.html')

@app.route('/api/generate_pattern', methods=['POST'])
def generate_pattern():
    """Generate a Kolam pattern based on parameters"""
    try:
        data = request.get_json()
        pattern_type = data.get('type', 'pulli')
        params = data.get('parameters', {})
        
        # Generate pattern based on type
        if pattern_type == 'pulli':
            rows = params.get('rows', 5)
            cols = params.get('cols', 5)
            style = params.get('style', 'basic')
            pattern = generator.generate_pulli_kolam(rows, cols, style)
            
        elif pattern_type == 'sikku':
            complexity = params.get('complexity', 3)
            pattern = generator.generate_sikku_kolam(complexity)
            
        elif pattern_type == 'kambi':
            size = params.get('size', 6)
            style = params.get('style', 'geometric')
            pattern = generator.generate_kambi_kolam(size, style)
            
        elif pattern_type == 'flower':
            petals = params.get('petals', 8)
            layers = params.get('layers', 3)
            pattern = generator.generate_flower_kolam(petals, layers)
            
        elif pattern_type == 'mandala':
            rings = params.get('rings', 4)
            segments = params.get('segments', 8)
            pattern = generator.generate_mandala_kolam(rings, segments)
            
        else:
            pattern = generator.generate_pulli_kolam(5, 5, 'basic')
        
        # Store pattern for later use
        pattern_id = f"pattern_{datetime.now().timestamp()}"
        current_patterns[pattern_id] = pattern
        
        # Generate visualization
        image_data = generate_pattern_image(pattern)
        
        # Analyze pattern properties
        analysis = analyze_pattern(pattern)
        
        return jsonify({
            'success': True,
            'pattern_id': pattern_id,
            'image': image_data,
            'analysis': analysis,
            'name': pattern.name
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/traditional_pattern/<pattern_name>')
def get_traditional_pattern(pattern_name):
    """Get a specific traditional pattern"""
    try:
        pattern_map = {
            'basic_pulli': traditional.create_basic_pulli_kolam,
            'diamond_pulli': traditional.create_diamond_pulli_kolam,
            'rangoli_flower': traditional.create_rangoli_flower,
            'deepavali_special': traditional.create_deepavali_special,
            'pongal_kolam': traditional.create_pongal_kolam,
            'geometric_sikku': traditional.create_geometric_sikku
        }
        
        if pattern_name in pattern_map:
            pattern = pattern_map[pattern_name]()
            
            # Store pattern
            pattern_id = f"traditional_{pattern_name}_{datetime.now().timestamp()}"
            current_patterns[pattern_id] = pattern
            
            # Generate visualization
            image_data = generate_pattern_image(pattern)
            
            # Analyze pattern
            analysis = analyze_pattern(pattern)
            
            return jsonify({
                'success': True,
                'pattern_id': pattern_id,
                'image': image_data,
                'analysis': analysis,
                'name': pattern.name
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Pattern not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export_pattern/<pattern_id>/<format>')
def export_pattern(pattern_id, format):
    """Export pattern in specified format"""
    try:
        if pattern_id not in current_patterns:
            return jsonify({'success': False, 'error': 'Pattern not found'}), 404
        
        pattern = current_patterns[pattern_id]
        
        if format == 'png':
            # Generate high-resolution PNG
            img_buffer = io.BytesIO()
            fig = Figure(figsize=(12, 12), dpi=300)
            ax = fig.add_subplot(111)
            ax.set_facecolor('#FFF8DC')
            
            # Draw pattern
            if pattern.grid:
                visualizer._draw_dots(ax, pattern.grid)
            visualizer._draw_curves(ax, pattern.curves)
            visualizer._customize_plot(ax, pattern, pattern.name)
            
            fig.savefig(img_buffer, format='png', bbox_inches='tight', 
                       facecolor='#FFF8DC', dpi=300)
            img_buffer.seek(0)
            
            return send_file(img_buffer, mimetype='image/png', 
                           as_attachment=True, 
                           download_name=f'{pattern.name.replace(" ", "_")}.png')
            
        elif format == 'svg':
            # Generate SVG
            svg_content = generate_svg_content(pattern)
            svg_buffer = io.BytesIO(svg_content.encode('utf-8'))
            
            return send_file(svg_buffer, mimetype='image/svg+xml',
                           as_attachment=True,
                           download_name=f'{pattern.name.replace(" ", "_")}.svg')
        
        else:
            return jsonify({'success': False, 'error': 'Unsupported format'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze_symmetries/<pattern_id>')
def analyze_symmetries(pattern_id):
    """Perform detailed symmetry analysis on pattern"""
    try:
        if pattern_id not in current_patterns:
            return jsonify({'success': False, 'error': 'Pattern not found'}), 404
        
        pattern = current_patterns[pattern_id]
        pattern.analyze_symmetries()
        
        # Generate symmetry visualization
        image_data = generate_symmetry_image(pattern)
        
        symmetry_info = {
            'symmetries': [s.value for s in pattern.symmetries],
            'symmetry_image': image_data,
            'analysis': {
                'has_rotational': any('rotational' in s.value.lower() for s in pattern.symmetries),
                'has_reflectional': any('reflection' in s.value.lower() for s in pattern.symmetries),
                'symmetry_count': len(pattern.symmetries)
            }
        }
        
        return jsonify({
            'success': True,
            'symmetry_info': symmetry_info
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_pattern_image(pattern, show_symmetry=False):
    """Generate base64 encoded image of the pattern"""
    fig = Figure(figsize=(8, 8), facecolor='#FFF8DC')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFF8DC')
    
    # Draw pattern components
    if pattern.grid:
        visualizer._draw_dots(ax, pattern.grid)
    visualizer._draw_curves(ax, pattern.curves)
    
    if show_symmetry:
        visualizer._draw_symmetry_indicators(ax, pattern)
    
    visualizer._customize_plot(ax, pattern, pattern.name)
    
    # Convert to base64
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', 
               facecolor='#FFF8DC', dpi=150)
    img_buffer.seek(0)
    
    img_data = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close(fig)
    
    return f"data:image/png;base64,{img_data}"

def generate_symmetry_image(pattern):
    """Generate image showing symmetry indicators"""
    fig = Figure(figsize=(8, 8), facecolor='#FFF8DC')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFF8DC')
    
    # Draw pattern with symmetry indicators
    if pattern.grid:
        visualizer._draw_dots(ax, pattern.grid, alpha=0.5)
    visualizer._draw_curves(ax, pattern.curves, alpha=0.7)
    visualizer._draw_symmetry_indicators(ax, pattern)
    visualizer._customize_plot(ax, pattern, f"{pattern.name} - Symmetry Analysis")
    
    # Convert to base64
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', 
               facecolor='#FFF8DC', dpi=150)
    img_buffer.seek(0)
    
    img_data = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close(fig)
    
    return f"data:image/png;base64,{img_data}"

def generate_svg_content(pattern):
    """Generate SVG content for the pattern"""
    bbox_min, bbox_max = pattern.get_bounding_box()
    width = bbox_max.x - bbox_min.x + 2
    height = bbox_max.y - bbox_min.y + 2
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{width*50}" height="{height*50}" 
     viewBox="{bbox_min.x-1} {bbox_min.y-1} {width} {height}">
     
  <rect width="100%" height="100%" fill="#FFF8DC"/>
  
  <!-- Pattern: {pattern.name} -->
  
  <!-- Grid dots -->
'''
    
    # Add dots
    if pattern.grid:
        for dot in pattern.grid.get_all_dots():
            svg_content += f'  <circle cx="{dot.x}" cy="{dot.y}" r="0.05" fill="#8B4513" opacity="0.7"/>\n'
    
    svg_content += '\n  <!-- Curves -->\n'
    
    # Add curves
    for i, curve in enumerate(pattern.curves):
        if curve:
            path_data = f'M {curve[0].x},{curve[0].y}'
            for point in curve[1:]:
                path_data += f' L {point.x},{point.y}'
            
            svg_content += f'''  <path d="{path_data}" 
                stroke="#FF4500" stroke-width="0.1" 
                fill="none" stroke-linecap="round" stroke-linejoin="round"/>
'''
    
    svg_content += '\n</svg>'
    
    return svg_content

def analyze_pattern(pattern):
    """Analyze pattern properties"""
    bbox_min, bbox_max = pattern.get_bounding_box()
    
    analysis = {
        'name': pattern.name,
        'type': pattern.kolam_type.value,
        'curves_count': len(pattern.curves),
        'total_points': sum(len(curve) for curve in pattern.curves),
        'dimensions': {
            'width': round(bbox_max.x - bbox_min.x, 2),
            'height': round(bbox_max.y - bbox_min.y, 2)
        }
    }
    
    if pattern.grid:
        analysis['grid'] = {
            'rows': pattern.grid.rows,
            'cols': pattern.grid.cols,
            'spacing': pattern.grid.spacing
        }
    
    # Analyze symmetries
    pattern.analyze_symmetries()
    analysis['symmetries'] = [s.value for s in pattern.symmetries]
    
    return analysis

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
