# -*- coding: utf-8 -*-
from src.camera.hikvision_client import HikvisionClientAsync
import asyncio

if __name__ == '__main__':
    client = HikvisionClientAsync('192.168.1.244', 'admin', 'admin')
    asyncio.run(client.test_connection_async())