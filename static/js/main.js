/* ============================================
   Insurance Management System - Main JavaScript
   Complete Interactive Features
   ============================================ */

'use strict';

/* ============================================
   1. DOM READY - INITIALIZATION
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Insurance Management System Loaded');

    // Initialize all components
    initAlerts();
    initTooltips();
    initPopovers();
    initFormValidation();
    initDataTables();
    initDatePickers();
    initSearchFilters();
    initStatCards();
    initCharts();
    initThemeToggle();

    console.log('✅ All components initialized');
});

/* ============================================
   2. ALERT MANAGEMENT
   ============================================ */

function initAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');

    alerts.forEach(alert => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            fadeOutAlert(alert);
        }, 5000);

        // Add close button functionality
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => fadeOutAlert(alert));
        }
    });
}

function fadeOutAlert(alert) {
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-20px)';
    setTimeout(() => {
        alert.remove();
    }, 300);
}

function showAlert(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const container = document.querySelector('.container, .container-fluid');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHTML);
        initAlerts();
    }
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/* ============================================
   3. BOOTSTRAP COMPONENTS
   ============================================ */

function initTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initPopovers() {
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/* ============================================
   4. FORM VALIDATION
   ============================================ */

function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                // Show error alert
                showAlert('Please fill in all required fields correctly.', 'danger');

                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }

            form.classList.add('was-validated');
        }, false);
    });
}

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        return form.checkValidity();
    }
    return true;
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

function validatePhone(phone) {
    const re = /^[0-9]{10}$/;
    return re.test(String(phone));
}

function validateRequired(value) {
    return value !== null && value !== undefined && value.trim() !== '';
}

/* ============================================
   5. CONFIRMATION DIALOGS
   ============================================ */

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(`⚠️ ${message}\n\nThis action cannot be undone.`);
}

function confirmAction(message, title = 'Confirm Action') {
    return confirm(`${title}\n\n${message}`);
}

function confirmSubmit(formName = 'this form') {
    return confirm(`Are you sure you want to submit ${formName}?`);
}

/* ============================================
   6. DATA TABLES ENHANCEMENT
   ============================================ */

function initDataTables() {
    // Add search highlight
    const searchInputs = document.querySelectorAll('input[type="text"][name="search"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function () {
            highlightSearchResults(this.value);
        });
    });

    // Add row click handlers
    const tableRows = document.querySelectorAll('table tbody tr[data-href]');
    tableRows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function () {
            window.location = this.dataset.href;
        });
    });

    // Add sorting capability
    addTableSorting();
}

function highlightSearchResults(searchTerm) {
    if (!searchTerm) return;

    const rows = document.querySelectorAll('table tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            row.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
        } else {
            row.style.backgroundColor = '';
        }
    });
}

function addTableSorting() {
    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(table => {
        const headers = table.querySelectorAll('thead th');
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => sortTable(table, index));
        });
    });
}

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();

        // Try numeric comparison first
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }

        // Fallback to string comparison
        return aText.localeCompare(bText);
    });

    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

/* ============================================
   7. DATE & TIME UTILITIES
   ============================================ */

function initDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set max date to today for past dates
        if (input.hasAttribute('data-max-today')) {
            input.max = getTodayDate();
        }

        // Set min date to today for future dates
        if (input.hasAttribute('data-min-today')) {
            input.min = getTodayDate();
        }
    });
}

function getTodayDate() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}

