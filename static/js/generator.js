// Kolam Pattern Generator - JavaScript
// ===================================

class KolamGenerator {
    constructor() {
        this.currentPatternId = null;
        this.zoomLevel = 1.0;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateParameterDisplay();
    }

    bindEvents() {
        // Pattern type change
        $('input[name="patternType"]').change(() => {
            this.updateParameterDisplay();
        });

        // Generate button
        $('#generate-btn').click(() => {
            this.generatePattern();
        });

        // Analyze button
        $('#analyze-btn').click(() => {
            this.analyzeSymmetries();
        });

        // Export buttons
        $('#export-png-btn').click(() => {
            this.exportPattern('png');
        });

        $('#export-svg-btn').click(() => {
            this.exportPattern('svg');
        });

        // Zoom controls
        $('#zoom-in-btn').click(() => {
            this.zoomIn();
        });

        $('#zoom-out-btn').click(() => {
            this.zoomOut();
        });

        $('#reset-zoom-btn').click(() => {
            this.resetZoom();
        });

        // Pattern display click for zoom
        $(document).on('click', '#pattern-display img', () => {
            this.toggleZoom();
        });
    }

    updateParameterDisplay() {
        const selectedType = $('input[name="patternType"]:checked').val();
        
        // Hide all parameter groups
        $('.parameter-group').addClass('d-none');
        
        // Show relevant parameter group
        $(`#${selectedType}-params`).removeClass('d-none');
    }

