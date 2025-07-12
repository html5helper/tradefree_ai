# ai/core/logging_patch.py

import logging.config
from uvicorn.config import LOGGING_CONFIG

def patch_uvicorn_logging(
    fmt: str = "%(asctime)s - %(levelname)s - %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S"
) -> None:
    """
    在程序最早期调用，用来给 Uvicorn 自带的 logging 配置添加时间戳格式。
    """
    # 覆写 default formatter
    LOGGING_CONFIG["formatters"]["default"]["fmt"]     = fmt
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = datefmt

    # 覆写 access formatter
    LOGGING_CONFIG["formatters"]["access"]["fmt"]     = (
        "%(asctime)s - %(levelname)s - %(client_addr)s "
        "- \"%(request_line)s\" %(status_code)s"
    )
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = datefmt

    # 重新加载
    logging.config.dictConfig(LOGGING_CONFIG)