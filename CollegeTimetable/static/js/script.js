document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value) {
                    event.preventDefault();
                    alert(`Please fill out the ${field.name} field.`);
                }
            });
        });
    });
});