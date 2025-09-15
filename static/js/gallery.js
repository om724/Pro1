// Gallery JavaScript functionality
// ===============================

class KolamGallery {
    constructor() {
        this.currentPatternId = null;
        this.culturalInfo = {
            'basic_pulli': {
                significance: 'The foundation of all Kolam art, representing simplicity and daily spiritual practice.',
                region: 'Common throughout Tamil Nadu',
                occasion: 'Daily morning rituals',
                symbolism: 'Dots represent the universe, loops represent the cycle of life'
            },
            'diamond_pulli': {
                significance: 'Represents expansion of consciousness and spiritual growth.',
                region: 'Popular in urban Tamil Nadu',
                occasion: 'Festivals and special occasions',
                symbolism: 'Diamond shape symbolizes the four directions and cosmic balance'
            },
            'rangoli_flower': {
                significance: 'Symbol of beauty, growth, and the flowering of human potential.',
                region: 'Common across South India',
                occasion: 'Wedding ceremonies and spring festivals',
                symbolism: 'Petals represent the unfolding of spiritual awareness'
            },
            'deepavali_special': {
                significance: 'Elaborate patterns to welcome light and prosperity during the festival of lights.',
                region: 'Throughout India with regional variations',
                occasion: 'Diwali/Deepavali celebrations',
                symbolism: 'Stars and lights represent victory of light over darkness'
            },
            'pongal_kolam': {
                significance: 'Celebrates the harvest season and gratitude to nature.',
                region: 'Tamil Nadu harvest regions',
                occasion: 'Pongal harvest festival',
                symbolism: 'Rice and grain motifs represent abundance and prosperity'
            },
            'geometric_sikku': {
                significance: 'Complex interlocking patterns representing the interconnectedness of all life.',
                region: 'Traditional villages of Tamil Nadu',
                occasion: 'Temple festivals and spiritual gatherings',
                symbolism: 'Interlocking elements represent unity and interdependence'
            }
        };
        this.init();
    }

    init() {
        this.loadPatternPreviews();
        this.bindEvents();
    }

    bindEvents() {
        // View pattern buttons
        $('.view-pattern-btn').on('click', (e) => {
            const patternName = $(e.target).data('pattern');
            this.showPatternModal(patternName);
        });

        // Gallery card clicks
        $('.gallery-card').on('click', (e) => {
            if (!$(e.target).hasClass('btn') && !$(e.target).closest('.btn').length) {
                const patternName = $(e.currentTarget).data('pattern');
                this.showPatternModal(patternName);
            }
        });

        // Modal export buttons
        $('#modal-export-png').on('click', () => {
            this.exportModalPattern('png');
        });

        $('#modal-export-svg').on('click', () => {
            this.exportModalPattern('svg');
        });
    }

    async loadPatternPreviews() {
        const patterns = ['basic_pulli', 'diamond_pulli', 'rangoli_flower', 
                         'deepavali_special', 'pongal_kolam', 'geometric_sikku'];

        for (const pattern of patterns) {
            try {
                const response = await fetch(`/api/traditional_pattern/${pattern}`);
                const data = await response.json();

                if (data.success) {
                    // Update the pattern card with actual image
                    const card = $(`.gallery-card[data-pattern="${pattern}"]`);
                    const placeholder = card.find('.pattern-placeholder');
                    
                    placeholder.html(`
                        <img src="${data.image}" alt="${data.name}" class="img-fluid">
                    `);
                }
            } catch (error) {
                console.error(`Error loading pattern ${pattern}:`, error);
                // Keep the loading spinner if failed
            }
        }
    }

