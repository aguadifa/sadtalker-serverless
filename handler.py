import os
import sys
import base64
import requests
import subprocess
import runpod

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception(f"Download failed: {url}")

def handler(event):
    try:
        job_input = event.get('input', {})
        audio_url = job_input.get('driven_audio')
        image_url = job_input.get('source_image')
        still = job_input.get('still', True)
        
        if not audio_url or not image_url:
            return {"error": "driven_audio and source_image URLs are required."}
            
        os.makedirs('/tmp/input', exist_ok=True)
        os.makedirs('/tmp/output', exist_ok=True)
        
        audio_path = "/tmp/input/audio.wav"
        image_path = "/tmp/input/image.png"
        output_dir = "/tmp/output"
        
        download_file(audio_url, audio_path)
        download_file(image_url, image_path)
        
        cmd = [
            "python", "inference.py",
            "--driven_audio", audio_path,
            "--source_image", image_path,
            "--result_dir", output_dir
        ]
        if still:
            cmd.append("--still")
            
        subprocess.run(cmd, check=True)
        
        generated_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
        if not generated_files:
            return {"error": "Video generation failed."}
            
        result_video_path = os.path.join(output_dir, generated_files[0])
        
        with open(result_video_path, "rb") as video_file:
            encoded_video = base64.b64encode(video_file.read()).decode('utf-8')
            
        return {
            "status": "success",
            "video_base64": encoded_video
        }

    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})
