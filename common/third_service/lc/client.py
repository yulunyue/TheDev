from common.third_util.io.api import Api
from common.model.export import LcSubmissionDetail
from .config import QUESTION_OF_TODAY, SEARCH_QUESTION_LIST, GET_QUESTION_DETAIL, SUBMISSION_DETAILS
from .error import LcError


class LcClient(Api):
    def login_with_selenium(self) -> str:
        from common.third_util.tool.selenium_util import SeleniumUtil
        from common.third_util.io.api import API_CONFIG

        s = SeleniumUtil(dev_port=9527)
        try:
            s.load()
        except Exception as e:
            cmd = str(e).strip()
            if not ("--remote-debugging-port" in cmd):
                raise
            import subprocess

            subprocess.Popen(
                cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            print("Chrome 调试浏览器已启动（端口 9527）")
            import time

            time.sleep(2)
            s.load()
        s.driver.get(f"{self.get_endpoint()}/")

        print("请在浏览器中登录 leetcode.cn，完成后按 Enter 继续...")
        input()

        session = s.get_cookies(name="LEETCODE_SESSION")
        if not session or isinstance(session, dict):
            raise LcError("未检测到 LEETCODE_SESSION cookie，请确认已登录")

        config = API_CONFIG.get(self.name)
        config.cookie.set_value(dict(LEETCODE_SESSION=session))
        config.save_to_local()
        print("LEETCODE_SESSION 已保存")
        return session

    def graphql(self, query: str, variables: dict, operationName: str = None) -> dict:
        param = dict(query=query, variables=variables)
        if operationName:
            param["operationName"] = operationName
        return self.post("/graphql", param)

    def get_daily(self) -> dict:
        data = self.graphql(QUESTION_OF_TODAY, {}, "questionOfToday")
        return data["data"]["todayRecord"][0]["question"]

    def query_num(self, num: str):
        from common.model.export import LcProblem

        data = self.graphql(
            SEARCH_QUESTION_LIST, dict(searchKeyword=num, limit=1, skip=0), "searchQuestionList"
        )
        questions = data["data"]["problemsetQuestionListV2"]["questions"]
        if len(questions) != 1:
            raise LcError(f"Question not found: {num}", data)
        ret = LcProblem().set_data(**questions[0])
        if ret.questionFrontendId != num:
            raise LcError(f"Question ID mismatch: {num} vs {ret.questionFrontendId}")
        return ret

    def query_detail(self, title_slug: str) -> dict:
        return self.graphql(GET_QUESTION_DETAIL, dict(titleSlug=title_slug), "getQuestionDetail")

    def check(self, submissionId: str) -> LcSubmissionDetail:
        data = self.graphql(SUBMISSION_DETAILS, dict(submissionId=submissionId), "submissionDetails")
        return LcSubmissionDetail().set_data(**data["data"]["submissionDetail"])