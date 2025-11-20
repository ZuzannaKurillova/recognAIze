"""
FastAPI Backend for Image Captioning Application
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

from model import get_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Image Captioning API",
    description="AI-powered image captioning using BLIP model",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular default
        "http://localhost:3000",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class CaptionResponse(BaseModel):
    caption: str
    success: bool
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


# Global model instance
model = None


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model
    try:
        logger.info("Starting up... Loading model...")
        model = get_model()
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None
    )


@app.post("/api/caption", response_model=CaptionResponse)
async def generate_caption(file: UploadFile = File(...)):
    """
    Generate caption for uploaded image
    
    Args:
        file: Uploaded image file (JPG, PNG, etc.)
        
    Returns:
        JSON response with generated caption
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPG, PNG, etc.)"
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 10MB"
            )
        
        # Generate caption
        logger.info(f"Generating caption for image: {file.filename}")
        caption = model.generate_caption(image_bytes)
        logger.info(f"Generated caption: {caption}")
        
        return CaptionResponse(
            caption=caption,
            success=True,
            message="Caption generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Image Captioning API",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
