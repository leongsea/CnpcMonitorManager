# -*- coding: utf-8 -*-
import time
from concurrent.futures import ThreadPoolExecutor
from hikvision_client import HikvisionClientAsync


class MultiCameraCaptureAsync:
    """异步多个摄像头图片捕获器"""
    def __init__(self):
        self.executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="Camera_Manager")
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "last_update": time.time()
        }

    def add_camera(self) -> bool:
        """添加摄像头信息到IP列表"""
        pass

    def _run_capture_async(self):
        """因为线程池只接受同步任务，所以这里采用

        同步函数"""
        async def capture_async():
            """同步函数里加异步函数用来执行真的任务"""
            client = HikvisionClientAsync()