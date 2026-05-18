import unittest
from unittest.mock import patch, MagicMock


class TestPrInfoReview(unittest.TestCase):
    def setUp(self):
        self.mock_github_api = patch(
            "common.model.git.pr_info.GitHubApi"
        )
        self.mock_api_instance = self.mock_github_api.start()

        self.mock_opencode = patch(
            "common.model.git.pr_info.OpencodeClient"
        )
        self.mock_opencode_instance = self.mock_opencode.start()

    def tearDown(self):
        self.mock_github_api.stop()
        self.mock_opencode.stop()

    def test_get_diff_content(self):
        from common.model.git.pr_info import PrInfo

        mock_api = MagicMock()
        mock_api.get_pr_diff.return_value = "diff --git a/file.py b/file.py\n--- a/file.py\n+++ b/file.py"
        self.mock_api_instance.return_value.load.return_value = mock_api

        pr = PrInfo().set_owner("test_owner").set_repo("test_repo").set_number(42)
        diff = pr.get_diff_content()

        self.assertIn("diff --git", diff)

    def test_get_issue_content_with_issue(self):
        from common.model.git.pr_info import PrInfo

        mock_api = MagicMock()
        mock_api.get_pr_link_isure.return_value = [
            {"number": 15, "url": "https://github.com/test/issue/15"}
        ]
        mock_api.get_issue.return_value = {
            "title": "Test Issue",
            "body": "Issue description",
        }
        self.mock_api_instance.return_value.load.return_value = mock_api

        pr = PrInfo().set_owner("test_owner").set_repo("test_repo").set_number(42)
        issue_info = pr.get_issue_content()

        self.assertIsNotNone(issue_info)
        self.assertEqual(issue_info["title"], "Test Issue")

    def test_get_issue_content_no_issue(self):
        from common.model.git.pr_info import PrInfo

        mock_api = MagicMock()
        mock_api.get_pr_link_isure.return_value = None
        self.mock_api_instance.return_value.load.return_value = mock_api

        pr = PrInfo().set_owner("test_owner").set_repo("test_repo").set_number(42)
        issue_info = pr.get_issue_content()

        self.assertIsNone(issue_info)

    def test_get_review_suggestion_success(self):
        from common.model.git.pr_info import PrInfo

        mock_api = MagicMock()
        mock_api.get_pr_diff.return_value = "diff --git a/file.py b/file.py\n--- a/file.py\n+++ b/file.py"
        mock_api.get_pr_link_isure.return_value = None
        mock_api.get_pr_info.return_value = {"files": {"title": "Test PR"}}
        self.mock_api_instance.return_value.load.return_value = mock_api

        mock_session = MagicMock()
        mock_session.id = "test_session_id"

        mock_client = MagicMock()
        mock_client.create_session.return_value = mock_session
        mock_client.execute_task.return_value = '''{
            "suggestions": [
                {
                    "file": "file.py",
                    "line_range": [1, 10],
                    "severity": "medium",
                    "type": "style",
                    "message": "Code style issue",
                    "suggestion": "Refactor for better readability"
                }
            ],
            "summary": "Code quality is acceptable"
        }'''
        self.mock_opencode_instance.return_value = mock_client

        pr = PrInfo().set_owner("test_owner").set_repo("test_repo").set_number(42)
        pr.title = "Test PR"
        result = pr.get_review_suggestion()

        self.assertIn("pr_title", result)
        self.assertEqual(result["pr_number"], 42)
        self.assertIn("suggestions", result)
        self.assertIn("summary", result)

    def test_get_review_suggestion_with_error(self):
        from common.model.git.pr_info import PrInfo

        mock_api = MagicMock()
        mock_api.get_pr_diff.side_effect = Exception("API error")
        self.mock_api_instance.return_value.load.return_value = mock_api

        pr = PrInfo().set_owner("test_owner").set_repo("test_repo").set_number(42)
        result = pr.get_review_suggestion()

        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()