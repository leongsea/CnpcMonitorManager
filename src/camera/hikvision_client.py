# -*- coding: utf-8 -*-

"""
海康摄像头连接取流并截图，保存文件路径至数据库
"""
import aiohttp
from typing import Optional
from src.database.camera_model import Camera
from src.utils.logger.logger_service import LoggerService
from src.utils.decorators.decorators import auto_request_context
from src.utils.global_context.global_context import GlobalContext

"""公共常量"""
TIMEOUT = 3
PORT = 554


class HikvisionClientAsync:
    """海康摄像头客户端"""

    def __init__(self, camera: Camera, **kwargs):
        """
        摄像头客户端初始函数
        Args:
            camera: 需要传入的摄像头对象Camera，包含ip,username,password等
            **kwargs: 其他关键字参数可能包括:
                user_id: 摄像头序号
        """
        self.ip = camera.ip
        self.username = camera.username
        self.password = camera.password
        self.user_id = kwargs.get("user_id")
        self.port = PORT
        self.timeout = TIMEOUT
        self.base_url = f"http://{self.ip}:{self.port}"
        self.headers = {
            'Content-Type': 'text/plain;charset=UTF-8',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        self.logger = LoggerService.get_instance()

    @auto_request_context
    async def capture_image_async(self) -> Optional[bytes]:
        """

        Returns:
            返回摄像头抓图响应
        """
        # --- 上下文设置 ---
        GlobalContext.set_multiple(service_name=self.__class__.__name__, usre_id=self.user_id, host_ip=self.ip)

        # --- 连接超时配置 ---
        timeout = aiohttp.ClientTimeout(
            total=self.timeout,
            connect=self.timeout,
            sock_read=self.timeout,
            sock_connect=self.timeout,
        )

        self.logger.info(f"Starting Connection ...")

        async with aiohttp.ClientSession(timeout=timeout) as session:
            """此处Url需要替换可能是RTSP协议也可能是ISAPI协议"""
            url = f"https://192.168.1.254/#/signin"
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    self.logger.warning(f"failed to capture,Status_code: {response.status}")
                    return None

    async def test_connection_async(self):
        """
        测试函数：测试capture_image_async是否连接成功

        Returns:
            连接响应成功：响应数据不为None则返回True

            连接响应报错: 其余情况均返回False
        """
        try:
            image_data = await self.capture_image_async()
            return image_data is not None
        except Exception as e:
            print(str(e))
            return False
