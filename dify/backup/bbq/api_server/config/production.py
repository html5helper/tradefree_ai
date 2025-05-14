from .base import BaseConfig

class ProductionConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        # 生产环境特定配置
        self.output_dir = "/data/www/svg"
        self.model_path = "/Users/qinbinbin/Desktop/llm/models/florence2/large"

        # 生产模式
        self.debug = False
