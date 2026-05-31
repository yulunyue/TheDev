import json
import os

import lark_oapi as lark


def _config():
    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "setting", "feishu.json")
    )
    with open(path) as f:
        return json.load(f)


class FeishuClient:
    _instance = None

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._client = (
            lark.Client.builder()
            .app_id(app_id)
            .app_secret(app_secret)
            .log_level(lark.LogLevel.ERROR)
            .build()
        )

    @property
    def client(self) -> lark.Client:
        return self._client

    @classmethod
    def get(cls):
        if cls._instance is None:
            cfg = _config()
            cls._instance = cls(cfg["app_id"], cfg["app_secret"])
        return cls._instance
