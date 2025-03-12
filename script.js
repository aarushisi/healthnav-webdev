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

    // Symptoms Submission (Redirects to display page automatically)
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
                window.location.href = "display.html"; // Auto-redirect to display page
            })
            .catch(error => console.error("Error sending symptoms:", error));
        });
    }

    // Fetch and display user data on the display page
    if (window.location.pathname.includes("display.html")) {
        fetch("http://127.0.0.1:5000/get-user-data")
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Error fetching user data:", data.error);
                    return;
                }

                document.getElementById("profile-name").textContent = data.name;
                document.getElementById("profile-age").textContent = data.age;
                document.getElementById("profile-gender").textContent = data.gender;
                document.getElementById("profile-insurance").textContent = data.insurance;
                document.getElementById("profile-symptoms").textContent = data.symptoms;
            })
            .catch(error => console.error("Error fetching data:", error));
    }
});