    async showPatternModal(patternName) {
        const modal = $('#patternModal');
        const modalTitle = $('#patternModalLabel');
        const modalDisplay = $('#modal-pattern-display');
        const modalInfo = $('#modal-pattern-info');
        const modalCultural = $('#modal-cultural-info');

        // Reset modal content
        modalDisplay.html('<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading pattern...</span></div>');
        modalInfo.html('<div class="spinner-border spinner-border-sm text-primary" role="status"><span class="visually-hidden">Loading...</span></div>');
        modalCultural.html('');

        // Show modal
        modal.modal('show');

        try {
            const response = await fetch(`/api/traditional_pattern/${patternName}`);
            const data = await response.json();

            if (data.success) {
                this.currentPatternId = data.pattern_id;

                // Update modal title
                modalTitle.text(`Pattern Details - ${data.name}`);

                // Update pattern display
                modalDisplay.html(`
                    <img src="${data.image}" alt="${data.name}" class="img-fluid">
                `);

                // Update pattern information
                const analysis = data.analysis;
                let symmetriesHtml = '';
                if (analysis.symmetries && analysis.symmetries.length > 0) {
                    symmetriesHtml = analysis.symmetries.map(sym => 
                        `<span class="badge bg-info me-1 mb-1">${sym}</span>`
                    ).join('');
                } else {
                    symmetriesHtml = '<span class="text-muted">None detected</span>';
                }

                const infoHtml = `
                    <div class="mb-2">
                        <strong>Name:</strong> ${analysis.name}
                    </div>
                    <div class="mb-2">
                        <strong>Type:</strong> ${analysis.type}
                    </div>
                    <div class="mb-2">
                        <strong>Curves:</strong> ${analysis.curves_count}
                    </div>
                    <div class="mb-2">
                        <strong>Points:</strong> ${analysis.total_points.toLocaleString()}
                    </div>
                    <div class="mb-2">
                        <strong>Dimensions:</strong> ${analysis.dimensions.width.toFixed(1)} × ${analysis.dimensions.height.toFixed(1)}
                    </div>
                    ${analysis.grid ? `
                    <div class="mb-2">
                        <strong>Grid:</strong> ${analysis.grid.rows}×${analysis.grid.cols}
                    </div>
                    ` : ''}
                    <div class="mb-2">
                        <strong>Symmetries:</strong><br>
                        ${symmetriesHtml}
                    </div>
                `;

                modalInfo.html(infoHtml);

                // Update cultural information
                const cultural = this.culturalInfo[patternName];
                if (cultural) {
                    const culturalHtml = `
                        <div class="mb-3">
                            <strong>Cultural Significance:</strong>
                            <p class="text-muted">${cultural.significance}</p>
                        </div>
                        <div class="mb-2">
                            <strong>Region:</strong> ${cultural.region}
                        </div>
                        <div class="mb-2">
                            <strong>Occasion:</strong> ${cultural.occasion}
                        </div>
                        <div class="mb-2">
                            <strong>Symbolism:</strong>
                            <p class="text-muted small">${cultural.symbolism}</p>
                        </div>
                    `;
                    modalCultural.html(culturalHtml);
                } else {
                    modalCultural.html('<p class="text-muted">Cultural information not available.</p>');
                }

            } else {
                throw new Error(data.error || 'Failed to load pattern');
            }
        } catch (error) {
            console.error('Error loading pattern details:', error);
            modalDisplay.html(`
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Failed to load pattern details. Please try again.
                </div>
            `);
            modalInfo.html('<p class="text-danger">Error loading pattern information.</p>');
        }
    }

    async exportModalPattern(format) {
        if (!this.currentPatternId) {
            this.showError('No pattern selected for export');
            return;
        }

        const exportBtn = $(`#modal-export-${format}`);
        const originalText = exportBtn.html();
        
        exportBtn.prop('disabled', true).html(`<i class="fas fa-spinner fa-spin me-1"></i>${format.toUpperCase()}`);

        try {
            // Create a temporary link and trigger download
            const link = document.createElement('a');
            link.href = `/api/export_pattern/${this.currentPatternId}/${format}`;
            link.download = `traditional_kolam.${format}`;
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

    showError(message) {
        const alert = $(`
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);

        $('.container').prepend(alert);
        setTimeout(() => alert.alert('close'), 5000);
    }

    showSuccess(message) {
        const alert = $(`
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="fas fa-check-circle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);

        $('.container').prepend(alert);
        setTimeout(() => alert.alert('close'), 5000);
    }
}

// Initialize when document is ready
$(document).ready(function() {
    window.kolamGallery = new KolamGallery();
    
    // Add staggered animation to gallery cards
    $('.gallery-card').each(function(index) {
        $(this).css('animation-delay', `${index * 0.1}s`).addClass('fade-in-up');
    });

    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
});
