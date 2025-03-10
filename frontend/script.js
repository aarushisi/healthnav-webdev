document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('info-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission and page refresh

        const userData = {
            name: document.getElementById('name').value,
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            insurance: document.getElementById('insurance').value
        };

        // Store the user data in localStorage
        localStorage.setItem('userData', JSON.stringify(userData));

        console.log("User data stored in localStorage:", userData);  // For testing
    });
});
