from .base import Io
from typing import Dict
from ..node import Node
from ...constant import C
from ..log import logger


class Manage:
    def __init__(self):
        self.io_map: Dict[str, Io] = dict()
        self.topics: Dict[str, set] = dict()

    def hander_msg(self, io: Io, msg: Node):
        self.io_map[io.username] = io
        if msg.type == C.METHOD_SUB:
            self.sub(msg.value, io.username)
        elif msg.type == C.METHOD_UN_SUB:
            self.un_sub(msg.value, io.username)
        return self

    def sub(self, topic_name, user_name):
        if topic_name not in self.topics:
            self.topics[topic_name] = set()
        self.topics[topic_name].add(user_name)
        logger.map(
            topic_name=topic_name, user_name=user_name, topics=self.topics[topic_name]
        )

    def un_sub(self, topic_name, user_name):
        if topic_name in self.topics:
            self.topics[topic_name].discard(user_name)

    def send(self, topic_name, data):
        for k in self.topics.get(topic_name, []):
            send_data = dict(type=topic_name, value=data)
            self.io_map[k].send_data(send_data)

    def get_all_users(self):
        return list(self.io_map.keys())

    def get_users_by_topic(self, topic_name):
        return self.topics.get(topic_name, set())


IO_MANAGE = Manage()
