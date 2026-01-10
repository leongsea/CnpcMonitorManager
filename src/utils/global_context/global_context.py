# -*- coding: utf-8 -*-
from contextvars import ContextVar
from typing import Any, Dict, Optional


class GlobalContext:
    """全局上下文管理器
    
    固定字段:
        - app_name: 应用名称
        - env_name: 环境名称 (Development/Production/Test)
        - service_name: 服务名称
        - request_id: 请求ID（每个请求独立）
        - user_id: 用户ID
        - host_ip: 主机IP
        - elapsed_time: 耗时（可选）

        # 获取字段
        user_id = GlobalContext.get('user_id', default='anonymous')
        
        # 获取所有上下文
        context = GlobalContext.get_all()
    """

    _context: ContextVar[Optional[Dict[str, Any]]] = ContextVar("context", default=None)

    @classmethod
    def _get_context(cls) -> Dict[str, Any]:
        """获取当前上下文字典"""
        context = cls._context.get()
        if context is None:
            context = {}
            cls._context.set(context)
        return context

    @classmethod
    def set(cls, key: str, value: Any):
        """设置单个字段"""
        context = cls._get_context().copy()
        context[key] = value
        cls._context.set(context)

    @classmethod
    def get(cls, key: str, default=None) -> Optional[Any]:
        """获取单个字段"""
        return cls._get_context().get(key, default)

    @classmethod
    def set_fixed_fields(cls, app_name: str = "Unknown_app", env_name: str = "Development"):
        cls.set_multiple(app_name=app_name, env_name=env_name)

    @classmethod
    def set_multiple(cls, **kwargs):
        context = cls._get_context().copy()
        context.update(kwargs)
        cls._context.set(context)

    @classmethod
    def get_all(cls):
        return cls._get_context().copy()

    @classmethod
    def clear_request_fields(cls):
        cls.set_multiple(request_id="N/A", user_id="N/A", host_ip="0.0.0.0", elapsed_time="N/A")