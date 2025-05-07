import torch

# 设置输出路径
OUTPUT_DIR = "/home/qinbinbin/ai_tools/dify/docker/volumes/certbot/www/svg"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_path = "/home/qinbinbin/ai_tools/ComfyUI/models/florence2/large"
