import runpod
import subprocess
import os
import urllib.request
from huggingface_hub import snapshot_download

def prepare_models():
    os.makedirs("checkpoints", exist_ok=True)
    os.makedirs("gfpgan/weights", exist_ok=True)
    
    # SadTalker 핵심 체크포인트 다운로드 (HuggingFace)
    print("Downloading SadTalker checkpoints from HuggingFace...")
    snapshot_download(
        repo_id="vinthony/SadTalker",
        local_dir="checkpoints",
        local_dir_use_symlinks=False
    )
    
    # GFPGAN / Facexlib 모델 다운로드
    gfpgan_urls = {
        "gfpgan/weights/alignment_WFLW_400_100_0.pth": "https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_400_100_0.pth",
        "gfpgan/weights/detection_Resnet50_Final.pth": "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth",
        "gfpgan/weights/GFPGANv1.4.pth": "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth",
        "gfpgan/weights/parsing_parsenet.pth": "https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth"
    }
    for path, url in gfpgan_urls.items():
        if not os.path.exists(path):
            print(f"Downloading {path}...")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                print(f"Failed to download {path}: {e}")

prepare_models()

def handler(job):
    job_input = job['input']
    source_image = job_input.get('source_image')
    driven_audio = job_input.get('driven_audio')
    
    os.makedirs('/tmp/input', exist_ok=True)
    os.makedirs('/tmp/output', exist_ok=True)
    
    img_path = '/tmp/input/image.png'
    audio_path = '/tmp/input/audio.wav'
    
    urllib.request.urlretrieve(source_image, img_path)
    urllib.request.urlretrieve(driven_audio, audio_path)
    
    cmd = [
        'python', 'inference.py',
        '--driven_audio', audio_path,
        '--source_image', img_path,
        '--result_dir', '/tmp/output',
        '--still'
    ]
    
    subprocess.run(cmd, check=True)
    
    output_files = os.listdir('/tmp/output')
    mp4_files = [f for f in output_files if f.endswith('.mp4')]
    if not mp4_files:
        raise Exception("No output video generated")
        
    res_path = os.path.join('/tmp/output', mp4_files[0])
    import base64
    with open(res_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
        
    return {"video_base64": encoded}

runpod.serverless.start({"handler": handler})
