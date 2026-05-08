from ..base import BaseModel
from common.third_service.get_service import get_lc_service
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
        submissionId = get_lc_service().submit(self.titleSlug, self.id, code)
        self.check(submissionId)

    def check(self, submissionId):
        storge = self.get_storge()

        while True:
            state = get_lc_service().check(submissionId)
            logger.map(
                passedTestCaseCnt=state.passedTestCaseCnt,
                totalTestCaseCnt=state.totalTestCaseCnt,
                case=state.outputDetail,
                status=state.statusDisplay,
            )
            error_msg = (
                state.outputDetail["compileError"] + state.outputDetail["runtimeError"]
            )
            if state.statusDisplay in {""} or error_msg:
                raise Exception(state.statusDisplay, error_msg)
            if state.statusDisplay in {""}:
                break
            time.sleep(1)
        storge.set(
            self.questionFrontendId, "cases", submissionId, value=state.outputDetail
        )

    def get_code(self) -> str:
        if self.code:
            return self.code
        question = get_lc_service().query_detail(self.titleSlug)["data"]["question"]
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
        lc = get_lc_service()
        t = lc.query_num(number)
        code = t.get_code()
        t.f.write_file(
            f"from common.util.export import List, Dict, functools, CT\n{code}return"
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
