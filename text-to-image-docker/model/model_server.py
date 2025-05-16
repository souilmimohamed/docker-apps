import os
import torch
import gc
import psutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diffusers import AutoPipelineForText2Image
import base64
from io import BytesIO
from PIL import Image

# Memory optimization
torch.set_num_threads(4)  # Limit CPU threads used for tensor computations

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_NAME = os.environ.get("MODEL_NAME", "stabilityai/sdxl-turbo")

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load the pipeline
print(f"Loading model: {MODEL_NAME}")
pipe = AutoPipelineForText2Image.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,  # Use float32 for CPU
)
pipe = pipe.to(device)
print("Model loaded successfully")

class GenerationRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_inference_steps: int = 4
    guidance_scale: float = 0.0
    width: int = 512
    height: int = 512

class GenerationResponse(BaseModel):
    image: str

@app.get("/health")
def health_check():
    # Include memory usage information
    memory = psutil.virtual_memory()
    return {
        "status": "ok",
        "device": device,
        "memory_usage_percent": memory.percent,
        "available_memory_mb": memory.available / (1024 * 1024)
    }

@app.post("/generate", response_model=GenerationResponse)
async def generate_image(request: GenerationRequest):
    try:
        # Ensure width and height are within reasonable CPU limits
        width = min(request.width, 512)  # Cap at 512 for CPU performance
        height = min(request.height, 512)  # Cap at 512 for CPU performance
        
        # Generate the image
        image = pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            num_inference_steps=min(request.num_inference_steps, 10),  # Cap steps for CPU
            guidance_scale=request.guidance_scale,
            width=width,
            height=height,
        ).images[0]
        
        # Clear CUDA cache or run garbage collection
        if device == "cuda":
            torch.cuda.empty_cache()
        else:
            gc.collect()  # Run garbage collection to free memory
        
        # Convert to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {"image": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)