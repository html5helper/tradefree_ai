from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        
        # 开发环境特定配置
        self.output_dir = "/home/qinbinbin/ai_tools/dify/docker/volumes/certbot/www/svg"
        self.model_path = "/home/qinbinbin/ai_tools/ComfyUI/models/florence2/large"
        
        # 调试模式
        self.debug = True