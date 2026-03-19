def get_dom_type(v, key=None, size=1):
    if isinstance(v, dict):
        return v
    elif hasattr(v, "to_json"):
        return v.to_json()
    return dict(key=v, value=v, type="str", size=size)
