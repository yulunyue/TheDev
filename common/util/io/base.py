from threading import Thread

import socket
from ..log import logger, Logger, get_log
from typing import Dict, List
import time
from ..tool import json_dumps


class Io:
    sock: socket.socket
    childs: Dict[str, "Io"]
    _logger: Logger = None
    username = None

    def set_addr(self, src_ip=None, src_port=None, dst_ip=None, dst_port=None):
        self.src_ip: str = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        return self

    def set_logger(self, t):
        self._logger = t
        return self

    def set_sock(self, sock):
        self.sock = sock
        return self

    def create_socket(self):
        pass

    def init_socket(self):
        pass

    def init_data(self):
        pass

    def loop(self):
        pass

    def run(self):
        pass

    def write(self, data):
        if isinstance(data, dict):
            data = json_dumps(data)
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send(data)

    def send(self, data):
        raise NotImplemented

    def send_data(self, data):
        self.write(data)

    def start(self):
        Thread(target=self.run, daemon=True).start()

    @property
    def logger(self):
        if self._logger is None:
            self._logger = get_log(
                f"data/io/{self.__class__.__name__}/{self.src_ip}_{self.src_port}.log"
            )
        return self._logger

    def __repr__(self):
        return f"{self.__class__.__name__} src={self.src_ip}:{self.src_port} dst={self.dst_ip}:{self.dst_port}"
