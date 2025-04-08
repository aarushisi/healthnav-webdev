document.addEventListener("DOMContentLoaded", function() {
    // Language Selection Handling
    const languageDropdown = document.getElementById("language-dropdown");
    const welcomeTitle = document.getElementById("welcome-title");
    const startButton = document.getElementById("get-started-btn");

    // Translations for multi-language support
    const translations = {
        en: {
            title: "Welcome to the Healthcare Navigator",
            button: "Get Started"
        },
        es: {
            title: "Bienvenido al Navegador de Atención Médica",
            button: "Comenzar"
        },
        fr: {
            title: "Bienvenue sur le Navigateur de Santé",
            button: "Commencer"
        }
    };

    if (languageDropdown) {
        // Load stored language preference
        const savedLanguage = localStorage.getItem("selectedLanguage") || "en";
        languageDropdown.value = savedLanguage;
        applyTranslations(savedLanguage);

        // Update language selection when changed
        languageDropdown.addEventListener("change", function() {
            const selectedLanguage = languageDropdown.value;
            localStorage.setItem("selectedLanguage", selectedLanguage);
            applyTranslations(selectedLanguage);
        });
    }

    // Apply translations based on selected language
    function applyTranslations(lang) {
        if (translations[lang]) {
            welcomeTitle.textContent = translations[lang].title;
            startButton.textContent = translations[lang].button;
        }
    }

    // Redirect to form page when "Get Started" button is clicked
    const startButtonElement = document.getElementById("get-started-btn");
    if (startButtonElement) {
        startButtonElement.addEventListener("click", function() {
            window.location.href = "form.html";
        });
    }

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
                insurance: document.getElementById('insurance').value,
                street: document.getElementById('street').value.trim(),
                city: document.getElementById('city').value.trim(),
                state: document.getElementById('state').value,
                zip: document.getElementById('zip').value.trim()
            };

            fetch("http://127.0.0.1:5002/submit", {
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

            fetch("http://127.0.0.1:5002/submit-symptoms", {
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
        fetch("http://127.0.0.1:5002/get-user-data")
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
                document.getElementById("profile-address").textContent = `${data.street}, ${data.city}, ${data.state}, ${data.zip}`;
                document.getElementById("profile-symptoms").textContent = data.symptoms;
            })
            .catch(error => console.error("Error fetching data:", error));
    }

    const correctButton = document.getElementById("correct-btn");
    if (correctButton) {
        correctButton.addEventListener("click", function() {
            window.location.href = "doctors.html";
        });
    }

    // Fetch and display doctors when on the doctors page
    if (window.location.pathname.includes("doctors.html")) {
        fetch("http://127.0.0.1:5002/get-user-data")
            .then(response => response.json())
            .then(userData => {
                if (userData.error) {
                    console.error("Error fetching user data:", userData.error);
                    return;
                }

                const userState = userData.state;  // Extract user's state

                // Fetch doctors and filter by state
                fetch("http://127.0.0.1:5002/get-doctors")
                    .then(response => response.json())
                    .then(doctors => {
                        const filteredDoctors = doctors
                            .filter(doc => doc.state === userState) // Match state
                            .sort((a, b) => a.last_name.localeCompare(b.last_name)) // Sort alphabetically
                            .slice(0, 10); // Limit to top 10

                        displayDoctors(filteredDoctors);
                    })
                    .catch(error => console.error("Error fetching doctors:", error));
            })
            .catch(error => console.error("Error fetching user data:", error));
    }

    if (window.location.pathname.includes("doctors.html")) {
        fetch("http://127.0.0.1:5002/get-user-data")
            .then(response => response.json())
            .then(userData => {
                if (userData.error) {
                    console.error("Error fetching user data:", userData.error);
                    return;
                }

                const userState = userData.state;

                // Fetch doctors and filter by state
                fetch("http://127.0.0.1:5002/get-doctors")
                    .then(response => response.json())
                    .then(doctors => {
                        const filteredDoctors = doctors
                        .filter(doc => doc.state === userState)
                        .sort((a, b) => a.last_name.localeCompare(b.last_name))
                        .slice(0, 10); // Limit to first 10 doctors

                        displayDoctors(filteredDoctors);
                    })
                    .catch(error => console.error("Error fetching doctors:", error));
            })
            .catch(error => console.error("Error fetching user data:", error));
    }

    const arrowButton = document.getElementById("arrow-btn");
    if (arrowButton) {
        arrowButton.addEventListener("click", function () {
            const symptoms = document.getElementById("symptoms-box").value.trim();
            if (symptoms === "") {
                console.log("[ARROW] No symptoms entered.");
                return;
            }
    
            console.log("[ARROW] Sending symptoms to /followup-arrow:", symptoms);
    
            fetch("http://127.0.0.1:5002/followup-arrow", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ symptoms: symptoms })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("[ARROW] Error from server:", data.error);
                } else {
                    console.log("[ARROW] Response from model:", data.followup_response);
                    alert("Model Response: " + data.followup_response); // temporary display
                }
            })
            .catch(error => console.error("[ARROW] Request failed:", error));
        });
    }       
});

function displayDoctors(doctors) {
    const doctorsList = document.getElementById("doctors-list");
    const message = document.getElementById("doctors-message");

    // Clear previous entries (Fixes the issue)
    doctorsList.innerHTML = "";

    if (doctors.length === 0) {
        message.textContent = "No doctors found in your city.";
        return;
    }

    message.style.display = "none"; // Hide loading message

    // Ensure we only display 10 doctors
    const limitedDoctors = doctors.slice(0, 10);

    limitedDoctors.forEach(doctor => {
        const listItem = document.createElement("li");
        listItem.textContent = `${doctor.first_name} ${doctor.last_name}, ${doctor.degree} - ${doctor.city}, ${doctor.state}`;
        doctorsList.appendChild(listItem);
    });
}