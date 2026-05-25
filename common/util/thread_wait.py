import threading
from typing import Any, Optional

from ..exception import ThreadError, TimeoutError
from .tool import uid


class ThreadWait:
    """通用线程同步等待"""
    
    def __init__(self, request_id: Optional[str] = None):
        self.request_id = request_id or uid(16)
        self.event = threading.Event()
        self._result: Optional[Any] = None
        self._error: Optional[str] = None
    
    def set_result(self, result: Any) -> None:
        self._result = result
        self.event.set()
    
    def set_error(self, error: str) -> None:
        self._error = error
        self.event.set()
    
    def wait(self, timeout: float = 30) -> Any:
        if not self.event.wait(timeout):
            raise TimeoutError(
                f"wait timeout: {self.request_id}",
                context={"timeout": timeout, "request_id": self.request_id}
            )
        if self._error:
            raise ThreadError(self._error)
        return self._result
    
    def is_done(self) -> bool:
        return self.event.is_set()
    
    def reset(self) -> None:
        self.event.clear()
        self._result = None
        self._error = None
    
    def get_result(self) -> Optional[Any]:
        return self._result
    
    def get_error(self) -> Optional[str]:
        return self._error