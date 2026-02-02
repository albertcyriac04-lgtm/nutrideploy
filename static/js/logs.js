// JavaScript for logs page

document.addEventListener('DOMContentLoaded', function() {
    const logForm = document.getElementById('logForm');
    const logsList = document.getElementById('logsList');
    
    if (logForm) {
        logForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(logForm);
            const data = {
                food_item_id: formData.get('food_item_id'),
                meal_type: formData.get('meal_type'),
                date: formData.get('date'),
                quantity: parseFloat(formData.get('quantity'))
            };
            
            try {
                const response = await fetch('/api/add-log/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    // Reload page to show new log
                    window.location.reload();
                } else {
                    const error = await response.json();
                    alert('Error: ' + (error.error || 'Failed to add meal'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to add meal. Please try again.');
            }
        });
    }
    
    // Update calories display when food item or quantity changes
    const foodItem = document.getElementById('foodItem');
    const quantity = document.getElementById('quantity');
    
    if (foodItem && quantity) {
        function updateCalories() {
            const selectedOption = foodItem.options[foodItem.selectedIndex];
            if (selectedOption && selectedOption.dataset.calories) {
                const baseCalories = parseFloat(selectedOption.dataset.calories);
                const qty = parseFloat(quantity.value) || 1;
                // You could display this somewhere if needed
            }
        }
        
        foodItem.addEventListener('change', updateCalories);
        quantity.addEventListener('input', updateCalories);
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