    async generatePattern() {
        const patternType = $('input[name="patternType"]:checked').val();
        const parameters = this.getPatternParameters(patternType);

        // Show loading state
        this.showLoading();
        this.disableControls();

        try {
            const response = await fetch('/api/generate_pattern', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: patternType,
                    parameters: parameters
                })
            });

            const data = await response.json();

            if (data.success) {
                this.displayPattern(data.image, data.name);
                this.displayPatternInfo(data.analysis);
                this.currentPatternId = data.pattern_id;
                this.enableControls();
                this.showSuccess('Pattern generated successfully!');
            } else {
                this.showError(data.error || 'Failed to generate pattern');
            }
        } catch (error) {
            console.error('Error generating pattern:', error);
            this.showError('Network error occurred. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    getPatternParameters(patternType) {
        const params = {};

        switch (patternType) {
            case 'pulli':
                params.rows = parseInt($('#rows').val());
                params.cols = parseInt($('#cols').val());
                params.style = $('input[name="pulliStyle"]:checked').val();
                break;

            case 'sikku':
                params.complexity = parseInt($('#complexity').val());
                break;

            case 'kambi':
                params.size = parseInt($('#size').val());
                params.style = $('input[name="kambiStyle"]:checked').val();
                break;

            case 'flower':
                params.petals = parseInt($('#petals').val());
                params.layers = parseInt($('#layers').val());
                break;

            case 'mandala':
                params.rings = parseInt($('#rings').val());
                params.segments = parseInt($('#segments').val());
                break;
        }

        return params;
    }

    displayPattern(imageData, patternName) {
        const patternDisplay = $('#pattern-display');
        
        patternDisplay.html(`
            <img src="${imageData}" alt="${patternName}" class="img-fluid">
        `).addClass('has-pattern');

        // Add fade in animation
        patternDisplay.find('img').addClass('fade-in-up');
    }

    displayPatternInfo(analysis) {
        const patternInfo = $('#pattern-info');
        const patternDetails = $('#pattern-details');

        let symmetriesHtml = '';
        if (analysis.symmetries && analysis.symmetries.length > 0) {
            symmetriesHtml = analysis.symmetries.map(sym => 
                `<span class="symmetry-badge">${sym}</span>`
            ).join(' ');
        } else {
            symmetriesHtml = '<span class="text-muted">None detected</span>';
        }

        const detailsHtml = `
            <div class="pattern-info-item">
                <span class="pattern-info-label">Name:</span>
                <span class="pattern-info-value">${analysis.name}</span>
            </div>
            <div class="pattern-info-item">
                <span class="pattern-info-label">Type:</span>
                <span class="pattern-info-value">${analysis.type}</span>
            </div>
            <div class="pattern-info-item">
                <span class="pattern-info-label">Curves:</span>
                <span class="pattern-info-value">${analysis.curves_count}</span>
            </div>
            <div class="pattern-info-item">
                <span class="pattern-info-label">Points:</span>
                <span class="pattern-info-value">${analysis.total_points.toLocaleString()}</span>
            </div>
            <div class="pattern-info-item">
                <span class="pattern-info-label">Dimensions:</span>
                <span class="pattern-info-value">${analysis.dimensions.width} × ${analysis.dimensions.height}</span>
            </div>
            ${analysis.grid ? `
            <div class="pattern-info-item">
                <span class="pattern-info-label">Grid:</span>
                <span class="pattern-info-value">${analysis.grid.rows}×${analysis.grid.cols}</span>
            </div>
            ` : ''}
            <div class="pattern-info-item">
                <span class="pattern-info-label">Symmetries:</span>
                <div class="mt-1">${symmetriesHtml}</div>
            </div>
        `;

        patternDetails.html(detailsHtml);
        patternInfo.show().addClass('fade-in-up');
    }

    async analyzeSymmetries() {
        if (!this.currentPatternId) {
            this.showError('Please generate a pattern first');
            return;
        }

        $('#analyze-btn').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...');

        try {
            const response = await fetch(`/api/analyze_symmetries/${this.currentPatternId}`);
            const data = await response.json();

            if (data.success) {
                this.displaySymmetryAnalysis(data.symmetry_info);
                this.showSuccess('Symmetry analysis completed!');
            } else {
                this.showError(data.error || 'Failed to analyze symmetries');
            }
        } catch (error) {
            console.error('Error analyzing symmetries:', error);
            this.showError('Network error occurred. Please try again.');
        } finally {
            $('#analyze-btn').prop('disabled', false).html('<i class="fas fa-search me-2"></i>Analyze Symmetries');
        }
    }

    displaySymmetryAnalysis(symmetryInfo) {
        const symmetryAnalysis = $('#symmetry-analysis');
        const symmetryResults = $('#symmetry-results');

        let symmetriesHtml = '';
        if (symmetryInfo.symmetries && symmetryInfo.symmetries.length > 0) {
            symmetriesHtml = symmetryInfo.symmetries.map(sym => 
                `<span class="symmetry-badge">${sym}</span>`
            ).join(' ');
        } else {
            symmetriesHtml = '<span class="text-muted">No symmetries detected</span>';
        }

        const analysisHtml = `
            <div class="row">
                <div class="col-md-8">
                    <h6><i class="fas fa-balance-scale me-2"></i>Detected Symmetries</h6>
                    <div class="mb-3">${symmetriesHtml}</div>
                    
                    <div class="row">
                        <div class="col-6">
                            <div class="text-center p-3 bg-light rounded">
                                <i class="fas fa-sync-alt fa-2x ${symmetryInfo.analysis.has_rotational ? 'text-success' : 'text-muted'}"></i>
                                <div class="mt-2">
                                    <strong>Rotational</strong><br>
                                    <small class="${symmetryInfo.analysis.has_rotational ? 'text-success' : 'text-muted'}">
                                        ${symmetryInfo.analysis.has_rotational ? 'Detected' : 'Not found'}
                                    </small>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-center p-3 bg-light rounded">
                                <i class="fas fa-arrows-alt-h fa-2x ${symmetryInfo.analysis.has_reflectional ? 'text-success' : 'text-muted'}"></i>
                                <div class="mt-2">
                                    <strong>Reflectional</strong><br>
                                    <small class="${symmetryInfo.analysis.has_reflectional ? 'text-success' : 'text-muted'}">
                                        ${symmetryInfo.analysis.has_reflectional ? 'Detected' : 'Not found'}
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center">
                        <img src="${symmetryInfo.symmetry_image}" alt="Symmetry Analysis" class="img-fluid rounded">
                        <small class="text-muted d-block mt-2">Symmetry indicators overlaid on pattern</small>
                    </div>
                </div>
            </div>
        `;

        symmetryResults.html(analysisHtml);
        symmetryAnalysis.show().addClass('fade-in-up');
    }

    async exportPattern(format) {
        if (!this.currentPatternId) {
            this.showError('Please generate a pattern first');
            return;
        }

        const exportBtn = $(`#export-${format}-btn`);
        const originalText = exportBtn.html();
        
        exportBtn.prop('disabled', true).html(`<i class="fas fa-spinner fa-spin me-1"></i>${format.toUpperCase()}`);

        try {
            // Create a temporary link and trigger download
            const link = document.createElement('a');
            link.href = `/api/export_pattern/${this.currentPatternId}/${format}`;
            link.download = `kolam_pattern.${format}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            this.showSuccess(`Pattern exported as ${format.toUpperCase()}!`);
        } catch (error) {
            console.error('Error exporting pattern:', error);
            this.showError('Failed to export pattern');
        } finally {
            setTimeout(() => {
                exportBtn.prop('disabled', false).html(originalText);
            }, 2000);
        }
    }

    // Zoom functionality
    zoomIn() {
        this.zoomLevel = Math.min(this.zoomLevel * 1.2, 3.0);
        this.applyZoom();
    }

    zoomOut() {
        this.zoomLevel = Math.max(this.zoomLevel / 1.2, 0.5);
        this.applyZoom();
    }

    resetZoom() {
        this.zoomLevel = 1.0;
        this.applyZoom();
    }

    toggleZoom() {
        this.zoomLevel = this.zoomLevel === 1.0 ? 2.0 : 1.0;
        this.applyZoom();
    }

    applyZoom() {
        const img = $('#pattern-display img');
        if (img.length) {
            img.css('transform', `scale(${this.zoomLevel})`);
            img.css('transition', 'transform 0.3s ease');
        }
    }

    // UI Helper Methods
    showLoading() {
        $('#pattern-display').hide();
        $('#loading').removeClass('d-none');
    }

    hideLoading() {
        $('#loading').addClass('d-none');
        $('#pattern-display').show();
    }

    disableControls() {
        $('#generate-btn').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i>Generating...');
        $('#analyze-btn, #export-png-btn, #export-svg-btn').prop('disabled', true);
    }

    enableControls() {
        $('#generate-btn').prop('disabled', false).html('<i class="fas fa-magic me-2"></i>Generate Pattern');
        $('#analyze-btn, #export-png-btn, #export-svg-btn').prop('disabled', false);
    }

    showError(message) {
        $('#error-message').text(message);
        $('#errorModal').modal('show');
    }

    showSuccess(message) {
        // Create temporary success alert
        const alert = $(`
            <div class="alert alert-success alert-dismissible fade show success-message" role="alert">
                <i class="fas fa-check-circle"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);

        // Add to top of pattern display area
        $('#pattern-display').closest('.card').before(alert);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alert.alert('close');
        }, 5000);
    }
}

// Initialize when document is ready
$(document).ready(function() {
    window.kolamGenerator = new KolamGenerator();
    
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Add loading animation to cards
    $('.card').each(function(index) {
        $(this).css('animation-delay', `${index * 0.1}s`).addClass('fade-in-up');
    });
});
