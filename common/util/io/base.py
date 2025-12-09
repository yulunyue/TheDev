from common.util.export import Thread, socket, logger, Dict, time


class Io:
    sock: socket.socket
    childs: Dict[str, "Io"]

    def set_addr(self, src_ip, src_port, dst_ip=None, dst_port=None):
        self.src_ip: str = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
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

    def receive_msg(self, client: "Io", msg):
        logger.debug(f"{self} receive from {client}")

    def start(self):
        Thread(target=self.run, daemon=True).start()

    @property
    def logger(self):
        return logger

    def __repr__(self):
        return f"{self.__class__.__name__} src={self.src_ip}:{self.src_port} dst={self.dst_ip}:{self.dst_port}"
