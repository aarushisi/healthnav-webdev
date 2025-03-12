document.addEventListener("DOMContentLoaded", function() {
    // Personal Info Form Submission (Redirects to symptoms page)
    const form = document.getElementById('info-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            let name = document.getElementById('name').value.trim();
            let age = parseInt(document.getElementById('age').value, 10);

            if (name === "") name = "Anonymous";
            if (isNaN(age) || age < 0 || age > 120) return;

            const userData = {
                name: name,
                age: age,
                gender: document.getElementById('gender').value,
                insurance: document.getElementById('insurance').value
            };

            fetch("http://127.0.0.1:5000/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData)
            })
            .then(response => response.json())
            .then(() => {
                window.location.href = "symptoms.html"; // Auto-redirect to symptoms page
            })
            .catch(error => console.error("Error sending data:", error));
        });
    }

    // Symptoms Submission (Redirects to next page automatically)
    const symptomsButton = document.getElementById('submit-symptoms-btn');
    if (symptomsButton) {
        symptomsButton.addEventListener("click", function() {
            const symptoms = document.getElementById("symptoms-box").value.trim();
            if (symptoms === "") return; // Prevent empty submissions

            const symptomData = { symptoms: symptoms };

            fetch("http://127.0.0.1:5000/submit-symptoms", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(symptomData)
            })
            .then(response => response.json())
            .then(() => {
                window.location.href = "display.html"; // Auto-redirect to the next step
            })
            .catch(error => console.error("Error sending symptoms:", error));
        });
    }
});
