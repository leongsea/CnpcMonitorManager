# -*- coding: utf-8 -*-
from loguru import logger
from typing import Any, Dict
import contextvars

"""用于存储请求上下文"""
request_id_var = contextvars.ContextVar('request_id', default='N/A')
user_id_var = contextvars.ContextVar('user_id', default='anonymous')


class LoggerService:
    """日志服务类 - 用于依赖注入"""

    def __init__(self, service_name: str, **extra_fields):
        self.service_name = service_name
        self.extra_fields = extra_fields
        self.logger = logger.bind(service=service_name, **extra_fields)

    def _get_context(self) -> Dict[str, Any]:
        """获取当前上下文信息"""
        context = {
            "service": self.service_name,
            "request_id": request_id_var.get(),
            "user_id": user_id_var.get()
        }
        # 合并额外字段（如 camera_ip）
        context.update(self.extra_fields)  # 合并绑定的字段
        return context

    def bind(self, **kwargs):
        new_fields = {**self.extra_fields,**kwargs}
        return LoggerService(self.service_name, **new_fields)

    def info(self, message: str, **kwargs):
        """结构化 INFO 日志"""
        context = self._get_context()
        context.update(kwargs)
        self.logger.bind(**context).opt(depth=1).info(message)

    def debug(self, message: str, **kwargs):
        """结构化 DEBUG 日志"""
        context = self._get_context()
        context.update(kwargs)
        self.logger.bind(**context).opt(depth=1).debug(message)

    def warning(self, message: str, **kwargs):
        """结构化 WARNING 日志"""
        context = self._get_context()
        context.update(kwargs)
        self.logger.bind(**context).opt(depth=1).warning(message)

    def error(self, message: str, exception: Exception = None, **kwargs):
        """结构化 ERROR 日志"""
        context = self._get_context()
        context.update(kwargs)
        if exception:
            self.logger.bind(**context).opt(exception=True,depth=1).error(message)
        else:
            self.logger.bind(**context).opt(depth=1).error(message)

    """理论上讲这个项目暂时用不到"""
    def set_request_context(self, request_id: str, user_id: str = None):
        """设置请求上下文"""
        request_id_var.set(request_id)
        if user_id:
            user_id_var.set(user_id)