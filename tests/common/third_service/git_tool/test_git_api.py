import unittest
from unittest.mock import patch, MagicMock


class TestGitHubApi(unittest.TestCase):
    def setUp(self):
        self.mock_http = patch("common.third_service.git_tool.git_api.GitHubApi.http")
        self.mock_http_instance = self.mock_http.start()
        self.mock_http_instance.return_value = (MagicMock(), {})

        from common.third_service.git_tool.git_api import GitHubApi

        self.api = GitHubApi().load("test_owner", "test_repo")

    def tearDown(self):
        self.mock_http.stop()

    def test_creation(self):
        from common.third_service.git_tool.git_api import GitHubApi

        api = GitHubApi()
        self.assertIsNotNone(api)

    def test_load(self):
        self.assertEqual(self.api.owner, "test_owner")
        self.assertEqual(self.api.repo, "test_repo")

    def test_get_endpoint(self):
        self.assertEqual(self.api.get_endpoint(), "https://api.github.com")

    def test_get_pr(self):
        self.api.get_pr(42)
        self.mock_http_instance.assert_called_once()
        args, kwargs = self.mock_http_instance.call_args
        method = args[0]
        path = args[1] if len(args) > 1 else kwargs.get("path", "")
        self.assertEqual(method, "GET")
        self.assertIn("42", path)

    def test_get_pr_info(self):
        self.api.get_pr_info(42)
        self.mock_http_instance.assert_called_once()
        args, kwargs = self.mock_http_instance.call_args
        path = args[1] if len(args) > 1 else kwargs.get("path", "")
        self.assertIn("42", path)

    def test_get_pr_files(self):
        self.api.get_pr_files(42)
        self.mock_http_instance.assert_called_once()
        args, kwargs = self.mock_http_instance.call_args
        path = args[1] if len(args) > 1 else kwargs.get("path", "")
        self.assertIn("42", path)
        self.assertIn("files", path)

    def test_graphql(self):
        self.mock_http_instance.return_value = (MagicMock(), {"data": {}})
        self.api.graphql("query { test }")
        self.mock_http_instance.assert_called_once()
        args, kwargs = self.mock_http_instance.call_args
        method = args[0]
        path = args[1] if len(args) > 1 else kwargs.get("path", "")
        self.assertEqual(method, "POST")
        self.assertIn("graphql", path)

    def test_get_pr_link_isure_no_errors(self):
        mock_resp = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "closingIssuesReferences": {
                            "nodes": [
                                {"number": 1, "url": "https://github.com/issue/1"}
                            ]
                        }
                    }
                }
            }
        }
        self.mock_http_instance.return_value = (MagicMock(), mock_resp)
        result = self.api.get_pr_link_isure(42)
        self.assertEqual(len(result), 1)

    def test_get_pr_link_isure_with_errors(self):
        mock_resp = {"errors": ["some error"]}
        self.mock_http_instance.return_value = (MagicMock(), mock_resp)
        result = self.api.get_pr_link_isure(42)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
