#!/usr/bin/env python3
"""
Simple FastAPI server for LIP-SYNC-float-fast inference
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import os
import sys
import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from generate import InferenceAgent, InferenceOptions

app = FastAPI(title="LIP-SYNC Float API")

# Base paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
RESULTS_DIR = BASE_DIR / "results"
CHECKPOINTS_DIR = BASE_DIR / "checkpoints"

# Ensure directories exist
RESULTS_DIR.mkdir(exist_ok=True)


class LipSyncRequest(BaseModel):
    ref_image: str  # Path to reference image in assets folder
    audio_file: str  # Path to audio file in assets folder
    emotion: str = "neutral"  # angry, disgust, fear, happy, neutral, sad, surprise
    a_cfg_scale: float = 2.0
    r_cfg_scale: float = 1.0
    e_cfg_scale: float = 1.0
    nfe: int = 10
    no_crop: bool = False
    seed: int = 25
    output_file: str = None  # Optional custom output filename


# Initialize inference agent
def get_agent():
    """Initialize and return inference agent"""
    if not hasattr(app.state, 'agent'):
        import argparse
        # Create InferenceOptions instance and initialize parser
        inference_opts = InferenceOptions()
        parser = argparse.ArgumentParser()
        parser = inference_opts.initialize(parser)
        # Parse with empty args to get defaults
        opt = parser.parse_args([])
        
        opt.rank = 0
        opt.ngpus = 1
        opt.ckpt_path = str(CHECKPOINTS_DIR / "float.pth")
        opt.res_dir = str(RESULTS_DIR)
        
        # Check checkpoint exists
        if not Path(opt.ckpt_path).exists():
            raise RuntimeError(f"Checkpoint not found: {opt.ckpt_path}")
        
        app.state.agent = InferenceAgent(opt)
    
    return app.state.agent


@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    try:
        get_agent()
        print("✓ Inference agent initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")


@app.get("/")
def read_root():
    return {
        "message": "LIP-SYNC Float API",
        "description": "Generate lip-synced videos from reference images and audio",
        "endpoints": {
            "/generate": "POST - Generate lip-synced video",
            "/health": "GET - Check API health"
        }
    }


@app.get("/health")
def health_check():
    """Check if the API and model are ready"""
    try:
        agent = get_agent()
        return {
            "status": "healthy",
            "checkpoint": str(CHECKPOINTS_DIR / "float.pth"),
            "assets_dir": str(ASSETS_DIR),
            "results_dir": str(RESULTS_DIR)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/generate")
def generate_lipsync(request: LipSyncRequest):
    """
    Generate lip-synced video from reference image and audio
    
    Example:
    {
        "ref_image": "thl2.PNG",
        "audio_file": "thl_trimmed.wav",
        "emotion": "neutral",
        "a_cfg_scale": 2.0,
        "e_cfg_scale": 1.0,
        "seed": 15
    }
    """
    try:
        agent = get_agent()
        
        # Validate inputs
        ref_path = ASSETS_DIR / request.ref_image
        audio_path = ASSETS_DIR / request.audio_file
        
        if not ref_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Reference image not found: {request.ref_image}"
            )
        
        if not audio_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Audio file not found: {request.audio_file}"
            )
        
        # Validate emotion
        valid_emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        if request.emotion and request.emotion not in valid_emotions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid emotion. Must be one of: {valid_emotions}"
            )
        
        # Generate output filename
        if request.output_file:
            output_filename = request.output_file
        else:
            video_name = ref_path.stem
            audio_name = audio_path.stem
            call_time = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            output_filename = f"{call_time}-{video_name}-{audio_name}-nfe{request.nfe}-seed{request.seed}-acfg{request.a_cfg_scale}-ecfg{request.e_cfg_scale}-{request.emotion}.mp4"
        
        res_video_path = str(RESULTS_DIR / output_filename)
        
        # Run inference
        result_path = agent.run_inference(
            res_video_path=res_video_path,
            ref_path=str(ref_path),
            audio_path=str(audio_path),
            a_cfg_scale=request.a_cfg_scale,
            r_cfg_scale=request.r_cfg_scale,
            e_cfg_scale=request.e_cfg_scale,
            emo=request.emotion,
            nfe=request.nfe,
            no_crop=request.no_crop,
            seed=request.seed,
            verbose=True
        )
        
        return {
            "status": "success",
            "ref_image": request.ref_image,
            "audio_file": request.audio_file,
            "emotion": request.emotion,
            "output_path": result_path,
            "output_file": output_filename,
            "message": "Lip-sync video generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Upload a reference image to assets folder"""
    try:
        file_path = ASSETS_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "filename": file.filename,
            "path": str(file_path),
            "message": "Image uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """Upload an audio file to assets folder"""
    try:
        file_path = ASSETS_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "filename": file.filename,
            "path": str(file_path),
            "message": "Audio uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
