import json
import os
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import httpx

from .client import _config

_TOKEN_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "tmp", "feishu_token.json")
)


def _save_token(data: dict):
    os.makedirs(os.path.dirname(_TOKEN_PATH), exist_ok=True)
    data["_saved_at"] = time.time()
    with open(_TOKEN_PATH, "w") as f:
        json.dump(data, f)


def _load_token() -> dict | None:
    if not os.path.exists(_TOKEN_PATH):
        return None
    with open(_TOKEN_PATH) as f:
        return json.load(f)


def _exchange_code(code: str, redirect_uri: str) -> dict:
    cfg = _config()
    resp = httpx.post(
        "https://open.feishu.cn/open-apis/authen/v1/access_token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "app_id": cfg["app_id"],
            "app_secret": cfg["app_secret"],
            "redirect_uri": redirect_uri,
        },
    )
    body = resp.json()
    if body.get("code") != 0:
        raise RuntimeError(f"token exchange failed: {body.get('msg')}")
    return body["data"]


def _refresh_token(refresh_token: str) -> dict:
    cfg = _config()
    resp = httpx.post(
        "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "app_id": cfg["app_id"],
            "app_secret": cfg["app_secret"],
        },
    )
    body = resp.json()
    if body.get("code") != 0:
        raise RuntimeError(f"token refresh failed: {body.get('msg')}")
    return body["data"]


def get_valid_user_token() -> str:
    token_data = _load_token()
    if token_data is None:
        raise RuntimeError("未登录，请先执行 `python -m tool.feishu auth`")

    elapsed = time.time() - token_data.get("_saved_at", 0)
    expires_in = token_data.get("expires_in", 7200)

    if elapsed < expires_in - 300:
        return token_data["access_token"]

    if token_data.get("refresh_token"):
        try:
            new_data = _refresh_token(token_data["refresh_token"])
            new_data["_saved_at"] = time.time()
            _save_token(new_data)
            return new_data["access_token"]
        except Exception:
            pass

    raise RuntimeError("token 已过期且无法刷新，请重新执行 `python -m tool.feishu auth`")


def login(port: int = 51497):
    redirect_uri = f"http://localhost:{port}/callback"
    cfg = _config()
    auth_url = (
        f"https://open.feishu.cn/open-apis/authen/v1/index"
        f"?app_id={cfg['app_id']}&redirect_uri={redirect_uri}&state=feishu_cli"
    )

    print(f"在浏览器中打开以下链接：\n   {auth_url}")
    webbrowser.open(auth_url)
    print(f"授权后会自动回调到本地端口 {port}")

    code = None

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal code
            params = parse_qs(urlparse(self.path).query)
            code = params.get("code", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
            self.server.server_close()

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.timeout = 120
    while code is None:
        server.handle_request()

    print("获取到授权码，正在换取 token...")
    token_data = _exchange_code(code, redirect_uri)
    _save_token(token_data)
    print(f"登录成功，有效期 {token_data.get('expires_in', 7200)} 秒")
    return token_data
