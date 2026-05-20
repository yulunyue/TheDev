import sys
import unittest
from unittest.mock import patch, MagicMock

sys.modules["opencode_ai"] = MagicMock()
sys.modules["opencode_ai.types"] = MagicMock()
sys.modules["opencode_ai.types.session"] = MagicMock()
sys.modules["opencode_ai.types.text_part_input_param"] = MagicMock()


class TestOpencodeClient(unittest.TestCase):

    def _make_config_mock(self, **kwargs):
        config = MagicMock()
        for key, value in kwargs.items():
            getter = MagicMock()
            getter.get_value.return_value = value
            setattr(config, key, getter)
        return config

    def setUp(self):
        self.config_patcher = patch(
            "common.third_util.llm.opencode_client.LlmConfig"
        )
        self.mock_llm_config = self.config_patcher.start()
        self.mock_config = self._make_config_mock(
            base_url="http://test.url/v1",
            provider_id="test_provider",
            model_id="test_model",
        )
        self.mock_llm_config.get.return_value = self.mock_config

    def tearDown(self):
        self.config_patcher.stop()

    def test_init_default_config(self):
        from common.third_util.llm.opencode_client import OpencodeClient

        OpencodeClient()
        self.mock_llm_config.get.assert_called_with("opencode")

    def test_init_custom_config(self):
        from common.third_util.llm.opencode_client import OpencodeClient

        OpencodeClient("custom_config")
        self.mock_llm_config.get.assert_called_with("custom_config")

    def test_provider_id(self):
        from common.third_util.llm.opencode_client import OpencodeClient

        client = OpencodeClient()
        self.assertEqual(client.provider_id, "test_provider")

    def test_model_id(self):
        from common.third_util.llm.opencode_client import OpencodeClient

        client = OpencodeClient()
        self.assertEqual(client.model_id, "test_model")

    def test_client_lazy_init(self):
        from common.third_util.llm.opencode_client import OpencodeClient

        client = OpencodeClient()
        self.assertIsNone(client._client)
        _ = client.client
        self.assertIsNotNone(client._client)
        self.assertIsNotNone(_)

    @patch("common.third_util.llm.opencode_client.Opencode")
    def test_create_session(self, mock_opencode):
        from common.third_util.llm.opencode_client import OpencodeClient

        mock_session = MagicMock()
        mock_session.id = "session_123"
        mock_opencode_instance = MagicMock()
        mock_opencode_instance.session.create.return_value = mock_session
        mock_opencode.return_value = mock_opencode_instance

        client = OpencodeClient()
        session = client.create_session()
        self.assertEqual(session.id, "session_123")

    @patch("common.third_util.llm.opencode_client.Opencode")
    def test_create_session_with_title(self, mock_opencode):
        from common.third_util.llm.opencode_client import OpencodeClient

        mock_session = MagicMock()
        mock_session.id = "session_456"
        mock_opencode_instance = MagicMock()
        mock_opencode_instance.session.create.return_value = mock_session
        mock_opencode.return_value = mock_opencode_instance

        client = OpencodeClient()
        session = client.create_session(title="test_title")
        mock_opencode_instance.session.create.assert_called_with(
            extra_body=dict(title="test_title")
        )
        self.assertEqual(session.id, "session_456")

    @patch("common.third_util.llm.opencode_client.Opencode")
    def test_execute_task(self, mock_opencode):
        from common.third_util.llm.opencode_client import OpencodeClient

        mock_result = MagicMock()
        mock_result.content = "test response"
        mock_opencode_instance = MagicMock()
        mock_opencode_instance.session.chat.return_value = mock_result
        mock_opencode.return_value = mock_opencode_instance

        client = OpencodeClient()
        result = client.execute_task("session_id", "hello")
        self.assertEqual(result, "test response")

        call_args = mock_opencode_instance.session.chat.call_args
        self.assertEqual(call_args[1]["id"], "session_id")
        self.assertEqual(call_args[1]["model_id"], "")
        self.assertEqual(call_args[1]["provider_id"], "")
        self.assertEqual(len(call_args[1]["parts"]), 1)

    @patch("common.third_util.llm.opencode_client.Opencode")
    def test_execute_task_uses_model_dump(self, mock_opencode):
        from common.third_util.llm.opencode_client import OpencodeClient

        mock_result = MagicMock(spec=["model_dump"])
        mock_result.model_dump.return_value = {"key": "value"}
        mock_opencode_instance = MagicMock()
        mock_opencode_instance.session.chat.return_value = mock_result
        mock_opencode.return_value = mock_opencode_instance

        client = OpencodeClient()
        result = client.execute_task("sid", "hi")
        self.assertEqual(result, {"key": "value"})

    @patch("common.third_util.llm.opencode_client.Opencode")
    def test_execute_task_falls_back_to_str(self, mock_opencode):
        from common.third_util.llm.opencode_client import OpencodeClient

        mock_result = MagicMock(spec=[])
        mock_opencode_instance = MagicMock()
        mock_opencode_instance.session.chat.return_value = mock_result
        mock_opencode.return_value = mock_opencode_instance

        client = OpencodeClient()
        result = client.execute_task("sid", "hi")
        self.assertIsInstance(result, str)

    @patch("common.third_util.llm.opencode_client.Opencode")
    def test_run(self, mock_opencode):
        from common.third_util.llm.opencode_client import OpencodeClient

        mock_session = MagicMock()
        mock_session.id = "session_run"
        mock_result = MagicMock()
        mock_result.content = "run result"
        mock_opencode_instance = MagicMock()
        mock_opencode_instance.session.create.return_value = mock_session
        mock_opencode_instance.session.chat.return_value = mock_result
        mock_opencode.return_value = mock_opencode_instance

        client = OpencodeClient()
        result = client.run("test prompt")
        self.assertEqual(result, "run result")
        mock_opencode_instance.session.create.assert_called_once()
        mock_opencode_instance.session.chat.assert_called_once()


if __name__ == "__main__":
    unittest.main()
