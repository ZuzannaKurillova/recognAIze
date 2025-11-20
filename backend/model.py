"""
Image Captioning Model Module
Uses Hugging Face transformers with BLIP (Bootstrapping Language-Image Pre-training) model
"""
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io
from typing import Optional


class ImageCaptioningModel:
    """Singleton class for image captioning model"""
    
    _instance: Optional['ImageCaptioningModel'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        print("Loading BLIP model... This may take a few minutes on first run.")
        
        # Use BLIP model for image captioning
        self.model_name = "Salesforce/blip-image-captioning-base"
        
        # Determine device (GPU if available, else CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load processor and model
        self.processor = BlipProcessor.from_pretrained(self.model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.model.eval()
        
        print("Model loaded successfully!")
        self._initialized = True
    
    def generate_caption(self, image_bytes: bytes, max_length: int = 50) -> str:
        """
        Generate caption for an image
        
        Args:
            image_bytes: Image data as bytes
            max_length: Maximum length of generated caption
            
        Returns:
            Generated caption as string
        """
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary (handles PNG with alpha channel, etc.)
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Process image
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            # Generate caption
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=5,  # Beam search for better quality
                    early_stopping=True
                )
            
            # Decode the generated caption
            caption = self.processor.decode(output[0], skip_special_tokens=True)
            
            return caption
            
        except Exception as e:
            raise Exception(f"Error generating caption: {str(e)}")


# Global instance
_model_instance: Optional[ImageCaptioningModel] = None


def get_model() -> ImageCaptioningModel:
    """Get or create the model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = ImageCaptioningModel()
    return _model_instance
