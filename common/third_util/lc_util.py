from common.service.api import Api


class LeetCode(Api):
    def check(self, check_id="629525294"):
        return self.get(f"/submissions/detail/{check_id}/check/")

    def get_endpoint(self):
        return "https://leetcode.cn"
    
    def submit(self, name="total-characters-in-string-after-transformations-i",code="import sys"):
        return self.post(f"/problems/{name}/submit",dict(lang="python3",question_id="3629",code=code))
