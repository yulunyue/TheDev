from ..base import BaseModel
from common.third_service.get_service import get_lc_service
from common.util.export import File, C, logger

LOCAL_STORGE = File("data/leetcode/storge.json").write_if_not_exists({})
logger.info(LOCAL_STORGE)


class LcProblem(BaseModel):
    def load(self, titleSlug, id, translatedTitle, questionFrontendId, **kw):
        self.titleSlug, self.id, self.translatedTitle = titleSlug, id, translatedTitle
        self.questionFrontendId = questionFrontendId
        return self

    def submit(self, code):
        check = LOCAL_STORGE.set(
            self.questionFrontendId,
            C.CHECK,
            value=lambda: get_lc_service().submit(self.titleSlug, self.id, code),
        )
        statu = LOCAL_STORGE.set(
            self.questionFrontendId,
            C.STATE,
            value=lambda: get_lc_service().check(check),
        )
        logger.map(check=check, statu=statu)
