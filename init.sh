conda create -n RL python=3.12 -y
source activate RL

cd open-r1-multimodal
pip install .
cd ..

pip uninstall open_r1 -y

pip install vllm==0.7.2
pip install math_verify
pip install pillow
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121 https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.0.post2/flash_attn-2.7.0.post2+cu12torch2.5cxx11abiFALSE-cp312-cp312-linux_x86_64.whl -U
pip install wandb
pip install qwen_vl_utils
pip install matplotlib seaborn pillow-avif-plugin

pip uninstall transformers -y
pip install git+https://github.com/huggingface/transformers.git@1931a351408dbd1d0e2c4d6d7ee0eb5e8807d7bf