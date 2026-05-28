import json
from common.util.export import File

LANG = "Python3"
CODE_DIR = "app/yly/algo/todo"
CACHE_DIR = "data/lc"

QUESTION_OF_TODAY = """
query questionOfToday {
  todayRecord {
    question {
      questionFrontendId
      title
      titleSlug
      difficulty
    }
    date
  }
}
"""

SEARCH_QUESTION_LIST = """
query searchQuestionList($limit: Int, $searchKeyword: String, $skip: Int) {
  problemsetQuestionListV2(limit: $limit, searchKeyword: $searchKeyword, skip: $skip) {
    questions {
      id titleSlug title translatedTitle questionFrontendId paidOnly difficulty
      topicTags { name slug nameTranslated }
      status isInMyFavorites frequency acRate contestPoint
    }
    totalLength finishedLength hasMore
  }
}
"""

GET_QUESTION_DETAIL = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    codeSnippets { lang code }
    sampleTestCase
    content
    translatedContent
    questionFrontendId
  }
}
"""

SUBMISSION_DETAILS = """
query submissionDetails($submissionId: ID!) {
  submissionDetail(submissionId: $submissionId) {
    code
    timestamp
    statusDisplay
    isMine
    runtimeDisplay: runtime
    memoryDisplay: memory
    memory: rawMemory
    lang
    langVerboseName
    question {
      questionId
      titleSlug
      hasFrontendPreview
    }
    user {
      realName
      userAvatar
      userSlug
    }
    runtimePercentile
    memoryPercentile
    submissionComment {
      flagType
    }
    passedTestCaseCnt
    totalTestCaseCnt
    fullCodeOutput
    testDescriptions
    testInfo
    testBodies
    stdOutput
    aiJudgeMessage
    isCompiledLang
    aiRecheckSubmitted
    ... on GeneralSubmissionNode {
      outputDetail {
        codeOutput
        expectedOutput
        input
        compileError
        runtimeError
        lastTestcase
      }
    }
    ... on ContestSubmissionNode {
      outputDetail {
        codeOutput
        expectedOutput
        input
        compileError
        runtimeError
        lastTestcase
      }
    }
  }
}
"""


class LcCache:
    DIR = CACHE_DIR

    @classmethod
    def get_path(cls, title_slug: str) -> str:
        return f"{cls.DIR}/{title_slug}.json"

    @classmethod
    def load(cls, title_slug: str):
        path = cls.get_path(title_slug)
        f = File(path)
        if f.exists():
            return f.read_file()
        return None

    @classmethod
    def save(cls, title_slug: str, data: dict) -> dict:
        path = cls.get_path(title_slug)
        File(path).make_dir_if_not_exist().write_file(
            json.dumps(data, ensure_ascii=False, indent=2)
        )
        return data
