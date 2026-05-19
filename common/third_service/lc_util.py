from common.third_util.io.api import Api
from common.model.export import LcProblem, LcSubmissionDetail
from common.util.export import File, Module

from .lc_cache import LcCache, CACHE_DIR
from .lc_parser import LcContentParser
from .lc_tester import LcLocalTester, CODE_DIR

CACHE_DIR = CACHE_DIR
CODE_DIR = CODE_DIR
LANG = "Python3"


class LcError(Exception):
    pass


class LeetCode(Api):
    CACHE_DIR = CACHE_DIR
    CODE_DIR = CODE_DIR

    def _refresh_auth(self):
        """
        401 时自动重新登录获取新的 session
        """
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

    def login_with_selenium(self, headless=True) -> str:
        username = self.get_username()
        password = self.get_password()
        if not username or not password:
            raise LcError("LeetCode credentials not configured in api.json")

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(options=options)
        try:
            wait = WebDriverWait(driver, 15)
            driver.get(f"{self.get_endpoint()}/accounts/login/")

            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='login']"))
            ).send_keys(username)

            driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(
                password
            )

            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            wait.until(lambda d: "/accounts/login/" not in d.current_url)

            for c in driver.get_cookies():
                if c["name"] == "LEETCODE_SESSION":
                    session = c["value"]
                    break
            else:
                raise LcError("Login succeeded but no LEETCODE_SESSION cookie found")
        finally:
            driver.quit()

        from common.third_util.io.api import API_CONFIG

        config = API_CONFIG.get(self.name)
        config.cookie.set_value(dict(LEETCODE_SESSION=session))
        config.save_to_local()
        return session

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

    def query_num(self, num: str) -> LcProblem:
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

    def submit(self, title_slug: str = None) -> str:
        daily = self.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = LcCache.load(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)

        question_id = cache["question_id"]
        code_path = f"{CODE_DIR}/lc_{question_id}.py"

        if not File(code_path).exists():
            raise LcError(f"Code file not found: {code_path}")

        code = File(code_path).read_file()
        data = self.post(
            f"/problems/{title_slug}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )
        return data["submission_id"]

    def graphql(self, query: str, variables: dict, operationName: str = None) -> dict:
        param = dict(query=query, variables=variables)
        if operationName:
            param["operationName"] = operationName
        return self.post("/graphql", param)

    def prepare_submit(self, title_slug: str = None) -> dict:
        daily = self.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = LcCache.load(title_slug)
        if cache:
            return cache

        if title_slug == daily["titleSlug"]:
            question_id = daily["questionFrontendId"]
            title = daily["title"]
            difficulty = daily["difficulty"]
        else:
            problem = self.query_num(title_slug.split("-")[-1])
            question_id = problem.questionFrontendId
            title = problem.title
            difficulty = problem.difficulty

        detail = self.query_detail(title_slug)
        question_data = detail["data"]["question"]

        test_cases = LcContentParser.build_test_cases(
            question_data["content"], question_data["sampleTestCase"]
        )

        cache_data = {
            "question_id": question_id,
            "title_slug": title_slug,
            "title": title,
            "difficulty": difficulty,
            "code_snippet": LcContentParser.get_code_snippet(
                question_data["codeSnippets"]
            ),
            "test_cases": test_cases,
            "content": question_data["content"],
        }
        return LcCache.save(title_slug, cache_data)

    def test_local(self, title_slug: str = None) -> dict:
        daily = self.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = LcCache.load(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)

        return LcLocalTester.test(cache)
