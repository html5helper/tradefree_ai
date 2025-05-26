# celeryconfig.py - 基础配置文件
import os

# 环境配置
ENV = os.getenv("ENV", "development")

# 根据环境导入对应的配置
if ENV == "production":
    from ai.config.celeryconfig_prod import *
else:
    from ai.config.celeryconfig_dev import *
