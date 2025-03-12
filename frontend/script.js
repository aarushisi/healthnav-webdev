document.addEventListener("DOMContentLoaded", function() {
    // Form submission for personal details
    const form = document.getElementById('info-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            let name = document.getElementById('name').value.trim();
            let age = parseInt(document.getElementById('age').value, 10);

            if (name === "") name = "Anonymous";
            if (isNaN(age) || age < 0 || age > 120) {
                alert("Please enter a valid age between 0 and 120.");
                return;
            }

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
            .then(data => {
                console.log("Server response:", data);
                alert("User data successfully stored!");
                window.location.href = "symptoms.html"; // Redirect to symptoms page
            })
            .catch(error => {
                console.error("Error sending data:", error);
                alert("Failed to store user data.");
            });
        });
    }

    // Symptom submission
    const symptomsButton = document.getElementById('submit-symptoms-btn');
    if (symptomsButton) {
        symptomsButton.addEventListener("click", function() {
            const symptoms = document.getElementById("symptoms-box").value.trim();

            if (symptoms === "") {
                alert("Please enter your symptoms before submitting.");
                return;
            }

            const symptomData = {
                symptoms: symptoms
            };

            fetch("http://127.0.0.1:5000/submit-symptoms", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(symptomData)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Symptoms stored:", data);
                alert("Symptoms successfully submitted!");
            })
            .catch(error => {
                console.error("Error sending symptoms:", error);
                alert("Failed to submit symptoms.");
            });
        });
    }
});
