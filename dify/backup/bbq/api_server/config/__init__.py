import os
from .development import DevelopmentConfig
from .production import ProductionConfig

def get_config():
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()

# Export configuration instance
config = get_config()

# Export required variables
device = config.device
torch_dtype = config.torch_dtype
model_path = config.model_path
output_dir = config.output_dir
default_audio_path = config.audio_path
