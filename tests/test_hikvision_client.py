# -*- coding: utf-8 -*-
from src.camera.hikvision_client import HikvisionClientAsync
from src.utils.logger.logger_config import LoggerConfig
import asyncio

async def test():
    client = HikvisionClientAsync('192.168.1.244', 'admin', 'admin')
    client2 = HikvisionClientAsync('192.168.1.214', 'admin', 'admin')
    clients = [client, client2]
    tasks = [c.test_connection_async() for c in clients]
    result = await asyncio.gather(*tasks)
    print(result)


if __name__ == '__main__':
    """日志单例创建"""
    LoggerConfig().setup_logger()
    """并发测试"""
    asyncio.run(test())