function formatDate(dateString, format = 'DD/MM/YYYY') {
    if (!dateString) return 'N/A';

    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    switch (format) {
        case 'DD/MM/YYYY':
            return `${day}/${month}/${year}`;
        case 'MM/DD/YYYY':
            return `${month}/${day}/${year}`;
        case 'YYYY-MM-DD':
            return `${year}-${month}-${day}`;
        default:
            return date.toLocaleDateString('en-IN');
    }
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';

    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function calculateDaysBetween(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    const diffTime = Math.abs(d2 - d1);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/* ============================================
   8. CURRENCY & NUMBER FORMATTING
   ============================================ */

function formatCurrency(amount) {
    if (isNaN(amount)) return '₹0.00';

    return '₹' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatNumber(number, decimals = 0) {
    if (isNaN(number)) return '0';

    return parseFloat(number).toLocaleString('en-IN', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function parseCurrency(currencyString) {
    return parseFloat(currencyString.replace(/[₹,]/g, '')) || 0;
}

/* ============================================
   9. SEARCH & FILTER
   ============================================ */

function initSearchFilters() {
    const searchForms = document.querySelectorAll('form[role="search"]');
    searchForms.forEach(form => {
        const input = form.querySelector('input[type="text"]');
        if (input) {
            // Add search icon
            input.style.paddingLeft = '2.5rem';

            // Add clear button
            addClearButton(input);

            // Add instant search (optional)
            if (input.hasAttribute('data-instant-search')) {
                input.addEventListener('input', debounce(() => {
                    form.submit();
                }, 500));
            }
        }
    });
}

function addClearButton(input) {
    if (input.value) {
        const clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'btn btn-sm btn-link position-absolute end-0 top-50 translate-middle-y';
        clearBtn.innerHTML = '<i class="fas fa-times"></i>';
        clearBtn.onclick = () => {
            input.value = '';
            input.focus();
            clearBtn.remove();
        };

        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(clearBtn);
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/* ============================================
   10. STATISTICS CARDS ANIMATION
   ============================================ */

function initStatCards() {
    const statCards = document.querySelectorAll('.stat-card, .card[data-stat]');

    // Animate numbers on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statCards.forEach(card => observer.observe(card));
}

function animateNumber(element) {
    const numberElement = element.querySelector('h3, h2, .stat-number');
    if (!numberElement) return;

    const finalNumber = parseInt(numberElement.textContent.replace(/[^0-9]/g, ''));
    if (isNaN(finalNumber)) return;

    const duration = 1000;
    const steps = 50;
    const increment = finalNumber / steps;
    let current = 0;

    const timer = setInterval(() => {
        current += increment;
        if (current >= finalNumber) {
            numberElement.textContent = formatNumber(finalNumber);
            clearInterval(timer);
        } else {
            numberElement.textContent = formatNumber(Math.floor(current));
        }
    }, duration / steps);
}

/* ============================================
   11. LOADING STATES
   ============================================ */

function showLoading(message = 'Loading...') {
    const loader = document.createElement('div');
    loader.id = 'global-loader';
    loader.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
    loader.style.backgroundColor = 'rgba(0,0,0,0.5)';
    loader.style.zIndex = '9999';
    loader.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div>${message}</div>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.remove();
    }
}

function showButtonLoading(button) {
    button.dataset.originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
}

function hideButtonLoading(button) {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || 'Submit';
}

/* ============================================
   12. CHARTS (Placeholder for Chart.js)
   ============================================ */

function initCharts() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') return;

    // Initialize any charts on the page
    const chartElements = document.querySelectorAll('canvas[data-chart]');
    chartElements.forEach(canvas => {
        const chartType = canvas.dataset.chartType || 'line';
        const chartData = JSON.parse(canvas.dataset.chartData || '{}');

        new Chart(canvas, {
            type: chartType,
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });
}

/* ============================================
   13. UTILITY FUNCTIONS
   ============================================ */

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

function printPage() {
    window.print();
}

function exportToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => col.textContent.trim());
        csv.push(rowData.join(','));
    });

    downloadFile(csv.join('\n'), filename, 'text/csv');
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/* ============================================
   14. LOCAL STORAGE HELPERS
   ============================================ */

function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

function getFromLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
        console.error('Error reading from localStorage:', e);
        return defaultValue;
    }
}

function removeFromLocalStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (e) {
        console.error('Error removing from localStorage:', e);
        return false;
    }
}

/* ============================================
   15. THEME TOGGLE
   ============================================ */

/**
 * Detect the user's OS-level colour-scheme preference.
 * @returns {'dark'|'light'}
 */
function getSystemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
}

/**
 * Apply a theme to <body> and persist it.
 * @param {'dark'|'light'} theme
 */
function setTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    saveToLocalStorage('theme', theme);

    // Update toggle button icon & aria-label
    const btn = document.getElementById('theme-toggle');
    if (btn) {
        btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
        btn.setAttribute('aria-label',
            theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
        btn.setAttribute('title',
            theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
    }
}

/**
 * Switch between light and dark themes.
 */
function toggleTheme() {
    const current = document.body.getAttribute('data-theme') || 'light';
    setTheme(current === 'light' ? 'dark' : 'light');
}

/**
 * Read saved preference (or fall back to OS preference) and apply it.
 * Wire up the toggle button click handler.
 */
function initThemeToggle() {
    // Determine starting theme: saved > OS preference > light
    const saved = getFromLocalStorage('theme', null);
    const theme = saved || getSystemTheme();
    setTheme(theme);

    // Attach click handler
    const btn = document.getElementById('theme-toggle');
    if (btn) {
        btn.addEventListener('click', toggleTheme);
    }

    // Optionally keep in sync with OS changes (no saved override)
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            // Only follow OS if the user has NOT manually chosen a theme
            if (!getFromLocalStorage('theme', null)) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}

/* ============================================
   16. AJAX HELPERS
   ============================================ */

async function fetchData(url, options = {}) {
    try {
        showLoading();
        const response = await fetch(url, options);
        hideLoading();

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        hideLoading();
        showAlert(`Error: ${error.message}`, 'danger');
        console.error('Fetch error:', error);
        return null;
    }
}

async function postData(url, data) {
    return fetchData(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
}

/* ============================================
   17. MOBILE DETECTION & RESPONSIVE
   ============================================ */

function isMobile() {
    return window.innerWidth <= 768;
}

function isTablet() {
    return window.innerWidth > 768 && window.innerWidth <= 1024;
}

function isDesktop() {
    return window.innerWidth > 1024;
}

// Handle window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Handle responsive changes
        console.log('Window resized');
    }, 250);
});

/* ============================================
   18. PERFORMANCE OPTIMIZATION
   ============================================ */

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

/* ============================================
   END OF MAIN.JS
   ============================================ */

console.log('📜 Main.js loaded successfully');
