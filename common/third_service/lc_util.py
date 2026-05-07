from common.third_util.io.api import Api


class LeetCode(Api):
    def check(self, check_id="629525294"):
        return self.get(f"/submissions/detail/{check_id}/check/")

    def get_endpoint(self):
        return "https://leetcode.cn"

    def submit(self, name, question_id, code):
        return self.post(
            f"/problems/{name}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )


if __name__ == "__main__":
    Api.enable_globel_log()
    print(LeetCode().submit())
