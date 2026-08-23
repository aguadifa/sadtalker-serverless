FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04
WORKDIR /workspace/SadTalker
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir runpod requests tqdm imageio imageio-ffmpeg opencv-python resampy yacs scipy librosa pillow kornia
COPY . .
CMD ["python", "-u", "handler.py"]
