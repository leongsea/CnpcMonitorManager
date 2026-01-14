# -*- coding: utf-8 -*-
import asyncio
from asyncio import Semaphore
from src.database.cmera_model import Camera
from typing import Dict, Any, List
from src.camera.hikvision_client import HikvisionClientAsync


class MultiCameraCaptureAsync:
    """异步多个摄像头图片捕获器"""

    def __init__(self, max_workers: int = 24):
        self.semaphore = Semaphore(max_workers)  # 信号量

    async def execute_task(self, camera: Camera) -> Dict[str, Any]:
        """
        执行单个任务
        Args:
            camera: camera instance
        Returns:
            结果字典 {status, data, error}
        """
        async with self.semaphore:
            try:
                hik_client = HikvisionClientAsync(camera)
                result = await hik_client.capture_image_async(camera)
                return {
                    'status': 'success',
                    'data': result,
                    'error': None
                }
            except Exception as e:
                return {
                    'status': 'failed',
                    'data': None,
                    'error': str(e)
                }

    async def execute_batch(self, camera_list: List[Camera]) -> Dict[str, Any]:
        """
            批量并发执行任务
            Args:
                camera_list: Camera列表，每个Camera包含自身的参数，如IP，username, Password

            Returns:
                统计结果 {total, success, failed, results}
        """
        # 构建任务列表
        task_list = [self.execute_task(camera) for camera in camera_list]

        #并发执行
        responses = await asyncio.gather(*task_list)

        # 统计
        total = len(responses)
        success_count= sum(1 for r in responses if r['status'] == 'success')
        failed = total - success_count

        return {
            'total': total,
            'success': success_count,
            'failed': failed,
            'results': responses
        }