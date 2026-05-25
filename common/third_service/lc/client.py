from common.third_util.io.api import Api
from common.model.export import LcSubmissionDetail
from common.util.export import File
from .config import LANG, CODE_DIR, CACHE_DIR
from .error import LcError


class LcClient(Api):
    CACHE_DIR = CACHE_DIR
    CODE_DIR = CODE_DIR

    def _refresh_auth(self):
        try:
            session = self.login()
            from common.third_util.io.api import API_CONFIG

            config = API_CONFIG.get(self.name)
            config.cookie.set_value(dict(LEETCODE_SESSION=session))
            config.save_to_local()
            return session
        except LcError as e:
            raise LcError(f"自动登录失败: {e}")

    def login(self) -> str:
        import requests
        import urllib3
        from common.third_util.io.api import API_CONFIG, USER_AGENT_DEFAULT

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        username = self.get_username()
        password = self.get_password()
        if not username or not password:
            raise LcError("LeetCode credentials not configured in api.json")

        sess = requests.Session()
        sess.headers.update({"User-Agent": USER_AGENT_DEFAULT})
        sess.get(f"{self.get_endpoint()}/accounts/login/", verify=False)
        csrf = sess.cookies.get("csrftoken", "")
        res = sess.post(
            f"{self.get_endpoint()}/accounts/login/",
            data=dict(login=username, password=password),
            headers={
                "Referer": f"{self.get_endpoint()}/accounts/login/",
                "X-CSRFToken": csrf,
            },
            verify=False,
        )
        session = res.cookies.get("LEETCODE_SESSION") or sess.cookies.get(
            "LEETCODE_SESSION"
        )
        if not session:
            raise LcError(
                "Login failed. LeetCode may require OAuth/captcha.\n"
                "To get the session cookie manually:\n"
                "  1. Open browser, login to https://leetcode.cn\n"
                "  2. Open DevTools > Application > Cookies\n"
                "  3. Copy the value of LEETCODE_SESSION\n"
                "  4. Set it in config/setting/api.json:\n"
                '     "cookie": {"LEETCODE_SESSION": "<your_session>"}'
            )

        config = API_CONFIG.get(self.name)
        config.cookie.set_value(dict(LEETCODE_SESSION=session))
        config.save_to_local()
        return session

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

    def login_with_browser_use(self) -> str:
        username = self.get_username()
        password = self.get_password()
        if not username or not password:
            raise LcError("LeetCode credentials not configured in api.json")

        from browser_use import Agent
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model="codeagent/MiniMax-M2.5",
            base_url="http://10.159.226.57:31943/v1",
            api_key="placeholder",
        )

        task = f"""
Go to https://leetcode.cn/accounts/login/
Wait for page to load
Fill in the login form:
- Find input field with name 'login' and enter: {username}
- Find input field with name 'password' and enter: {password}
Click the submit button to login
Wait for login to complete (URL changes from /accounts/login/)
Return the LEETCODE_SESSION cookie value
"""

        agent = Agent(task=task, llm=llm)
        result = agent.run()

        session = str(result)

        from common.third_util.io.api import API_CONFIG

        config = API_CONFIG.get(self.name)
        config.cookie.set_value(dict(LEETCODE_SESSION=session))
        config.save_to_local()
        return session

    def graphql(self, query: str, variables: dict, operationName: str = None) -> dict:
        param = dict(query=query, variables=variables)
        if operationName:
            param["operationName"] = operationName
        return self.post("/graphql", param)

    def get_daily(self) -> dict:
        query = """
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
        data = self.graphql(query, {}, "questionOfToday")
        return data["data"]["todayRecord"][0]["question"]

    def query_num(self, num: str):
        from common.model.export import LcProblem

        query = """
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
        data = self.graphql(
            query, dict(searchKeyword=num, limit=1, skip=0), "searchQuestionList"
        )
        questions = data["data"]["problemsetQuestionListV2"]["questions"]
        if len(questions) != 1:
            raise LcError(f"Question not found: {num}", data)
        ret = LcProblem().set_data(**questions[0])
        if ret.questionFrontendId != num:
            raise LcError(f"Question ID mismatch: {num} vs {ret.questionFrontendId}")
        return ret

    def query_detail(self, title_slug: str) -> dict:
        query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    codeSnippets { lang code }
    sampleTestCase
    content
  }
}
"""
        return self.graphql(query, dict(titleSlug=title_slug), "getQuestionDetail")

    def check(self, submissionId: str) -> LcSubmissionDetail:
        query = """
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
        data = self.graphql(query, dict(submissionId=submissionId), "submissionDetails")
        return LcSubmissionDetail().set_data(**data["data"]["submissionDetail"])
