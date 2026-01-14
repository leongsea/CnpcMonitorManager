from pydantic import BaseModel, Field, ConfigDict


class Camera(BaseModel):
    """
    摄像头配置对象

    Attributes:
        ip: 摄像头IP地址
        username: admin
        password: tx123456
    """
    # 配置
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    # 字段定义
    ip: str = Field(...,description='host_IP')
    username:str = Field(default='admin',description='username')
    password:str = Field(...,description='password')

    # 方法
    def to_dict(self) -> dict:
        """转换为字典"""
        return self.model_dump()

    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return self.model_dump_json()