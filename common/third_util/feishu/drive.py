import json
import os

import httpx

from .auth import get_valid_user_token

API_BASE = "https://open.feishu.cn"


def upload_file(file_path, parent_node, parent_type="explorer", user_token=None):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    token = user_token or get_valid_user_token()

    resp = httpx.post(
        f"{API_BASE}/open-apis/drive/v1/files/upload_all",
        data={
            "file_name": file_name,
            "parent_type": parent_type,
            "parent_node": parent_node,
            "size": str(file_size),
        },
        files={"file": (file_name, open(file_path, "rb"))},
        headers={"Authorization": f"Bearer {token}"},
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"upload_file failed: code={data.get('code')} msg={data.get('msg')}")
    return data.get("data", {}).get("file_token")


def upload_media(file_path, parent_node, parent_type="sheet_image", extra=None, user_token=None):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    token = user_token or get_valid_user_token()

    fields = {
        "file_name": file_name,
        "parent_type": parent_type,
        "parent_node": parent_node,
        "size": str(file_size),
    }
    if extra:
        fields["extra"] = json.dumps(extra)

    resp = httpx.post(
        f"{API_BASE}/open-apis/drive/v1/medias/upload_all",
        data=fields,
        files={"file": (file_name, open(file_path, "rb"))},
        headers={"Authorization": f"Bearer {token}"},
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"upload_media failed: code={data.get('code')} msg={data.get('msg')}")
    return data.get("data", {}).get("file_token")


def download_file(file_token: str, user_token: str = None) -> bytes:
    token = user_token or get_valid_user_token()
    resp = httpx.get(
        f"{API_BASE}/open-apis/drive/v1/files/{file_token}/download",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code != 200:
        data = resp.json()
        raise RuntimeError(f"download_file failed: {resp.status_code} msg={data.get('msg')}")
    return resp.content


def make_attachment(file_token, file_name, mime_type="application/octet-stream", size=0):
    return [{
        "fileToken": file_token,
        "mimeType": mime_type,
        "size": size,
        "text": file_name,
        "type": "attachment",
    }]
