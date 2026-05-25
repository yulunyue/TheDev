from ..base import BaseModel
from common.util.export import File, C, logger, Tuple
import time


class LcProblem(BaseModel):
    def load(
        self, titleSlug, id, translatedTitle, questionFrontendId, fun_name="", **kw
    ):
        self.fun_name = fun_name
        self.titleSlug, self.id, self.translatedTitle = titleSlug, id, translatedTitle
        self.questionFrontendId = questionFrontendId
        self.f = File(f"app/yly/algo/todo/lc_{questionFrontendId}.py")
        self.code = ""
        return self

    def submit(self, code):
        from common.third_service.lc import get_lc_service, LcProblemService
        client = get_lc_service()
        service = LcProblemService(client)
        submissionId = service.submit(self.titleSlug, code)
        self.check(submissionId)

    def check(self, submissionId):
        from common.third_service.lc import get_lc_service
        storge = self.get_storge()
        client = get_lc_service()

        while True:
            state = client.check(submissionId)
            logger.map(
                passedTestCaseCnt=state.passedTestCaseCnt,
                totalTestCaseCnt=state.totalTestCaseCnt,
                status=state.statusDisplay,
            )
            error_msg = (
                state.outputDetail["compileError"] + state.outputDetail["runtimeError"]
            )
            if state.statusDisplay in {"Time Limit Exceeded"} or error_msg:
                raise Exception(state.statusDisplay, error_msg)
            if state.statusDisplay in {"Wrong Answer", "Accepted"}:
                break
            time.sleep(4)
        storge.set(
            self.questionFrontendId, "cases", submissionId, value=state.outputDetail
        )

    def get_code(self) -> str:
        from common.third_service.lc import get_lc_service
        if self.code:
            return self.code
        client = get_lc_service()
        question = client.query_detail(self.titleSlug)["data"]["question"]
        codeSnippets, sampleTestCase, content = (
            question["codeSnippets"],
            question["sampleTestCase"],
            question["content"],
        )
        for code in codeSnippets:
            if code["lang"] == "Python3":
                self.code = code["code"]
        return self.code

    @classmethod
    def make(cls, number):
        from common.third_service.lc import get_lc_service
        client = get_lc_service()
        t = client.query_num(number)
        code = t.get_code()

        t.f.write_if_not_exists(
            f"from common.util.export import List, Dict, functools, CT, LOG\n\n\n{code}return"
        )
        t.fun_name = code.split("def ").pop().split("(")[0]
        return t.to_json()

    def to_json(self):
        return dict(
            fun_name=self.fun_name,
            titleSlug=self.titleSlug,
            id=self.id,
            translatedTitle=self.translatedTitle,
            questionFrontendId=self.questionFrontendId,
        )
