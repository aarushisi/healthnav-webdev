document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('info-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission and page refresh

        const name = document.getElementById('name').value;
        const age = document.getElementById('age').value;

        // Check if name or age is empty
        if (name.trim() === "") {
            alert("Please enter your name.");
            return; // Prevent form submission
        }

        if (age.trim() === "" || isNaN(age) || age <= 0) {
            alert("Please enter a valid age.");
            return; // Prevent form submission
        }

        const userData = {
            name: name,
            age: age,
            gender: document.getElementById('gender').value,
            insurance: document.getElementById('insurance').value
        };

        // Store user data in sessionStorage as a JSON string
        sessionStorage.setItem('userData', JSON.stringify(userData));

        console.log('User data stored:', userData);  // For testing, we log the user data to the console

        // Redirect to the symptoms page
        window.location.href = 'symptoms.html';
    });
});
