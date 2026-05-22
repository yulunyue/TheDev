import time
from .base import Io
from typing import Dict, TYPE_CHECKING
from ..log import logger
from ..tool import uid

if TYPE_CHECKING:
    from ..node import Node
    from ...constant import C
    from .agent_client import AgentTcpClient


class Manage:
    def __init__(self):
        self.io_map: Dict[str, Io] = dict()
        self.topics: Dict[str, set] = dict()
        self.agent_clients: Dict[str, "AgentTcpClient"] = dict()

    def handler_msg(self, io: Io, msg: "Node"):
        from ...constant import C
        
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

    def register_agent(self, agent_id, info: dict, client: "AgentTcpClient"):
        client.agent_id = agent_id
        client.platform = info.get("platform")
        client.hostname = info.get("hostname")
        client.ip = info.get("ip")
        client.port = info.get("port")
        client.last_heartbeat = time.time()
        self.agent_clients[agent_id] = client
        logger.info(f"agent registered: {agent_id} {info.get('platform')}")

    def unregister_agent(self, agent_id):
        self.agent_clients.pop(agent_id, None)
        logger.info(f"agent unregistered: {agent_id}")

    def list_agents(self):
        result = []
        for agent_id, client in self.agent_clients.items():
            result.append({
                "agent_id": agent_id,
                "platform": getattr(client, "platform", None),
                "hostname": getattr(client, "hostname", None),
                "ip": getattr(client, "ip", None),
                "port": getattr(client, "port", None),
                "last_heartbeat": getattr(client, "last_heartbeat", None),
            })
        return result

    def handler_agent_msg(self, client: "AgentTcpClient", msg: "Node"):
        from ...constant import C
        
        t = msg.type
        if t == C.MSG_REGISTER:
            self.register_agent(
                msg.data.get("agent_id"),
                dict(
                    platform=msg.data.get("platform"),
                    hostname=msg.data.get("hostname"),
                    ip=client.src_ip,
                    port=client.src_port,
                ),
                client,
            )
            client.write_node(msg.__class__(type=C.MSG_REGISTER_OK))
        elif t == C.MSG_HEARTBEAT:
            client.last_heartbeat = time.time()
        elif t == C.MSG_UNREGISTER:
            self.unregister_agent(client.agent_id)
        elif t in (C.MSG_EXEC_STDOUT, C.MSG_EXEC_STDERR, C.MSG_EXEC_DONE):
            client.store_output(msg, self)

    def send_exec(self, agent_id, command, timeout=30):
        from ..node import Node
        from ...constant import C
        
        client = self.agent_clients.get(agent_id)
        if not client:
            raise ValueError(f"agent not found: {agent_id}")
        cmd_id = uid(16)
        client.write_node(
            Node(
                type=C.MSG_EXEC,
                key=cmd_id,
                data={"command": command, "timeout": timeout},
            )
        )
        return cmd_id

    def get_agent_output(self, cmd_id):
        for client in self.agent_clients.values():
            output = client.get_output(cmd_id)
            if output:
                return output
        return None

    def start_agent_server(self, host="0.0.0.0", port=20001):
        from .agent_server import AgentTcpServer

        AgentTcpServer(self).set_addr(src_ip=host, src_port=port).start()
        logger.info(f"agent server started on {host}:{port}")


IO_MANAGE = Manage()