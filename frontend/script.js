// Get references to the elements
const fileInput = document.getElementById("fileInput");
const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer"); // New element for container
const resultDiv = document.getElementById("result");

// Event listener for when a file is selected
fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0]; // Get the selected file

    if (file) {
        const reader = new FileReader(); // Create a FileReader object

        reader.onload = function(e) {
            imagePreview.src = e.target.result; // Set the image source to the read data URL
            previewContainer.classList.remove('hidden'); // Show the preview container
            resultDiv.innerHTML = "Ready to analyze."; // Reset result text
        };

        reader.readAsDataURL(file); // Read the image file as a data URL
    } else {
        imagePreview.src = "#"; // Clear the image source
        previewContainer.classList.add('hidden'); // Hide the preview container
        resultDiv.innerHTML = "Please select an image.";
    }
});


async function uploadImage() {
    // Moved fileInput and resultDiv declaration to top for global access within script.js
    // const fileInput = document.getElementById("fileInput"); // Already declared globally
    // const resultDiv = document.getElementById("result"); // Already declared globally

    if (!fileInput.files.length) {
        resultDiv.innerHTML = "Please select an image.";
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    // Update UI to show loading state
    resultDiv.innerHTML = "Analyzing...";

    try {
    // Make sure this fetch URL is correct!
    const response = await fetch("http://127.0.0.1:8000/detect", {
        method: "POST",
        body: formData,
    });

        if (!response.ok) {
             throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Update UI with the final results
// script.js (inside uploadImage function after const data = await response.json();)
// This structure correctly accesses the keys from your main.py response.

resultDiv.innerHTML = `
    <div class="result-line">Freshness: <b>${data.freshness}</b></div>
    <div class="result-line">Confidence: <b>${data.confidence}</b></div>
`;
    } catch (error) {
        console.error("Error during image analysis:", error);
        resultDiv.innerHTML = "Error: Could not connect to the server or process the image.";
    }
}