// Main JavaScript for NutriDiet

document.addEventListener('DOMContentLoaded', function () {
    // Initialize any global functionality
    console.log('NutriDiet app loaded');

    // Mobile menu toggle (if needed)
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const sidebar = document.querySelector('aside');

    if (mobileMenuButton && sidebar) {
        mobileMenuButton.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }

    // Add any global event listeners here
});

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatNumber(num) {
    return Math.round(num).toLocaleString();
}

