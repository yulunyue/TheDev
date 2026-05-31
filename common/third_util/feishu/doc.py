from .api import _api_request


def read_raw_content(document_id: str, user_token: str = None) -> str:
    data = _api_request(
        "GET",
        f"/open-apis/docx/v1/documents/{document_id}/raw_content",
        user_token=user_token,
    )
    return data.get("data", {}).get("content", "")
