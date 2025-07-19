// Somali English Blog - Main JavaScript
// Professional client-side functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initializeSearch();
    initializeFormValidation();
    initializeLazyLoading();
    initializeTooltips();
    initializeScrollToTop();
    initializeSmoothScrolling();
    initializeImageModal();
    
    console.log('Somali English Blog initialized successfully');
});

/**
 * Enhanced search functionality
 */
function initializeSearch() {
    const searchForms = document.querySelectorAll('form[action*="search"]');
    
    searchForms.forEach(form => {
        const searchInput = form.querySelector('input[name="q"]');
        
        if (searchInput) {
            // Add search suggestions (basic implementation)
            let searchTimeout;
            
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query.length < 2) return;
                
                searchTimeout = setTimeout(() => {
                    // Could implement search suggestions here
                    console.log('Search query:', query);
                }, 300);
            });
            
            // Enhance search form submission
            form.addEventListener('submit', function(e) {
                const query = searchInput.value.trim();
                if (!query) {
                    e.preventDefault();
                    showAlert('Please enter a search term', 'warning');
                    searchInput.focus();
                }
            });
        }
    });
}

/**
 * Form validation enhancements
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[method="POST"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            // Clear previous error states
            form.querySelectorAll('.is-invalid').forEach(field => {
                field.classList.remove('is-invalid');
            });
            
            // Validate required fields
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                }
                
                // Email validation
                if (field.type === 'email' && field.value.trim()) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(field.value)) {
                        field.classList.add('is-invalid');
                        isValid = false;
                    }
                }
                
                // URL validation
                if (field.type === 'url' && field.value.trim()) {
                    try {
                        new URL(field.value);
                    } catch {
                        field.classList.add('is-invalid');
                        isValid = false;
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields correctly', 'danger');
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            } else {
                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
                    submitBtn.disabled = true;
                    
                    // Re-enable if form submission fails
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }, 10000);
                }
            }
        });
        
        // Real-time validation feedback
        form.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('blur', function() {
                validateField(this);
            });
            
            field.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

/**
 * Validate individual field
 */
function validateField(field) {
    field.classList.remove('is-invalid', 'is-valid');
    
    if (field.hasAttribute('required') && !field.value.trim()) {
        field.classList.add('is-invalid');
        return false;
    }
    
    if (field.type === 'email' && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    if (field.type === 'url' && field.value.trim()) {
        try {
            new URL(field.value);
        } catch {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    if (field.value.trim()) {
        field.classList.add('is-valid');
    }
    
    return true;
}

/**
 * Lazy loading for images and content
 */
function initializeLazyLoading() {
    // Intersection Observer for lazy loading
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // Lazy load cards on scroll
    const cards = document.querySelectorAll('.card');
    let cardIndex = 0;
    
    function loadMoreCards() {
        const cardsToLoad = 6;
        const endIndex = Math.min(cardIndex + cardsToLoad, cards.length);
        
        for (let i = cardIndex; i < endIndex; i++) {
            cards[i].style.opacity = '0';
            cards[i].style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                cards[i].style.transition = 'all 0.5s ease';
                cards[i].style.opacity = '1';
                cards[i].style.transform = 'translateY(0)';
            }, (i - cardIndex) * 100);
        }
        
        cardIndex = endIndex;
    }
    
    // Initial load
    loadMoreCards();
    
    // Load more on scroll
    window.addEventListener('scroll', throttle(() => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            if (cardIndex < cards.length) {
                loadMoreCards();
            }
        }
    }, 250));
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Scroll to top button
 */
function initializeScrollToTop() {
    // Create scroll to top button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-4 rounded-circle';
    scrollBtn.style.cssText = `
        width: 50px;
        height: 50px;
        z-index: 1000;
        display: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    scrollBtn.setAttribute('aria-label', 'Scroll to top');
    document.body.appendChild(scrollBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', throttle(() => {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    }, 100));
    
    // Smooth scroll to top
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                
                const offsetTop = targetElement.offsetTop - 100; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Image modal for post content
 */
function initializeImageModal() {
    const postContent = document.querySelector('.post-content');
    if (!postContent) return;
    
    const images = postContent.querySelectorAll('img');
    
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            createImageModal(this.src, this.alt);
        });
    });
}

/**
 * Create image modal
 */
function createImageModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${alt || 'Image'}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img src="${src}" class="img-fluid" alt="${alt || ''}">
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', () => {
        modal.remove();
    });
}

/**
 * Copy to clipboard functionality
 */
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text).then(() => {
            showAlert('Link copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

/**
 * Fallback copy function for older browsers
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert('Link copied to clipboard!', 'success');
    } catch (err) {
        showAlert('Failed to copy link', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            const alert = new bootstrap.Alert(alertDiv);
            alert.close();
        }
    }, 5000);
}

/**
 * Throttle function for performance optimization
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

/**
 * Handle network errors gracefully
 */
window.addEventListener('online', () => {
    showAlert('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    showAlert('Connection lost. Some features may not work.', 'warning');
});

/**
 * Performance monitoring
 */
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.timing;
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
            
            if (loadTime > 3000) {
                console.warn('Page load time:', loadTime + 'ms');
            }
        }, 0);
    });
}

/**
 * Export functions for global access
 */
window.BlogApp = {
    copyToClipboard,
    showAlert,
    validateField
};
