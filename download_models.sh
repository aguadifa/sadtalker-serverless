#!/bin/bash
mkdir -p checkpoints
mkdir -p gfpgan/weights

python -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='vinthony/SadTalker', local_dir='checkpoints', local_dir_use_symlinks=False)
"

wget -O gfpgan/weights/alignment_WFLW_400_100_0.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_400_100_0.pth
wget -O gfpgan/weights/detection_Resnet50_Final.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
wget -O gfpgan/weights/GFPGANv1.4.pth https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
wget -O gfpgan/weights/parsing_parsenet.pth https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth
