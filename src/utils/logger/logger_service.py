# -*- coding: utf-8 -*-
from loguru import logger
from typing import Any, Dict, Optional
from src.utils.global_context.global_context import GlobalContext


class LoggerService:
    """日志服务类 - 不用于依赖注入"""
    _instance = None

    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = logger

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def _get_context() -> Dict[str, Any]:
        """获取当前上下文信息"""
        context = {}

        """收集所有上下文"""
        if app_name := GlobalContext.app_name.get():
            context["app_name"] = app_name

        if env_name := GlobalContext.env.get():
            context["env_name"] = env_name

        if service_name := GlobalContext.service_name.get():
            context["service_name"] = service_name

        if req_id := GlobalContext.request_id.get():
            context['request_id'] = req_id

        if u_id := GlobalContext.user_id.get():
            context['user_id'] = u_id
        return context

    def _log(self, level: str, message: str, exception: Optional[Exception] = None, **kwargs):
        context = self._get_context()
        context.update(kwargs)
        bound_logger = self.logger.bind(**context).opt(depth=2)
        if exception and level.lower() == "error":
            bound_logger.opt(exception=True).error(message)
        else:
            getattr(bound_logger, level.lower())(message)

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
