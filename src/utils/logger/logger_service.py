# -*- coding: utf-8 -*-
from src.utils.logger.logger_config import get_logger
from typing import Any, Dict, Optional
from src.utils.global_context.global_context import GlobalContext


class LoggerService:
    """日志服务类 - 不用于依赖注入"""
    _instance = None

    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = get_logger()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # @staticmethod
    # def _get_context() -> Dict[str, Any]:
    #     """获取当前上下文信息"""
    #     context = {}
    #
    #     """收集所有上下文"""
    #     if app_name := GlobalContext.get('app_name'):
    #         context["app_name"] = app_name
    #
    #     if env_name := GlobalContext.get('env_name'):
    #         context["env_name"] = env_name
    #     return context

    def _log(self, level: str, message: str, exception: Optional[Exception] = None, **kwargs):
        if exception and level.lower() == "error":
            self.logger.opt(exception=True, depth=2).error(message)
        else:
            getattr(self.logger.opt(depth=2), level.lower())(message)

    def info(self, message: str, **kwargs):
        """结构化 INFO 日志"""
        self._log("info", message, **kwargs)

    def debug(self, message: str, **kwargs):
        """结构化 DEBUG 日志"""
        self._log("debug", message, **kwargs)

    def warning(self, message: str, **kwargs):
        """结构化 WARNING 日志"""
        self._log("warning", message, **kwargs)

    def error(self, message: str, exception: Exception = None, **kwargs):
        """结构化 ERROR 日志"""
        self._log("error", message, exception=exception, **kwargs)

    def success(self, message: str, **kwargs):
        self._log("success", message, **kwargs)
