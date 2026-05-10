from ..base import BaseModel


class LcSubmissionDetail(BaseModel):
    def load(
        self,
        statusDisplay,
        outputDetail,
        code,
        passedTestCaseCnt,
        totalTestCaseCnt,
        **kw,
    ):
        self.code = code
        self.passedTestCaseCnt = passedTestCaseCnt
        self.totalTestCaseCnt = totalTestCaseCnt
        self.statusDisplay = statusDisplay
        self.outputDetail = outputDetail
        return super().load(**kw)
