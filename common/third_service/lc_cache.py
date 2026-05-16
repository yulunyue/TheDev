import json
from common.util.export import File

CACHE_DIR = "data/lc"


class LcCache:
    DIR = CACHE_DIR

    @classmethod
    def get_path(cls, title_slug: str) -> str:
        return f"{cls.DIR}/{title_slug}.json"

    @classmethod
    def load(cls, title_slug: str):
        path = cls.get_path(title_slug)
        f = File(path)
        if f.exists():
            return f.read_file()
        return None

    @classmethod
    def save(cls, title_slug: str, data: dict) -> dict:
        path = cls.get_path(title_slug)
        File(path).make_dir_if_not_exist().write_file(
            json.dumps(data, ensure_ascii=False, indent=2)
        )
        return data
