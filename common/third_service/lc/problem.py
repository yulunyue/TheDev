from common.util.export import File
from common.model.export import LcSubmissionDetail
from .config import LANG, CODE_DIR, CACHE_DIR, LcCache
from .error import LcError
from .parser import LcContentParser
from .client import LcClient


class LcProblemService:
    def __init__(self, client: LcClient):
        self.client = client

    def prepare_submit(self, title_slug: str = None) -> dict:
        daily = self.client.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = LcCache.load(title_slug)
        if cache:
            return cache

        detail = self.client.query_detail(title_slug)
        question_data = detail["data"]["question"]

        if title_slug == daily["titleSlug"]:
            question_id = daily["questionFrontendId"]
            title = daily["title"]
            difficulty = daily["difficulty"]
        else:
            question_id = question_data.get("questionFrontendId", "")
            info = self.client.query_num(question_id).kw
            title = info.get("title", "")
            difficulty = info.get("difficulty", "")

        test_cases = LcContentParser.build_test_cases(
            question_data["content"], question_data["sampleTestCase"]
        )

        cache_data = {
            "question_id": question_id,
            "title_slug": title_slug,
            "title": title,
            "difficulty": difficulty,
            "code_snippet": LcContentParser.get_code_snippet(
                question_data["codeSnippets"]
            ),
            "test_cases": test_cases,
            "content": question_data["content"],
        }
        return LcCache.save(title_slug, cache_data)

    def submit(self, title_slug: str = None, code: str = None) -> str:
        daily = self.client.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = LcCache.load(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)

        question_id = cache["question_id"]

        if code is None:
            code_path = f"{CODE_DIR}/lc_{question_id}.py"
            if not File(code_path).exists():
                raise LcError(f"Code file not found: {code_path}")
            code = File(code_path).read_file()

        data = self.client.post(
            f"/problems/{title_slug}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )
        return data["submission_id"]
