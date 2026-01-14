# -*- coding: utf-8 -*-
from pathlib import Path

class PathUtil:
    """
    文件通用工具类
    :param file_dir: 直接传入目录符号后的路径即可, eg: storage/temp
    """
    def __init__(self, file_dir:str = None):
        self.file_dir = file_dir or 'storage/temp'
        self.save_dir = None
        self.parent_dir = self._find_project_root()

    @staticmethod
    def _find_project_root():
        current = Path(__file__).resolve()
        for path in current.parents:
            if (path / 'main.py').exists():
                return path
        return current.parents[0]

    def set_save_dir(self):
        self.save_dir = self.parent_dir / self.file_dir
        return self

    def ensure_create(self):
        self.save_dir.mkdir(parents=True, exist_ok=True)
        return self.save_dir
