from common.third_util.io.api import Api
from common.model.export import LcProblem, LcSubmissionDetail
from common.util.export import File, logger, Module
import sys

LOCAL_STORGE = File("data/leetcode/storge.json").write_if_not_exists({})
logger.info(LOCAL_STORGE)


class LeetCode(Api):
    LOG_ENABLE_DEFAULT = True

    def check(self, submissionId):
        query = "\n    query submissionDetails($submissionId: ID!) {\n  submissionDetail(submissionId: $submissionId) {\n    code\n    timestamp\n    statusDisplay\n    isMine\n    runtimeDisplay: runtime\n    memoryDisplay: memory\n    memory: rawMemory\n    lang\n    langVerboseName\n    question {\n      questionId\n      titleSlug\n      hasFrontendPreview\n    }\n    user {\n      realName\n      userAvatar\n      userSlug\n    }\n    runtimePercentile\n    memoryPercentile\n    submissionComment {\n      flagType\n    }\n    passedTestCaseCnt\n    totalTestCaseCnt\n    fullCodeOutput\n    testDescriptions\n    testInfo\n    testBodies\n    stdOutput\n    aiJudgeMessage\n    isCompiledLang\n    aiRecheckSubmitted\n    ... on GeneralSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n    ... on ContestSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n  }\n}\n    "
        data = self.graphql(query, dict(submissionId=submissionId), "submissionDetails")
        return LcSubmissionDetail().set_data(**data["data"]["submissionDetail"])

    def get_endpoint(self):
        return "https://leetcode.cn"

    def submit(self, name, question_id, code):
        data = self.post(
            f"/problems/{name}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )
        return data["submission_id"]

    def query_detail(self, title):
        query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    codeSnippets { lang code }
    sampleTestCase
    content
  }
}
"""
        data = self.graphql(query, dict(titleSlug=title), "getQuestionDetail")
        return data

    def query_num(self, num):
        data = self.graphql(
            "\n    query searchQuestionList($limit: Int, $searchKeyword: String, $skip: Int) {\n  problemsetQuestionListV2(\n    limit: $limit\n    searchKeyword: $searchKeyword\n    skip: $skip\n  ) {\n    questions {\n      id\n      titleSlug\n      title\n      translatedTitle\n      questionFrontendId\n      paidOnly\n      difficulty\n      topicTags {\n        name\n        slug\n        nameTranslated\n      }\n      status\n      isInMyFavorites\n      frequency\n      acRate\n      contestPoint\n    }\n    totalLength\n    finishedLength\n    hasMore\n  }\n}\n    ",
            dict(searchKeyword=num, limit=1, skip=0),
            "searchQuestionList",
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

    def graphql(self, query, variables, operationName=None):
        param = dict(query=query, variables=variables)
        if operationName:
            param.update(operationName=operationName)
        return self.post(f"/graphql", param)

    def run(self, number):
        f = File(f"app/yly/algo/todo/lc_{number}.py")
        if not f.exists():
            t = self.query_num(number)
            code, case = t.get_code()
            f.write_file(
                f"from common.util.export import List, Dict, functools, CT\n{code}"
            )
            LOCAL_STORGE.set(number, "cases", value=dict(case0=[case]))
        cases = LOCAL_STORGE.get(number, "cases")
        fun_name = code.split("def ").pop().split("(")[0]
        fun = Module().load_module_object(
            f"app.yly.algo.todo.lc_{number}::Solution::{fun_name}"
        )
        for case in cases:
            exp = case[-1]
            result = fun(*case[:-1])
            if exp != result:
                raise Exception(f"{result}:{exp}")
