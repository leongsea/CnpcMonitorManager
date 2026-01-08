# -*- coding: utf-8 -*-
from loguru import logger
import sys
import json
from pathlib import Path

class LoggerConfig(object):
    """日志配置类"""

    def __init__(self, log_dir:str = "../storage/logs", app_name:str = "my_app"):
        self.log_dir = Path(log_dir)
        self.app_name = app_name
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def setup_logger(self):
        """配置结构化日志"""

        """移除默认logger"""
        logger.remove()

        """自定义格式化函数"""
        def format_record(record):
            extra = record["extra"]
            service = extra.get("service", "Unknown")
            request_id = extra.get("request_id", "N/A")
            user_id = extra.get("user_id", "N/A")
            ip = extra.get("ip")

            """基础格式"""
            parts = [
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green>",
                "<level>{level: <8}</level>",
                f"<blue>{service}</blue>",
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            ]

            """动态绑定字段"""
            if ip:
                parts.append(f"<yellow>IP:{ip}</yellow>")

            if request_id != "N/A":
                parts.append(f"<magenta>req:{request_id[:8]}</magenta>")

            if user_id != "N/A" and user_id != "anonymous":
                parts.append(f"<cyan>user:{user_id}</cyan>")

            """消息"""
            message_part = "<level>{message}</level>"

            parts.append(message_part)

            return " | ".join(parts) + "\n"

        """控制台输出"""
        logger.add(
            sys.stdout,
            level="INFO",
            colorize=True,
            format=format_record,
        )

        # """文件输出 - Json格式"""
        # logger.add(
        #     self.log_dir / f"{self.app_name}_{{time:YYYY-MM-DD}}.json",
        #     format="{message}",
        #     level="DEBUG",
        #     rotation="00:00",  # 每天轮转
        #     retention="30 days",  # 保留30天
        #     compression="zip",  # 压缩旧日志
        #     serialize=True,  # 自动序列化为 JSON
        #     enqueue=True  # 异步写入
        # )

        """错误日志单独文件"""
        logger.add(
            self.log_dir / f"{self.app_name}_error_{{time:YYYY-MM-DD}}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation="100 MB",
            retention="90 days",
            backtrace=True,  # 显示完整堆栈
            diagnose=True  # 显示变量值
        )
        return logger