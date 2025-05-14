import os
import torch

class BaseConfig:
    def __init__(self):
        # Device configuration
        self.device = self._get_device()
        self.torch_dtype = self._get_torch_dtype()
        self.model_path = self._get_model_path()
        self.output_dir = self._get_output_dir()
    
    def _get_device(self):
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda:0"
        return "cpu"
    
    def _get_torch_dtype(self):
        if self.device == "cuda:0":
            return torch.float16
        return torch.float32
    
    def _get_model_path(self):
        return os.getenv("MODEL_PATH", "/home/qinbinbin/ai_tools/ComfyUI/models/florence2/large")
    
    def _get_output_dir(self):
        return os.getenv("OUTPUT_DIR", "/home/qinbinbin/ai_tools/dify/docker/volumes/certbot/www/svg")