from common.third_util.io.api import Api
from common.model.export import LcProblem


class LeetCode(Api):
    def check(self, check_id="629525294"):
        return self.get(f"/submissions/detail/{check_id}/check")

    def get_endpoint(self):
        return "https://leetcode.cn"

    def submit(self, name, question_id, code):
        data = self.post(
            f"/problems/{name}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )
        return data["submission_id"]

    def query_num(self, num):
        data = self.graphql(
            dict(
                query="\n    query searchQuestionList($limit: Int, $searchKeyword: String, $skip: Int) {\n  problemsetQuestionListV2(\n    limit: $limit\n    searchKeyword: $searchKeyword\n    skip: $skip\n  ) {\n    questions {\n      id\n      titleSlug\n      title\n      translatedTitle\n      questionFrontendId\n      paidOnly\n      difficulty\n      topicTags {\n        name\n        slug\n        nameTranslated\n      }\n      status\n      isInMyFavorites\n      frequency\n      acRate\n      contestPoint\n    }\n    totalLength\n    finishedLength\n    hasMore\n  }\n}\n    ",
                variables=dict(searchKeyword=num, limit=1, skip=0),
                operationName="searchQuestionList",
            )
        )
        try:
            questions = data["data"]["problemsetQuestionListV2"]["questions"]
            if len(questions) != 1:
                raise Exception(questions, num)
            ret = LcProblem().set_data(**questions[0])
            if ret.questionFrontendId != num:
                raise Exception(num, ret.questionFrontendId)
            return ret
        except Exception as e:
            raise Exception(e, data)

    def graphql(self, data):
        return self.post(f"/graphql", data)


if __name__ == "__main__":
    Api.enable_globel_log()
    print(LeetCode().query_num(200))
