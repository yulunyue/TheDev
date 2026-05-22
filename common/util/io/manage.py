import time
from .base import Io
from typing import Dict
from ..node import Node
from ...constant import C
from ..log import logger


class Manage:
    def __init__(self):
        self.io_map: Dict[str, Io] = dict()
        self.topics: Dict[str, set] = dict()
        self.agents: Dict[str, dict] = dict()

    def handler_msg(self, io: Io, msg: Node):
        if not io.username:
            raise Exception(msg)
        if msg.type == C.METHOD_SUB:
            self.sub(msg.value, io.username)
        elif msg.type == C.METHOD_UN_SUB:
            self.un_sub(msg.value, io.username)
        elif msg.type == C.METHOD_LOGIN_OUT:
            if io.username in self.io_map:
                self.io_map.pop(io.username)
        elif msg.type == C.METHOD_LOGIN:
            self.io_map[io.username] = io
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
        return list(self.io_map.keys())

    def get_users_by_topic(self, topic_name):
        return self.topics.get(topic_name, set())

    def register_agent(self, agent_id, info: dict):
        self.agents[agent_id] = info
        logger.info(f"agent registered: {agent_id} {info.get('platform')}")

    def unregister_agent(self, agent_id):
        self.agents.pop(agent_id, None)
        logger.info(f"agent unregistered: {agent_id}")

    def heartbeat_agent(self, agent_id):
        if agent_id in self.agents:
            self.agents[agent_id]["last_heartbeat"] = time.time()

    def list_agents(self):
        return [{"agent_id": k, **v} for k, v in self.agents.items()]

    def start_agent_server(self, host="0.0.0.0", port=20001):
        from .agent_server import AgentTcpServer

        AgentTcpServer(self).set_addr(src_ip=host, src_port=port).start()
        logger.info(f"agent server started on {host}:{port}")


IO_MANAGE = Manage()
