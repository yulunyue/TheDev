import time
from .base import Io
from typing import Dict, TYPE_CHECKING
from ..log import logger

if TYPE_CHECKING:
    from ..node import Node
    from ...constant import C


class Manage:
    def __init__(self):
        self.io_map: Dict[str, Io] = dict()
        self.topics: Dict[str, set] = dict()

    def handler_msg(self, io: Io, msg: "Node"):
        from ...constant import C

        t = msg.type
        io.last_heartbeat = time.time()
        if t == C.METHOD_LOGIN:
            io.username = msg.value
            if hasattr(io, "src_ip"):
                io.ip = io.src_ip
                io.port = io.src_port
            self.io_map[io.username] = io
        elif not io.username:
            raise Exception(msg)
        elif t == C.METHOD_LOGIN_OUT:
            self.io_map.pop(io.username, None)
        elif t == C.METHOD_SUB:
            self.sub(msg.value, io.username)
        elif t == C.METHOD_UN_SUB:
            self.un_sub(msg.value, io.username)
        else:
            io.hander_msg(msg)
        logger.info(f"msg={msg.to_json()} user={io.username}")
        return self

    def sub(self, topic_name, user_name):
        if topic_name not in self.topics:
            self.topics[topic_name] = set()
        self.topics[topic_name].add(user_name)

    def un_sub(self, topic_name, user_name):
        if topic_name in self.topics:
            self.topics[topic_name].discard(user_name)

    def send(self, topic_name, data):
        users = self.topics.get(topic_name, [])
        for k in list(users):
            send_data = dict(type=topic_name, value=data)
            if k in self.io_map:
                self.io_map[k].send_data(send_data)
            else:
                users.remove(k)

    def get_all_users(self):
        return self.io_map.keys()

    def get_users_by_topic(self, topic_name):
        return self.topics.get(topic_name, set())

    def start_agent_server(self, host="0.0.0.0", port=20001):
        from .agent_server import AgentTcpServer

        AgentTcpServer(self).set_addr(src_ip=host, src_port=port).start()
        logger.info(f"agent server started on {host}:{port}")


IO_MANAGE = Manage()
