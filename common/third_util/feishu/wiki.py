from .api import _api_request


def resolve_node(wiki_token: str, user_token: str = None):
    body = _api_request(
        "GET", "/open-apis/wiki/v2/spaces/get_node",
        queries=[("token", wiki_token)],
        user_token=user_token,
    )
    node = body.get("data", {}).get("node", {})
    return node.get("obj_token"), node.get("obj_type"), node.get("title")
