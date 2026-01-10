# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from loguru import logger as _base_logger
from src.utils.common.file_tools import PathUtil
from src.utils.global_context.global_context import GlobalContext

# 全局变量: 存储 patched logger
_patched_logger = None

class LoggerConfig(object):
    """日志配置类"""
    """仅做一次配置，所以无需设置单例"""

    def __init__(self, log_dir:str = "storage/logs", app_name:str = "cnpc_monitor"):

        self.app_name = app_name
        self.log_dir = PathUtil(log_dir).set_save_dir().ensure_create()

    def setup_logger(self):
        """配置结构化日志"""
        global _patched_logger

        """移除默认logger"""
        _base_logger.remove()

        """自定义格式化函数"""
        def format_record(record):
            # 获取自定义的extra_fields
            extra = record["extra"]

            # 获取该条日志的等级
            level = record["level"].name

            # 以下是获取自定义字段的相关内容
            # name = extra.get("app_name")
            service = extra.get("service_name")
            request_id = extra.get("request_id", "N/A")
            user_id = extra.get("user_id", "N/A")
            host_ip = extra.get("host_ip")
            elapsed_time = extra.get("elapsed_time")

            """基础格式"""
            parts = [
                "<white>{time:YYYY-MM-DD HH:mm:ss}</white>",
                "<level>{level: <8}</level>",
            ]

            """Display the function field conditionally according to user level."""
            if level == "ERROR":
                parts.append("<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>")

            """动态绑定字段"""
            if service and service is not None:
                parts.append(f"<blue>{service}</blue>")

            if request_id and request_id !='N/A':
                parts.append(f"<magenta>request_ID:{request_id[:64]}</magenta>")

            if user_id and user_id != "N/A":
                parts.append(f"<cyan>user_ID:{user_id}</cyan>")

            if host_ip:
                parts.append(f"<yellow>{host_ip}</yellow>")

            if elapsed_time:
                parts.append(f"<red>Elapsed_time: {elapsed_time:.2f} s</red>")

            """消息"""
            message_part = "<level>{message}</level>"

            parts.append(message_part)

            return " | ".join(parts) + "\n"

        """控制台输出"""
        _base_logger.add(
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
        _base_logger.add(
            self.log_dir / f"{self.app_name}_error_{{time:YYYY-MM-DD}}.log",
            format=format_record,
            level="ERROR",
            rotation="100 MB",
            retention="90 days",
            backtrace=True,  # 显示完整堆栈
            diagnose=True  # 显示变量值
        )

        _patched_logger = _base_logger.patch(self.patch_record)
        _patched_logger.success("Logger Config successfully configured.")
        return _patched_logger

    """设置拦截器，在进入日志记录前更新上下文"""
    @staticmethod
    def patch_record(record):
        context = GlobalContext.get_all()
        context = {k:v for k,v in context.items()}
        record["extra"].update(context)

def get_logger():
    if _patched_logger is None:
        raise RuntimeError(f"Logger not configured.")
    return _patched_logger