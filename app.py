import gradio as gr
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load model
print("Loading BLIP model...")
model_name = "Salesforce/blip-image-captioning-base"
device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)
print(f"Model loaded on {device}")

def generate_caption(image):
    """Generate caption for uploaded image"""
    if image is None:
        return "Please upload an image"
    
    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Process and generate caption
    inputs = processor(image, return_tensors="pt").to(device)
    
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=50,
            num_beams=5,
            early_stopping=True
        )
    
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption

# Create Gradio interface
demo = gr.Interface(
    fn=generate_caption,
    inputs=gr.Image(type="pil", label="Upload Image"),
    outputs=gr.Textbox(label="Generated Caption", lines=3),
    title="🖼️ RecogAIze - AI Image Captioning",
    description="Upload an image and get an AI-generated caption using the BLIP model from Salesforce Research.",
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
    ),
    allow_flagging="never",
    examples=[
        # You can add example images here
    ]
)

if __name__ == "__main__":
    demo.launch()
