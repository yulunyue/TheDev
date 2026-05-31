import json

import httpx
import lark_oapi as lark

from .client import FeishuClient

API_BASE = "https://open.feishu.cn"


def _api_request(method: str, uri: str, *, queries=None, body=None, user_token=None):
    if user_token:
        headers = {"Authorization": f"Bearer {user_token}"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        resp = httpx.request(method, f"{API_BASE}{uri}", params=queries, json=body, headers=headers)
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"{uri} failed: code={data.get('code')} msg={data.get('msg')}")
        return data

    client = FeishuClient.get().client
    req = (
        lark.BaseRequest.builder()
        .http_method(getattr(lark.HttpMethod, method.upper()))
        .uri(uri)
        .token_types({lark.AccessTokenType.TENANT})
    )
    if queries:
        req = req.queries(queries)
    if body is not None:
        req = req.body(body)

    resp = client.request(req.build())
    if not resp.success():
        raise RuntimeError(f"{uri} failed: code={resp.code} msg={resp.msg}")
    return json.loads(resp.raw.content)
