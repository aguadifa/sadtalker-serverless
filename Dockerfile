FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /workspace/SadTalker

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 wget git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir runpod requests tqdm imageio imageio-ffmpeg opencv-python resampy yacs scipy librosa pillow kornia face_alignment gfpgan

COPY . .

# SadTalker 모델 저장 폴더 생성 및 다운로드
RUN mkdir -p checkpoints gfpgan/weights && \
    wget -O checkpoints/mapping_00109-model.pth.tar https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar && \
    wget -O checkpoints/mapping_00229-model.pth.tar https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar && \
    wget -O checkpoints/SadTalker_V0.0.2_256.safetensors https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors && \
    wget -O checkpoints/SadTalker_V0.0.2_512.safetensors https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors && \
    wget -O gfpgan/weights/alignment_WFLW_400_100_0.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_400_100_0.pth && \
    wget -O gfpgan/weights/detection_Resnet50_Final.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth && \
    wget -O gfpgan/weights/GFPGANv1.4.pth https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth && \
    wget -O gfpgan/weights/parsing_parsenet.pth https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth

CMD ["python", "-u", "handler.py"]
