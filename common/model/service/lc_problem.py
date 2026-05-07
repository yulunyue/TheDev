from ..base import BaseModel
from common.third_service.get_service import get_lc_service
from common.util.export import File, C, logger, Tuple
import time


class LcProblem(BaseModel):
    def load(self, titleSlug, id, translatedTitle, questionFrontendId, **kw):
        self.titleSlug, self.id, self.translatedTitle = titleSlug, id, translatedTitle
        self.questionFrontendId = questionFrontendId
        return self

    def submit(self, code):
        s = get_lc_service()
        check = s.submit(self.titleSlug, self.id, code)
        state = s.check(check)
        logger.map(
            title=self.titleSlug,
            check=check,
            outputDetail=state.outputDetail,
            passedTestCaseCnt=state.passedTestCaseCnt,
            totalTestCaseCnt=state.totalTestCaseCnt,
        )
        return state.totalTestCaseCnt

    def get_code(self) -> Tuple[str, str]:
        question = get_lc_service().query_detail(self.titleSlug)["data"]["question"]
        codeSnippets, sampleTestCase, content = (
            question["codeSnippets"],
            question["sampleTestCase"],
            question["content"],
        )
        for code in codeSnippets:
            if code["lang"] == "Python3":
                return code["code"], sampleTestCase
        return "", ""
