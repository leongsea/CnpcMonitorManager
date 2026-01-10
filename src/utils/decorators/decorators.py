# -*- coding: utf-8 -*-
import functools
import time, random, string
from typing import Callable, Any
from src.utils.logger.logger_config import get_logger
from src.utils.global_context.global_context import GlobalContext


def auto_request_context(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        logger = get_logger()
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳
        # random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        # request_id = f"Req-{timestamp}-{random_str}"
        # GlobalContext.set_multiple(request_id = request_id)
        start_time = time.time()
        result = None
        try:
            # 5. 执行业务函数
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            # 6. 计算耗时（毫秒）
            elapsed_time = time.time() - start_time

            # 7. 设置 elapsed_time 到 GlobalContext
            GlobalContext.set('elapsed_time', elapsed_time)

            # 8. 根据抓图结果进行打印
            if result is not None:
                logger.success(f"Request completed: Capture Successful!")
            else:
                logger.warning(f"Request completed: {e.__class__.__qualname__}")
        finally:
            # 9. 清理请求字段
            GlobalContext.clear_request_fields()

    return wrapper
