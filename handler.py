import runpod
import subprocess
import os
import requests
import base64

def download_file(url, save_path):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def handler(job):
    job_input = job['input']
    source_image = job_input.get('source_image')
    driven_audio = job_input.get('driven_audio')
    
    os.makedirs('/tmp/input', exist_ok=True)
    os.makedirs('/tmp/output', exist_ok=True)
    
    img_path = '/tmp/input/image.png'
    audio_path = '/tmp/input/audio.wav'
    
    # User-Agent 적용한 안전한 다운로드
    download_file(source_image, img_path)
    download_file(driven_audio, audio_path)
    
    cmd = [
        'python', 'inference.py',
        '--driven_audio', audio_path,
        '--source_image', img_path,
        '--result_dir', '/tmp/output',
        '--checkpoint_dir', './checkpoints',
        '--still'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Inference Error Log:", result.stderr)
        raise Exception(f"Inference failed: {result.stderr}")
        
    output_files = os.listdir('/tmp/output')
    mp4_files = [f for f in output_files if f.endswith('.mp4')]
    if not mp4_files:
        raise Exception("No output video generated")
        
    res_path = os.path.join('/tmp/output', mp4_files[0])
    with open(res_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
        
    return {"video_base64": encoded}

runpod.serverless.start({"handler": handler})
