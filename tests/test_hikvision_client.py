# -*- coding: utf-8 -*-


from src.camera.hikvision_client import HikvisionClientAsync
from src.database.camera_model import Camera
from src.utils.logger.logger_config import LoggerConfig
from src.utils.global_context.global_context import GlobalContext
import asyncio

async def test():
    camera1 = Camera(username = '5', ip = '192.168.2.114', password = '<PASSWORD>')
    camera2 = Camera(username = '6', ip = '192.168.2.124', password = '<PASSWORD>')
    client = HikvisionClientAsync(camera1)
    client2 = HikvisionClientAsync(camera2)
    clients = [client, client2]
    tasks = [c.test_connection_async() for c in clients]
    result = await asyncio.gather(*tasks)


if __name__ == '__main__':
    """日志单例创建"""
    GlobalContext.set_fixed_fields(app_name='cnpc_monitor', env_name='Development')
    patched_logger = LoggerConfig().setup_logger()


    """并发测试"""
    asyncio.run(test())

