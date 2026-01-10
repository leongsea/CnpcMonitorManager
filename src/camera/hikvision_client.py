# -*- coding: utf-8 -*-

"""
海康摄像头连接取流并截图，保存文件路径至数据库
"""
import aiohttp
from typing import Optional
from src.utils.decorators.decorators import auto_request_context
from src.utils.logger.logger_service import LoggerService
from src.utils.global_context.global_context import GlobalContext

"""公共常量"""
TIMEOUT = 3
PORT = 554


class HikvisionClientAsync:
    """海康摄像头客户端"""

    def __init__(self, **kwargs):
        """
        初始化摄像头客户端
        :param ip: 191.51.100.25
        :param username: admin
        :param password: hik12345+/tx123456/Tx136248
        :param port: 554
        :param timeout: 请求超时时间, 10秒默认
        """
        self.ip = kwargs.get('host_ip')
        self.password = kwargs.get('password')
        self.user_id = kwargs.get('user_id')
        self.username = 'admin'
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
    async def capture_image_async(self, **kwargs) -> Optional[bytes]:
        """
        捕获单个摄像头图片
        :param channel: 通道号默认为1
        :return: bytes: 二进制数据，失败返回None
        """

        """上下文设置"""
        # 固定的几个字段需要去设置，每个client是不一样的
        GlobalContext.set_multiple(service_name=self.__class__.__name__, usre_id='5', host_ip=self.ip)

        """Create an object for timeout"""
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
        """异步测试连接"""
        try:
            image_data = await self.capture_image_async()
            return image_data is not None
        except Exception as e:
            print(str(e))
            return False
