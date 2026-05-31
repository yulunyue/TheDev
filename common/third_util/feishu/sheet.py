import base64

import httpx

from .api import _api_request, API_BASE
from .auth import get_valid_user_token


def read_range(spreadsheet_token: str, sheet_id: str, range_: str = None, user_token: str = None):
    full = f"{sheet_id}" if range_ is None else f"{sheet_id}!{range_}"
    data = _api_request(
        "GET",
        f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{full}",
        user_token=user_token,
    )
    return data.get("data", {}).get("valueRange", {}).get("values", [])


def write_range(spreadsheet_token: str, sheet_id: str, range_: str, values, user_token: str = None):
    full = f"{sheet_id}!{range_}"
    data = _api_request(
        "PUT",
        f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values",
        body={"valueRange": {"range": full, "values": values}},
        user_token=user_token,
    )
    return data.get("data", {}).get("revision", 0)


def spreadsheet_meta(spreadsheet_token: str, user_token: str = None):
    data = _api_request(
        "GET",
        f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/metainfo",
        user_token=user_token,
    )
    return data.get("data", {})


def insert_image(spreadsheet_token: str, sheet_id: str, cell: str, image_path: str, name: str = None, user_token: str = None):
    token = user_token or get_valid_user_token()
    range_ = f"{sheet_id}!{cell}:{cell}"

    with open(image_path, "rb") as f:
        fb = f.read()
    missing = 4 - len(fb) % 4
    if missing:
        fb += b"=" * missing
    b64 = base64.b64encode(fb).decode("utf-8")

    name = name or image_path.split("/")[-1]
    resp = httpx.post(
        f"{API_BASE}/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_image",
        json={"range": range_, "image": b64, "name": name},
        headers={"Authorization": f"Bearer {token}"},
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"insert_image failed: code={data.get('code')} msg={data.get('msg')}")
    return data.get("data", {}).get("revision", 0)
