# RecognAIze - AI Image Captioning Application

An AI-powered web application that automatically generates descriptive captions for images using deep learning. Built with Angular frontend, FastAPI backend, and PyTorch-based BLIP (Bootstrapping Language-Image Pre-training) model.

<img width="834" height="1077" alt="Screenshot 2025-11-20 at 16 57 21" src="https://github.com/user-attachments/assets/41e7467b-8851-429a-9807-cf264ef1e13b" />


## Features

- 🖼️ **Drag-and-drop image upload** with preview
- 🤖 **AI-powered caption generation** using state-of-the-art BLIP model
- 📝 **Caption history** tracking (last 5 captions)
- ⚡ **Real-time processing** with loading states
- 🎨 **Modern, responsive UI** with gradient backgrounds and animations
- 🔒 **File validation** (type and size checks)

## Technology Stack

### Frontend
- **Angular 19** - Modern web framework
- **TypeScript** - Type-safe JavaScript
- **CSS3** - Custom styling with gradients and animations
- **RxJS** - Reactive programming

### Backend
- **FastAPI** - High-performance Python web framework
- **PyTorch** - Deep learning framework
- **Transformers (Hugging Face)** - Pre-trained BLIP model
- **Pillow** - Image processing

### AI Model
- **BLIP** (Salesforce/blip-image-captioning-base) - State-of-the-art image captioning model

## Installation

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **npm** or **yarn**

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### Start the Frontend Server

```bash
cd frontend
ng serve
```

The frontend application will be available at `http://localhost:4200`

## Usage

1. Open your browser and navigate to `http://localhost:4200`
2. Drag and drop an image or click to browse
3. Wait for the AI to generate a caption
4. View the generated caption and caption history

## API Endpoints

### `POST /api/caption`
Upload an image and receive a generated caption.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "caption": "a dog sitting on a beach",
  "success": true,
  "message": "Caption generated successfully"
}
```

### `GET /api/health`
Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Project Structure

```
recogAIze/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── model.py             # BLIP model loader and inference
│   ├── requirements.txt     # Python dependencies
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── image-upload/      # Image upload component
│   │   │   │   └── caption-display/   # Caption display component
│   │   │   ├── services/
│   │   │   │   └── api.service.ts     # API communication service
│   │   │   ├── app.component.*        # Main app component
│   │   │   └── app.config.ts
│   │   └── styles.css                 # Global styles
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Configuration

### Backend Configuration
- **Port**: 8000 (default)
- **CORS**: Configured for `http://localhost:4200`
- **Max file size**: 10MB
- **Supported formats**: JPG, PNG, GIF, and other image formats

### Frontend Configuration
- **Port**: 4200 (default)
- **API URL**: `http://localhost:8000/api`

## Model Information

The application uses the **BLIP** (Bootstrapping Language-Image Pre-training) model from Salesforce Research. This model is specifically designed for image-to-text tasks and provides high-quality, descriptive captions.

- **Model**: `Salesforce/blip-image-captioning-base`
- **Architecture**: Vision Transformer + Language Model

On first run, the model will be automatically downloaded (~1GB). Subsequent runs will use the cached model.

## Performance

- **Caption generation**: ~2-5 seconds (depending on hardware)
- **GPU support**: Automatically uses CUDA if available
- **CPU fallback**: Works on CPU (slower but functional)

## Troubleshooting

## Acknowledgments

- **BLIP Model**: Salesforce Research
- **Hugging Face**: Transformers library
- **Angular Team**: Angular framework
- **FastAPI**: Modern Python web framework
