import axios from 'axios';

document.addEventListener('DOMContentLoaded', function() {
    const statusElement = document.getElementById('status');
    const generateBtn = document.getElementById('generate-btn');
    const promptInput = document.getElementById('prompt');
    const negativePromptInput = document.getElementById('negative-prompt');
    const stepsInput = document.getElementById('steps');
    const guidanceInput = document.getElementById('guidance');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const loadingElement = document.getElementById('loading');
    const generatedImage = document.getElementById('generated-image');
    
    // Model service URL
    const MODEL_SERVICE_URL = 'http://localhost:8080';
    
    // Check if the model service is running
    checkModelService();
    
    // Check model service health every 10 seconds
    setInterval(checkModelService, 10000);
    
    function checkModelService() {
        axios.get(`${MODEL_SERVICE_URL}/health`)
            .then(() => {
                statusElement.textContent = 'Connected to model service';
                statusElement.className = 'status connected';
                generateBtn.disabled = false;
            })
            .catch(() => {
                statusElement.textContent = 'Cannot connect to model service. Make sure it is running.';
                statusElement.className = 'status disconnected';
                generateBtn.disabled = true;
            });
    }
    
    generateBtn.addEventListener('click', function() {
        // Validate input
        if (!promptInput.value.trim()) {
            alert('Please enter a prompt');
            return;
        }
        
        // Disable button and show loading
        generateBtn.disabled = true;
        loadingElement.style.display = 'block';
        loadingElement.textContent = 'Generating image... This may take 30-60 seconds on CPU.';
        generatedImage.style.display = 'none';
        
        // Prepare request data
        const requestData = {
            prompt: promptInput.value,
            negative_prompt: negativePromptInput.value,
            num_inference_steps: parseInt(stepsInput.value),
            guidance_scale: parseFloat(guidanceInput.value),
            width: parseInt(widthInput.value),
            height: parseInt(heightInput.value)
        };
        
        // Send request to model service
        axios.post(`${MODEL_SERVICE_URL}/generate`, requestData)
            .then(response => {
                // Display the generated image
                generatedImage.src = `data:image/png;base64,${response.data.image}`;
                generatedImage.style.display = 'block';
            })
            .catch(error => {
                alert(`Error generating image: ${error.response?.data?.detail || error.message}`);
                console.error('Error:', error);
            })
            .finally(() => {
                // Re-enable button and hide loading
                generateBtn.disabled = false;
                loadingElement.style.display = 'none';
            });
    });
});