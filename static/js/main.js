// Main JavaScript - Common functionality
// ====================================

$(document).ready(function() {
    // Initialize tooltips globally
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
            && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });

    // Auto-dismiss alerts after 5 seconds
    $('.alert').each(function() {
        var alert = $(this);
        if (alert.hasClass('auto-dismiss') || alert.find('.btn-close').length) {
            setTimeout(function() {
                if (alert.hasClass('show')) {
                    alert.alert('close');
                }
            }, 5000);
        }
    });

    // Add loading states to buttons on form submission
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').each(function() {
            var btn = $(this);
            var originalText = btn.html();
            btn.prop('disabled', true)
               .html('<i class="fas fa-spinner fa-spin me-2"></i>Loading...');
            
            // Restore button after 10 seconds (safety fallback)
            setTimeout(function() {
                btn.prop('disabled', false).html(originalText);
            }, 10000);
        });
    });

    // Fade in animations for elements with fade-in-up class
    $('.fade-in-up').each(function(index) {
        var element = $(this);
        setTimeout(function() {
            element.addClass('animate__animated animate__fadeInUp');
        }, index * 100);
    });

    // Back to top button
    var backToTop = $('<button class="btn btn-primary btn-floating" id="back-to-top" title="Back to top" style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; display: none; border-radius: 50%; width: 50px; height: 50px;"><i class="fas fa-chevron-up"></i></button>');
    $('body').append(backToTop);

    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });

    $('#back-to-top').click(function() {
        $('html, body').animate({scrollTop: 0}, 500);
        return false;
    });
});
