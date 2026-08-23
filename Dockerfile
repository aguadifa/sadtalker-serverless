FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /workspace/SadTalker

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 git wget && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir runpod requests tqdm imageio imageio-ffmpeg opencv-python resampy yacs scipy librosa pillow kornia face_alignment gfpgan huggingface_hub

COPY . .

# 도커 빌드 타임에 모델 내장
RUN bash download_models.sh

CMD ["python", "-u", "handler.py"]
