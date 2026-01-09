# -*- coding: utf-8 -*-
from contextvars import ContextVar
from typing import Any, Dict, Optional


class GlobalContext:
    """应用级别上下文"""
    app_name: ContextVar[str] = ContextVar('app_name', default='N/A')
    env: ContextVar[str] = ContextVar('env', default='development')

    """服务级别上下文"""
    service_name: ContextVar[str] = ContextVar('service_name', default='Unknown_Service')

    """
    每个请求独立ID标识，且每个请求独立
    """
    request_id: ContextVar[Optional[str]] = ContextVar('request_id', default='_404')
    user_id: ContextVar[Optional[str]] = ContextVar('user_id', default='anonymous')

    """业务级别标识"""
    device_ip: ContextVar[Optional[str]] = ContextVar('device_ip', default='Unknown IP')