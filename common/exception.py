"""
TheDev 异常类层次结构
所有异常继承自 TheDevException，提供统一的错误处理接口
"""


class TheDevException(Exception):
    """基础异常类"""

    def __init__(self, message: str = "", context=None):
        self.code = self.__class__.__name__
        self.message = message
        self.context = context

        if context:
            super().__init__(f"[{self.code}] {message} | context: {context}")
        else:
            super().__init__(f"[{self.code}] {message}")


class ValidationError(TheDevException):
    """数据验证错误"""
    pass


class NotFoundError(TheDevException):
    """资源未找到"""
    pass


class ModuleLoadError(TheDevException):
    """模块加载失败"""
    pass


class ConfigError(TheDevException):
    """配置错误"""
    pass


class ApiError(TheDevException):
    """API 调用错误"""
    pass


class TaskError(TheDevException):
    """任务执行错误"""
    pass


class GameError(TheDevException):
    """游戏逻辑错误"""
    pass


class FileError(TheDevException):
    """文件操作错误"""
    pass


class ThreadError(TheDevException):
    """线程/并发错误"""
    pass


class TimeoutError(TheDevException):
    """等待超时"""
    pass


class EsError(TheDevException):
    """Elasticsearch 操作错误"""
    pass