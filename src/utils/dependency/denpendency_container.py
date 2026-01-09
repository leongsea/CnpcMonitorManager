from dataclasses import dataclass
from ..logger.logger_service import LoggerService
from ..logger.logger_config import LoggerConfig


@dataclass
class DependencyContainer:
    """依赖注入容器"""

    def __init__(self):
        # 初始化日志配置
        config = LoggerConfig(app_name="cnpc_monitor")
        config.setup_logger()

        # 缓存服务实例
        self._services = {}

    def get_logger(self, service_name: str, **bind_fields) -> LoggerService:
        """获取日志服务实例（单例模式）"""
        if bind_fields:
            return LoggerService(service_name=service_name, **bind_fields)

        if service_name not in self._services:
            self._services[service_name] = LoggerService(service_name)
        return self._services[service_name]


# 全局容器实例
# container = DependencyContainer()